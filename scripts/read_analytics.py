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

## The sampling cliff (found 2026-08-16, and it had been silently live)

`rumPageloadEventsAdaptiveGroups` is an *adaptive* dataset: Cloudflare picks
which underlying table answers a query from the time range asked for. Measured
on this account, on 2026-08-16:

    since >= 2026-08-09T00:00:00Z  ->  sampleInterval ~1    (raw)
    since <= 2026-08-08T23:00:00Z  ->  sampleInterval 10    (1-in-10 sample)

That cliff is exactly 7 days back at UTC midnight, and the trigger is the
**start** of the window, not its length: a 5-day query starting 8 days ago is
sampled too.

What makes it dangerous rather than merely coarse is that the whole answer
degrades, including the recent days that *are* held at full resolution. At a
sample interval of 10, any day under about 10 views has no sampled event to
scale up and so returns **no row at all**. Measured, same account, same minute:

    --days 7   ->  08-12: 6, 08-13: 13, 08-14: 16, 08-15: 5, 08-16: 6
    --days 8   ->  08-12: 10, and 08-13 through 08-16 do not exist

Asking for one more day of history deleted four of the last five days, with no
error and exit code 0. The old default of `--days 7` sat one day inside the
cliff by luck, not by choice.

Two things follow, and both are implemented below:

1. **Chunk the window.** Slices are cut so the recent ones stay on the raw
   table, so a 30-day request now returns real daily numbers for the last week
   instead of destroying them. History older than the cliff is genuinely only
   available sampled; that is Cloudflare's retention, not a bug here.
2. **Never report a sampled number as if it were a count.** Every query asks
   for `sampleInterval`, every sampled day is marked in the output, and the run
   **exits 2** on partial resolution, the same convention `injury_check.py` and
   `reddit_rss.py` use. An instrument that cannot say it degraded gets read as
   if it did not, which is the failure this repo keeps paying for.

Note `count` and `visits` are different questions: `count` is pageloads (what
"page views" means everywhere else in this repo) and `visits` is sessions
arriving from outside. Both are printed, because on 2026-08-14 they were 16 and
6, and a cycle quoting the wrong one would be off by more than double.

Credentials come from `.cloudflare.json` in the main checkout (gitignored, and
absent from every worktree — see `local_config` in build.py for that trap).
Token needs Account / Account Analytics / Read and nothing else.

    python scripts/read_analytics.py [--days 7] [--paths] [--referers] [--hourly]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
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

# How far back the raw table reaches, measured rather than assumed. Slices are
# cut against this so the recent end of a long window never gets dragged onto
# the sampled table. If Cloudflare moves the cliff, the sampleInterval readings
# below say so out loud rather than this constant quietly becoming a lie.
RAW_DAYS = 7

# Above this, a row is a scaled-up sample rather than a count, and days quieter
# than the interval vanish entirely instead of reporting zero.
SAMPLED_AT = 1.5

QUERY = """
query($acct:String!,$since:Time!,$until:Time!){
  viewer{ accounts(filter:{accountTag:$acct}){
    rumPageloadEventsAdaptiveGroups(
      limit:5000,
      filter:{datetime_geq:$since, datetime_lt:$until, bot:0 %(extra)s},
      orderBy:[%(order)s_ASC]
    ){ count sum{visits} avg{sampleInterval} dimensions{ %(dims)s requestHost } }
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


def fetch(acct: str, token: str, since: str, until: str,
          dims: str, order: str, page: str | None = None) -> list[dict]:
    """One slice. Raises nothing useful to callers; exits on a hard failure,
    because a half-read number is worse than no number."""
    extra = f', requestPath:"{page}"' if page else ""
    body = json.dumps({"query": QUERY % {"dims": dims, "order": order,
                                         "extra": extra},
                       "variables": {"acct": acct, "since": since,
                                     "until": until}}).encode()
    req = urllib.request.Request(GRAPHQL, data=body, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
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


def slices(days: int) -> list[tuple[str, str]]:
    """Cut the window so the raw-table portion is never dragged onto the
    sampled table by an older sibling in the same query.

    Anchored to the *end* and cut at the cliff, so the most recent slice is
    always fully inside the raw window. Half-open with datetime_lt, so an event
    on a boundary instant is counted once and not twice.
    """
    now = datetime.now(timezone.utc)
    end = (now.date() + timedelta(days=1))
    start = now.date() - timedelta(days=days)
    cliff = now.date() - timedelta(days=RAW_DAYS)

    edges = [start]
    if start < cliff < end:
        edges.append(cliff)
    edges.append(end)
    fmt = "%Y-%m-%dT00:00:00Z"
    return [(a.strftime(fmt), b.strftime(fmt))
            for a, b in zip(edges, edges[1:]) if a < b]


def collect(acct: str, token: str, days: int, dims: str, order: str,
            page: str | None = None) -> tuple[list[dict], float, list[str]]:
    """Every slice, merged, plus the worst sample interval seen and the list of
    slices that came back sampled."""
    rows: list[dict] = []
    worst = 1.0
    degraded: list[str] = []
    for since, until in slices(days):
        got = fetch(acct, token, since, until, dims, order, page)
        si = max([r["avg"]["sampleInterval"] for r in got], default=1.0)
        worst = max(worst, si)
        if si > SAMPLED_AT:
            degraded.append(f"{since[:10]} to {until[:10]} (1 in {si:g})")
        for r in got:
            r["_sampled"] = si > SAMPLED_AT
        rows.extend(got)
    return rows, worst, degraded


def breakdown(rows: list[dict], key: str, title: str) -> None:
    """Group the merged rows by one dimension, per site, biggest first."""
    print(f"\n{title}")
    for host in HOSTS:
        agg: dict[str, int] = {}
        for r in rows:
            if r["dimensions"]["requestHost"] != host:
                continue
            k = r["dimensions"].get(key) or "(none)"
            agg[k] = agg.get(k, 0) + r["count"]
        if not agg:
            continue
        print(f"  {host}")
        for k, n in sorted(agg.items(), key=lambda kv: (-kv[1], kv[0]))[:20]:
            print(f"    {n:5d}  {k}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--paths", action="store_true",
                    help="which pages were read")
    ap.add_argument("--referers", action="store_true",
                    help="where readers came from; the only direct evidence "
                         "a Reddit post sent anybody")
    ap.add_argument("--hourly", action="store_true",
                    help="hour buckets, for reconstructing a post's effect "
                         "without a baseline written down in advance")
    ap.add_argument("--page", metavar="PATH",
                    help="count one exact path, e.g. /requests.html. This is "
                         "the only way to get an unsampled answer about a "
                         "single page: asking for requestPath as a dimension "
                         "samples 1 in 2, and a page with one real view can "
                         "then be missing rather than zero")
    args = ap.parse_args()

    # Git Bash on Windows rewrites a leading-slash argument into a Windows
    # path, so `--page /requests.html` arrives as `C:/Program Files/Git/
    # requests.html` and returns a truthful zero about a path that does not
    # exist. Caught doing exactly that on 2026-08-16. Refuse it rather than
    # answer it, because the wrong answer here looks identical to the right one.
    if args.page and not args.page.startswith("/"):
        sys.exit(f"--page must be a site path starting with '/', got "
                 f"{args.page!r}. On Git Bash prefix the command with "
                 f"MSYS_NO_PATHCONV=1, or use PowerShell.")

    acct, token = load_creds()
    bucket = "datetimeHour" if args.hourly else "date"
    dims = bucket
    if args.paths:
        dims += " requestPath"
    if args.referers:
        dims += " refererHost"
    rows, worst, degraded = collect(acct, token, args.days, dims, bucket,
                                    args.page)

    totals: dict[str, int] = {h: 0 for h in HOSTS}
    visits: dict[str, int] = {h: 0 for h in HOSTS}
    per_day: dict[str, dict[str, list]] = {h: {} for h in HOSTS}
    other: dict[str, int] = {}
    for r in rows:
        host = r["dimensions"]["requestHost"]
        if host in totals:
            totals[host] += r["count"]
            visits[host] += r["sum"]["visits"]
            cell = per_day[host].setdefault(r["dimensions"][bucket], [0, False])
            cell[0] += r["count"]
            cell[1] = cell[1] or r["_sampled"]
        else:
            other[host] = other.get(host, 0) + r["count"]

    scope = f", path {args.page}" if args.page else ""
    print(f"Cloudflare Web Analytics, last {args.days} days{scope}, "
          f"bots excluded")
    print(f"queried in {len(slices(args.days))} slice(s) to stay on the raw "
          f"table where possible\n")
    dead = []
    for host, total in totals.items():
        print(f"{host}: {total} page views, {visits[host]} visits")
        for day, (n, sampled) in sorted(per_day[host].items()):
            print(f"    {day}  {n}{'   [sampled, not a count]' if sampled else ''}")
        if total == 0 and not args.page:
            print("    nothing recorded. If the site has had readers, the "
                  "beacon is being rejected, not missing. Load the page in a "
                  "browser and watch the POST to cloudflareinsights.com/cdn-cgi/rum.")
            dead.append(host)
        elif total == 0:
            print("    nobody has loaded this page. Scoped to one path, so "
                  "this is a fact about the page, not about the beacon.")

    if args.paths:
        breakdown(rows, "requestPath", "Pages read:")
    if args.referers:
        breakdown(rows, "refererHost", "Referrers ((none) = typed, bookmarked "
                                       "or stripped):")

    if other:
        print("\nOther hostnames on this account:")
        for host, n in sorted(other.items(), key=lambda kv: -kv[1]):
            print(f"    {host}  {n}")

    if degraded:
        print(f"\nPARTIAL: {len(degraded)} slice(s) came back sampled rather "
              f"than counted:")
        for d in degraded:
            print(f"    {d}")
        print(f"    At 1 in {worst:g}, a day with fewer views than that has no "
              f"sampled event to scale up and is **missing rather than zero**. "
              f"Do not read an absent day as no readers, and do not put a "
              f"sampled figure in MEASURE.md without saying it is sampled. "
              f"Cloudflare holds the raw table for about {RAW_DAYS} days.")

    # 2 = the report is partial, matching injury_check.py and reddit_rss.py.
    # 1 = a site is reporting nothing at all, which is an instrument failure.
    if dead:
        return 1
    return 2 if degraded else 0


if __name__ == "__main__":
    raise SystemExit(main())
