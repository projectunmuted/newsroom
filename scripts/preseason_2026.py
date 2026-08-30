#!/usr/bin/env python3
"""Pull every team's 2026 preseason record, so the published dataset has a
column for the season a reader is actually in.

    python scripts/preseason_2026.py            # table to stdout
    python scripts/preseason_2026.py --refetch   # ignore the cache

Why this exists: `datasets/` answers "does an NFL team's preseason record
predict its regular season" with 798 team-seasons ending in 2025. That is the
right answer and it is one season out of date on the only week anybody types
the question. The 2026 preseason finished 2026-08-29. A reader whose team just
went 3-0 wants the base rate *and* the list they are on, and the second half was
missing.

**These rows are not the dataset.** They have no regular season yet, so they
cannot go in the historical CSV without a schema full of blanks and a
correlation that quietly includes them. They ship as their own file, and the
regular-season columns get filled once 2026 finishes, which is a February 2027
job.

The fetch is `preseason_full.fetch`, unchanged, so the id-matching fix and the
0-0 phantom rule apply here too. Exit 2 if any team's preseason is not complete;
a partial read is not a record.

**The 3-game assumption is wrong for exactly 2 teams a year**, and the first
version of this script exited 2 because of it. Arizona and Carolina came back
with 4 finished preseason games. That is not a data defect: they played the
2026 Hall of Fame Game on 08-07, which is a preseason fixture and counts. So
completeness is tested by asking whether any scheduled fixture is still
unplayed, not by counting to 3.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import preseason_full as pf   # noqa: E402

SEASON = 2026
CACHE = os.path.join(HERE, "preseason_2026_cache.json")


def unplayed(team: str) -> list[str]:
    """Dates of fixtures ESPN lists for this team that have no final score."""
    data = pf._get(pf.API.format(team=team, season=SEASON, st=1))
    out = []
    for event in data.get("events", []):
        comp = event["competitions"][0]
        scores = [s.get("score", {}).get("value")
                  for s in comp.get("competitors", [])]
        if any(v is None for v in scores):
            out.append(event.get("date", "")[:10])
    return out


def collect(refetch: bool = False) -> list[dict]:
    if os.path.exists(CACHE) and not refetch:
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)

    rows = []
    for team in pf.TEAMS:
        w, g = pf.fetch(team, SEASON, 1)
        rows.append({"team": team, "season": SEASON, "pre_w": w, "pre_g": g,
                     "pre_pct": (w / g) if g else 0.0,
                     "unplayed": unplayed(team)})
        print("  %s %g-%g" % (team, w, g - w), file=sys.stderr)
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
    return rows


def main() -> int:
    rows = collect("--refetch" in sys.argv)
    pending = [r for r in rows if r.get("unplayed")]
    empty = [r for r in rows if not r["pre_g"]]

    rows.sort(key=lambda r: (-r["pre_pct"], r["team"]))
    print("2026 preseason, %d teams" % len(rows))
    for r in rows:
        print("  %-4s %g-%g  %.3f"
              % (r["team"], r["pre_w"], r["pre_g"] - r["pre_w"], r["pre_pct"]))

    if len(rows) != 32:
        sys.stderr.write("expected 32 teams, got %d\n" % len(rows))
        return 2
    if empty:
        sys.stderr.write("no finished games for %s\n"
                         % ", ".join(r["team"] for r in empty))
        return 2
    if pending:
        sys.stderr.write(
            "partial: fixtures still unplayed for %s\n"
            % ", ".join("%s (%s)" % (r["team"], ",".join(r["unplayed"]))
                        for r in pending))
        return 2
    four = [r["team"] for r in rows if r["pre_g"] == 4]
    print("\nEvery listed fixture is final. %d teams played 4 (%s); the rest "
          "played 3. Exit 0."
          % (len(four), ", ".join(sorted(four)) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
