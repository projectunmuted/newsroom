#!/usr/bin/env python3
"""Read Cloudflare Web Analytics page views for both sites.

Why this exists: `check_live.py` asserts the beacon *tag* is in the live HTML,
which is one step short of the truth. On 2026-08-12 both sites carried the tag
and collected nothing, because the beacon's POST to `cdn-cgi/rum` was answered
503 and the tag being present says nothing about whether the far end accepts it.

So this asks the only question that settles it: does Cloudflare hold any page
views for these hostnames? A number here means the whole chain works. A zero
against a site that has demonstrably had readers means it does not, whatever
the HTML says.

Credentials come from `.cloudflare.json` in the main checkout (gitignored, and
absent from every worktree — see `local_config` in build.py for that trap).
Token needs Account / Account Analytics / Read and nothing else.

    python scripts/read_analytics.py [--days 7]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from build import DSR, JOURNAL, local_config  # noqa: E402

GRAPHQL = "https://api.cloudflare.com/client/v4/graphql"

# Every hostname the beacon should be reporting from, and the site it belongs
# to. requestHost is what the RUM dataset records, so this is the join key.
HOSTS = {
    DSR.base_url.split("//")[1]: "detroitsportsreporter.com",
    JOURNAL.base_url.split("//")[1]: "project-unmuted.com",
}

QUERY = """
query($acct:String!,$since:Time!,$until:Time!){
  viewer{ accounts(filter:{accountTag:$acct}){
    rumPageloadEventsAdaptiveGroups(
      limit:1000,
      filter:{datetime_geq:$since, datetime_leq:$until, bot:0},
      orderBy:[date_ASC]
    ){ count dimensions{ date requestHost } }
  }}}
"""


def load_creds() -> tuple[str, str]:
    path = local_config(".cloudflare.json")
    if path is None:
        sys.exit("no .cloudflare.json in the main checkout; see ASK-HUMAN.md")
    cfg = json.loads(path.read_text(encoding="utf-8"))
    acct, token = cfg.get("account_id", ""), cfg.get("token", "")
    if not acct or not token:
        sys.exit(".cloudflare.json has an empty account_id or token")
    return acct, token


def query(acct: str, token: str, days: int) -> list[dict]:
    since = (date.today() - timedelta(days=days)).isoformat() + "T00:00:00Z"
    until = (date.today() + timedelta(days=1)).isoformat() + "T00:00:00Z"
    body = json.dumps({"query": QUERY, "variables": {
        "acct": acct, "since": since, "until": until}}).encode()
    req = urllib.request.Request(GRAPHQL, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Cloudflare returned HTTP {e.code}. A 403 usually means the "
                 f"token lacks Account Analytics: Read.")
    if payload.get("errors"):
        sys.exit(f"GraphQL errors: {json.dumps(payload['errors'])[:400]}")
    accounts = payload["data"]["viewer"]["accounts"]
    if not accounts:
        sys.exit("no such account, or the token cannot see it. Check account_id.")
    return accounts[0]["rumPageloadEventsAdaptiveGroups"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()

    acct, token = load_creds()
    rows = query(acct, token, args.days)

    totals: dict[str, int] = {h: 0 for h in HOSTS}
    per_day: dict[str, dict[str, int]] = {h: {} for h in HOSTS}
    other: dict[str, int] = {}
    for r in rows:
        host = r["dimensions"]["requestHost"]
        if host in totals:
            totals[host] += r["count"]
            per_day[host][r["dimensions"]["date"]] = (
                per_day[host].get(r["dimensions"]["date"], 0) + r["count"])
        else:
            other[host] = other.get(host, 0) + r["count"]

    print(f"Cloudflare Web Analytics, last {args.days} days, bots excluded\n")
    dead = []
    for host, total in totals.items():
        print(f"{host}: {total} page views")
        for day, n in sorted(per_day[host].items()):
            print(f"    {day}  {n}")
        if total == 0:
            print("    nothing recorded. If the site has had readers, the "
                  "beacon is being rejected, not missing. Load the page in a "
                  "browser and watch the POST to cloudflareinsights.com/cdn-cgi/rum.")
            dead.append(host)
    if other:
        print("\nOther hostnames on this account:")
        for host, n in sorted(other.items(), key=lambda kv: -kv[1]):
            print(f"    {host}  {n}")

    # Non-zero exit when a site reports nothing at all, so a cycle cannot read
    # "0" as a fact about readers when it is a fact about the instrument.
    return 1 if dead else 0


if __name__ == "__main__":
    raise SystemExit(main())
