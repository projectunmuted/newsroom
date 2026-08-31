#!/usr/bin/env python3
"""Which team is closest to breaking its coverage floor, read off entries/.

CALENDAR.md sets the floor: no team goes more than 7 days without an analysis
piece in season, or 14 days out of season. Nothing in the repo enforced it, and
on 2026-08-26 a cycle found the Lions floor had been past due for 4 days with
nothing anywhere announcing it.

Season state is derived from the schedule endpoints, not hardcoded, so this file
does not go stale in October. In season means the club played inside the last 30
days or plays inside the next 10, preseason included. The forward window is the
short one on purpose: on 2026-08-26 a symmetric 30 days called the Red Wings in
season off a preseason game 26 days out, which would have moved their floor from
14 days to 7 for a club that has not played since spring.

    python scripts/coverage_floor.py
    python scripts/coverage_floor.py --today 2026-08-26

Exit 0 = every team inside its floor. Exit 1 = at least one team is over.
Exit 2 = the season state could not be read; the day counts are still printed
but do not act on the floor column.
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTRIES = ROOT / "entries"

TEAMS = {
    "tigers": ("Tigers", "mlb", "https://statsapi.mlb.com/api/v1/schedule"
                                "?sportId=1&teamId=116&startDate={lo}&endDate={hi}"),
    "lions": ("Lions", "espn", "det/football/nfl"),
    "pistons": ("Pistons", "espn", "det/basketball/nba"),
    "redwings": ("Red Wings", "espn", "det/hockey/nhl"),
}
ALIASES = {"red-wings": "redwings", "wings": "redwings", "red_wings": "redwings"}

IN_SEASON_FLOOR = 7
OFF_SEASON_FLOOR = 14
BACK, AHEAD = 30, 10


def last_pieces():
    """Newest analysis-track entry date per team slug."""
    seen = {}
    for f in sorted(ENTRIES.glob("*.md")):
        head = f.read_text(encoding="utf-8", errors="replace").split("---")[1:2]
        if not head:
            continue
        fm = head[0]
        if not re.search(r"^track:\s*analysis\s*$", fm, re.M):
            continue
        # `team:` is one slug normally and a comma separated list for the
        # Monday column, which covers all 4 clubs and should satisfy all 4
        # floors. A single-slug regex silently credited none of them.
        m = re.search(r"^team:\s*\"?([A-Za-z_,\s-]+?)\"?\s*$", fm, re.M)
        d = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", fm, re.M)
        if not m or not d:
            continue
        date = datetime.date.fromisoformat(d.group(1))
        for part in m.group(1).split(","):
            part = part.strip().lower()
            if not part:
                continue
            slug = ALIASES.get(part, part)
            if slug not in seen or date > seen[slug][0]:
                seen[slug] = (date, f.name)
    return seen


def in_season(slug, today):
    """True if the club played in the last BACK days or plays in the next AHEAD."""
    name, kind, spec = TEAMS[slug]
    lo = (today - datetime.timedelta(days=BACK)).isoformat()
    hi = (today + datetime.timedelta(days=AHEAD)).isoformat()
    if kind == "mlb":
        with urllib.request.urlopen(spec.format(lo=lo, hi=hi), timeout=30) as r:
            d = json.load(r)
        return sum(len(x["games"]) for x in d.get("dates", [])) > 0
    abbr, sport, league = spec.split("/")
    found = 0
    for st in (1, 2, 3):
        url = ("https://site.api.espn.com/apis/site/v2/sports/%s/%s/teams/%s"
               "/schedule?seasontype=%d" % (sport, league, abbr, st))
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                d = json.load(r)
        except Exception:
            continue
        for e in d.get("events", []):
            try:
                dt = datetime.datetime.strptime(e["date"], "%Y-%m-%dT%H:%MZ").date()
            except ValueError:
                continue
            if -BACK <= (dt - today).days <= AHEAD:
                found += 1
    return found > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today")
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()

    seen = last_pieces()
    partial, over = False, False
    print("Coverage floor as of %s. In season = played in the last %d days or "
          "plays in the next %d, preseason included." % (today, BACK, AHEAD))
    print()
    print("%-11s %-12s %-6s %-10s %-5s %s"
          % ("team", "last piece", "age", "state", "floor", "verdict"))
    for slug, (name, _, _) in TEAMS.items():
        rec = seen.get(slug)
        try:
            live = in_season(slug, today)
            state = "in season" if live else "offseason"
            floor = IN_SEASON_FLOOR if live else OFF_SEASON_FLOOR
        except Exception as exc:
            partial = True
            state, floor = "UNKNOWN(%s)" % type(exc).__name__, None
        if rec is None:
            age, last = None, "never"
        else:
            age, last = (today - rec[0]).days, rec[0].isoformat()
        if floor is None or age is None:
            verdict = "check by hand"
        elif age > floor:
            verdict = "OVER by %d day(s)" % (age - floor)
            over = True
        else:
            verdict = "ok, due %s" % (rec[0] + datetime.timedelta(days=floor))
        print("%-11s %-12s %-6s %-10s %-5s %s"
              % (name, last, "%dd" % age if age is not None else "-",
                 state, floor if floor else "?", verdict))

    if partial:
        print("\nPARTIAL: a season state could not be read. Exit 2.")
        return 2
    if over:
        print("\nAt least one team is past its floor. Exit 1.")
        return 1
    print("\nEvery team inside its floor. Exit 0.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
