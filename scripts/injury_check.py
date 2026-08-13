#!/usr/bin/env python3
"""Who is not available, for both teams in a game, before the pick is committed.

Written 2026-08-13, after grading the first miss, because of a near thing rather
than a disaster.

Pick 5 was committed at 16:43 ET on 2026-08-12. At 16:48 ET, 5 minutes later,
r/motorcitykitties posted that Detroit had placed **Riley Greene** on the 10-day
injured list with a right hamstring strain. Greene has 492 plate appearances and
an .816 OPS, which is the most of anybody on the roster and the best mark of any
regular. A published prediction on a Tigers game that does not mention their best
hitter being unavailable is the kind of thing a reader catches first, and the
answer "it broke 5 minutes after I hit commit" is true exactly once.

The uncomfortable part is not the timing. It is that **nothing in this project
has ever checked an injury list.** Not the sweep, not the pick routine, not any
of the other 27 scripts. Greene was missed by luck rather than caught by process,
and the same luck runs the other way just as easily.

So this runs before a pick gets committed, and it answers 2 questions:

  1. **What changed recently?** The league's own transactions feed for both
     clubs, default the last 3 days. This is where an IL placement shows up
     first, with the injury named.
  2. **Who is out right now, and does it matter?** Everybody on the 40-man
     roster whose status is not Active, ranked by how much they have actually
     played this season. A 12th reliever on the 60-day and the team's best hitter
     on the 10-day arrive from the API looking identical, and they are not.

"Does it matter" is deliberately crude: plate appearances for hitters, innings
for pitchers, with a line drawn at 200 PA or 40 IP. That is not a value metric
and it is not trying to be. It is a filter that puts Riley Greene above the guy
who threw 1.2 innings in April, so the reader of the output sees the name that
changes the analysis without reading 23 rows.

**Reassigned to Minors and Designated for Assignment are reported too**, under a
separate heading, because they are availability changes and not injuries. Rolling
them in with the IL would overstate the injury list.

    python scripts/injury_check.py 824238        # both teams in that game
    python scripts/injury_check.py --team 116    # one club by MLB team id
    python scripts/injury_check.py 824238 --days 7 --json

**Exit codes matter here and they follow this project's standing lesson.** An
instrument that cannot report its own failure gets read as if it succeeded, which
is how the sweep spent 4 cycles calling subs it never reached empty. So:

  0  every fetch landed, and the report below is complete
  2  at least one fetch failed, the report is partial, and **an empty injury
     list from this run means nothing**

An exit of 2 is not "no news". It is "I do not know", and the two must never
print the same way.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "logs" / "injury-check-cache.json"
CACHE_MINUTES = 20
SEASON = 2026
API = "https://statsapi.mlb.com/api/v1"

# The line between "a name that changes the analysis" and roster depth. Crude on
# purpose; see the module docstring.
NOTABLE_PA = 200
NOTABLE_IP = 40.0

# Statuses that are an availability change but not an injury.
NON_INJURY = {"RM", "DES", "DEV", "RA"}


class Incomplete(Exception):
    """A fetch failed. The caller must not read absence as evidence."""


def _cache_read() -> dict:
    if not CACHE.exists():
        return {}
    try:
        blob = json.loads(CACHE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if time.time() - blob.get("fetched_at", 0) > CACHE_MINUTES * 60:
        return {}
    return blob.get("urls", {})


def _cache_write(urls: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(
        json.dumps({"fetched_at": time.time(), "urls": urls}, indent=1),
        encoding="utf-8",
    )


_MEM: dict = {}
_FAILURES: list[str] = []


def get(url: str) -> dict:
    """Fetch JSON, caching for CACHE_MINUTES. Raises Incomplete on failure."""
    if url in _MEM:
        return _MEM[url]
    try:
        with urllib.request.urlopen(url, timeout=30) as fh:
            data = json.loads(fh.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        _FAILURES.append(f"{url} -> {exc}")
        raise Incomplete(url) from exc
    _MEM[url] = data
    return data


def teams_in_game(game_pk: int) -> list[tuple[int, str]]:
    d = get(f"{API}/schedule?gamePk={game_pk}")
    dates = d.get("dates") or []
    if not dates or not dates[0].get("games"):
        raise Incomplete(f"gamePk {game_pk} returned no game")
    g = dates[0]["games"][0]
    return [
        (g["teams"]["away"]["team"]["id"], g["teams"]["away"]["team"]["name"]),
        (g["teams"]["home"]["team"]["id"], g["teams"]["home"]["team"]["name"]),
    ]


def team_name(team_id: int) -> str:
    d = get(f"{API}/teams/{team_id}?season={SEASON}")
    return d["teams"][0]["name"]


def transactions(team_id: int, days: int, today: str) -> list[dict]:
    start = _days_before(today, days)
    d = get(
        f"{API}/transactions?teamId={team_id}&startDate={start}&endDate={today}"
    )
    return d.get("transactions", [])


def _days_before(iso: str, days: int) -> str:
    import datetime

    d = datetime.date.fromisoformat(iso) - datetime.timedelta(days=days)
    return d.isoformat()


def unavailable(team_id: int) -> list[dict]:
    """Everyone on the 40-man whose status is not Active, with workload."""
    d = get(f"{API}/teams/{team_id}/roster?rosterType=40Man&season={SEASON}")
    rows = [
        r for r in d.get("roster", []) if r.get("status", {}).get("code") != "A"
    ]
    if not rows:
        return []

    ids = ",".join(str(r["person"]["id"]) for r in rows)
    people = get(
        f"{API}/people?personIds={ids}"
        f"&hydrate=stats(group=[hitting,pitching],type=season,season={SEASON})"
    )
    stats = {p["id"]: p for p in people.get("people", [])}

    out = []
    for r in rows:
        pid = r["person"]["id"]
        person = stats.get(pid, {})
        pa = ip = 0.0
        ops = era = None
        for grp in person.get("stats", []):
            splits = grp.get("splits") or []
            if not splits:
                continue
            st = splits[0].get("stat", {})
            if grp["group"]["displayName"] == "hitting":
                pa = float(st.get("plateAppearances") or 0)
                ops = st.get("ops")
            elif grp["group"]["displayName"] == "pitching":
                ip = float(st.get("inningsPitched") or 0)
                era = st.get("era")
        status = r.get("status", {})
        out.append(
            {
                "name": r["person"]["fullName"],
                "position": r["position"]["abbreviation"],
                "status_code": status.get("code"),
                "status": status.get("description"),
                "injury": status.get("code") not in NON_INJURY,
                "pa": int(pa),
                "ip": ip,
                "ops": ops,
                "era": era,
                "notable": pa >= NOTABLE_PA or ip >= NOTABLE_IP,
            }
        )
    # Rank by workload so the name that changes the analysis is at the top.
    out.sort(key=lambda r: max(r["pa"] / NOTABLE_PA, r["ip"] / NOTABLE_IP), reverse=True)
    return out


def report(team_id: int, days: int, today: str) -> dict:
    partial = []
    name = f"team {team_id}"
    try:
        name = team_name(team_id)
    except Incomplete:
        partial.append("team name")
    try:
        txns = transactions(team_id, days, today)
    except Incomplete:
        txns, partial = [], partial + ["transactions"]
    try:
        out = unavailable(team_id)
    except Incomplete:
        out, partial = [], partial + ["roster/status"]
    return {
        "team_id": team_id,
        "team": name,
        "transactions": txns,
        "unavailable": out,
        "incomplete": partial,
    }


def render(rep: dict, days: int) -> None:
    print(f"\n=== {rep['team']}")

    if rep["incomplete"]:
        print(f"  !! INCOMPLETE: could not fetch {', '.join(rep['incomplete'])}.")
        print("     An empty list below is 'I do not know', not 'nothing to report'.")

    txns = rep["transactions"]
    print(f"\n  Transactions, last {days} days ({len(txns)}):")
    if not txns and "transactions" not in rep["incomplete"]:
        print("    none")
    for t in txns:
        print(f"    {t.get('date')}  {t.get('typeDesc')}: {t.get('description')}")

    injured = [r for r in rep["unavailable"] if r["injury"]]
    other = [r for r in rep["unavailable"] if not r["injury"]]

    notable = [r for r in injured if r["notable"]]
    print(f"\n  Injured, and they have played enough to matter ({len(notable)}):")
    if not notable and "roster/status" not in rep["incomplete"]:
        print("    none")
    for r in notable:
        print(f"    {_line(r)}")

    rest = [r for r in injured if not r["notable"]]
    print(f"\n  Injured, light workload this season ({len(rest)}):")
    for r in rest:
        print(f"    {_line(r)}")

    if other:
        print(f"\n  Not injured, but unavailable ({len(other)}):")
        for r in other:
            print(f"    {_line(r)}")


def _line(r: dict) -> str:
    # Use the listed position, not a PA-vs-IP comparison. A pitcher who has not
    # thrown this season has 0 of each, and 0 >= 0 rendered him as a hitter with
    # "0 PA, OPS -", which is the wrong stat line for the wrong reason.
    if r["position"] == "P":
        load = f"{r['ip']} IP, ERA {r['era'] or '-'}"
    else:
        load = f"{r['pa']} PA, OPS {r['ops'] or '-'}"
    return f"{r['name']:<24} {r['position']:<3} {r['status']:<22} {load}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("game_pk", nargs="?", type=int, help="MLB gamePk")
    ap.add_argument("--team", type=int, action="append", help="MLB team id")
    ap.add_argument("--days", type=int, default=3, help="transaction window")
    ap.add_argument("--date", help="treat this ISO date as today")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.game_pk and not args.team:
        ap.error("give a gamePk or at least one --team")

    import datetime

    today = args.date or datetime.date.today().isoformat()

    cached = _cache_read()
    _MEM.update(cached)

    targets: list[int] = list(args.team or [])
    if args.game_pk:
        try:
            targets = [t[0] for t in teams_in_game(args.game_pk)] + targets
        except Incomplete:
            print(f"!! could not resolve gamePk {args.game_pk}", file=sys.stderr)

    reports = [report(t, args.days, today) for t in targets]
    _cache_write(_MEM)

    incomplete = any(r["incomplete"] for r in reports) or not targets

    if args.json:
        print(json.dumps({"reports": reports, "complete": not incomplete}, indent=1))
    else:
        for rep in reports:
            render(rep, args.days)
        print()
        if incomplete:
            print("EXIT 2: the report above is PARTIAL. Do not read an empty")
            print("injury list as 'nobody is hurt'. Re-run before committing a pick.")
            for f in _FAILURES:
                print(f"  failed: {f}")
        else:
            print("EXIT 0: every fetch landed. The lists above are complete.")

    return 2 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main())
