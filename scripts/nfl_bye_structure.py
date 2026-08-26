#!/usr/bin/env python3
"""Where every NFL team's bye falls in 2026, and how long the run after it is.

Pulls all 32 regular-season schedules from ESPN's public JSON on every run.
Nothing is hardcoded except the team list endpoint, so re-running this IS the
diff. Prints the arithmetic beside every value.

Exit 0 = complete read of all 32 clubs. Exit 2 = partial; do not publish from a 2.

Usage:
    python scripts/nfl_bye_structure.py [--season 2026] [--csv out.csv]
"""
import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request

TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
SCHED_URL = ("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/"
             "{abbr}/schedule?season={season}&seasontype=2")
LAST_WEEK = 18


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def teams():
    d = get(TEAMS_URL)
    rows = d["sports"][0]["leagues"][0]["teams"]
    return [(t["team"]["abbreviation"].lower(), t["team"]["displayName"]) for t in rows]


def schedule(abbr, season):
    """Return {week: (datetime, opp_abbr, home_or_away)} for the regular season."""
    d = get(SCHED_URL.format(abbr=abbr, season=season))
    me = abbr.upper()
    games = {}
    for e in d.get("events", []):
        wk = (e.get("week") or {}).get("number")
        if not wk:
            continue
        comp = e["competitions"][0]
        dt = datetime.datetime.strptime(e["date"], "%Y-%m-%dT%H:%MZ")
        mine = [c for c in comp["competitors"]
                if c["team"]["abbreviation"].upper() == me]
        other = [c for c in comp["competitors"]
                 if c["team"]["abbreviation"].upper() != me]
        if not mine or not other:
            continue
        games[wk] = (dt, other[0]["team"]["abbreviation"], mine[0]["homeAway"])
    return games


def analyse(games):
    played = sorted(games)
    byes = [w for w in range(1, LAST_WEEK + 1) if w not in games]
    bye = byes[0] if len(byes) == 1 else None
    after = len([w for w in played if bye and w > bye])
    before = len([w for w in played if bye and w < bye])
    # short weeks: fewer than 6 full days between kickoffs
    short = []
    for i in range(1, len(played)):
        prev, cur = games[played[i - 1]][0], games[played[i]][0]
        gap = (cur - prev).days
        if gap <= 4:
            short.append((played[i], gap, games[played[i]][1]))
    return {
        "weeks": played,
        "byes": byes,
        "bye": bye,
        "before": before,
        "after": after,
        "short": short,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--csv")
    a = ap.parse_args()

    try:
        roster = teams()
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        print("FAILED to read the team list: %s" % exc)
        return 2

    rows, failures = [], []
    for abbr, name in roster:
        try:
            g = schedule(abbr, a.season)
        except (urllib.error.URLError, ValueError) as exc:
            failures.append("%s (%s)" % (abbr, exc))
            continue
        if len(g) != LAST_WEEK - 1:
            failures.append("%s returned %d games, expected %d"
                            % (abbr, len(g), LAST_WEEK - 1))
            continue
        r = analyse(g)
        if r["bye"] is None:
            failures.append("%s has byes %s, expected exactly 1" % (abbr, r["byes"]))
            continue
        r["abbr"] = abbr.upper()
        r["name"] = name
        rows.append(r)

    print("Season %d, regular season only. %d of %d clubs read."
          % (a.season, len(rows), len(roster)))
    print()

    if rows:
        print("Bye week, then the unbroken run of games after it.")
        print("  run after bye = %d - bye week, because the last week is %d."
              % (LAST_WEEK, LAST_WEEK))
        print()
        print("%-4s %-24s %4s %7s %6s  %s"
              % ("", "club", "bye", "before", "after", "short weeks (<=4 days)"))
        for r in sorted(rows, key=lambda x: (x["bye"], -x["after"])):
            sw = ", ".join("wk%d %dd vs %s" % (w, g, o) for w, g, o in r["short"]) or "-"
            print("%-4s %-24s %4d %7d %6d  %s"
                  % (r["abbr"], r["name"], r["bye"], r["before"], r["after"], sw))
        print()
        earliest = min(r["bye"] for r in rows)
        longest = max(r["after"] for r in rows)
        print("Earliest bye in the league: week %d (%s)"
              % (earliest, ", ".join(r["abbr"] for r in rows if r["bye"] == earliest)))
        print("Longest run after a bye: %d games (%s)"
              % (longest, ", ".join(r["abbr"] for r in rows if r["after"] == longest)))
        byecount = {}
        for r in rows:
            byecount[r["bye"]] = byecount.get(r["bye"], 0) + 1
        print("Byes per week: " + ", ".join("wk%d=%d" % (w, byecount[w])
                                            for w in sorted(byecount)))
        det = [r for r in rows if r["abbr"] == "DET"]
        if det:
            d = det[0]
            rank = sorted(rows, key=lambda x: (x["bye"], -x["after"]))
            pos = [i for i, r in enumerate(rank) if r["abbr"] == "DET"][0] + 1
            print()
            print("DETROIT: bye week %d, %d games before it, %d after."
                  % (d["bye"], d["before"], d["after"]))
            print("  %d of %d clubs have a bye no later than Detroit's."
                  % (len([r for r in rows if r["bye"] <= d["bye"]]), len(rows)))
            print("  %d of %d clubs finish with a longer unbroken run."
                  % (len([r for r in rows if r["after"] > d["after"]]), len(rows)))
            print("  ordering position (bye asc, then run desc): %d" % pos)
            early_bye = [r for r in rows if r["bye"] <= d["bye"]]
            early_short = [r for r in rows
                           if any(w <= d["bye"] for w, _, _ in r["short"])]
            both = [r["abbr"] for r in early_bye
                    if r["abbr"] in {x["abbr"] for x in early_short}]
            print("  clubs with a bye by week %d: %s"
                  % (d["bye"], ", ".join(sorted(r["abbr"] for r in early_bye))))
            print("  clubs with a short week by week %d: %s"
                  % (d["bye"], ", ".join(sorted(r["abbr"] for r in early_short))))
            print("  BOTH (early bye and early short week): %s"
                  % ", ".join(sorted(both)))
            two = sorted(r["abbr"] for r in rows if len(r["short"]) >= 2)
            none_ = sorted(r["abbr"] for r in rows if not r["short"])
            print("  clubs with 2+ short weeks (%d): %s" % (len(two), ", ".join(two)))
            print("  clubs with 0 short weeks (%d): %s" % (len(none_), ", ".join(none_)))
            first_short = min((w for r in rows for w, _, _ in r["short"]))
            owners = sorted({r["abbr"] for r in rows
                             for w, _, _ in r["short"] if w == first_short})
            print("  earliest short week anywhere: week %d (%s)"
                  % (first_short, ", ".join(owners)))

    if a.csv and rows:
        with open(a.csv, "w", encoding="utf-8") as fh:
            fh.write("abbr,name,bye,before,after\n")
            for r in rows:
                fh.write("%s,%s,%d,%d,%d\n"
                         % (r["abbr"], r["name"], r["bye"], r["before"], r["after"]))
        print("\nwrote %s" % a.csv)

    if failures:
        print()
        print("PARTIAL READ. %d club(s) unusable:" % len(failures))
        for f in failures:
            print("  " + f)
        print("Exit 2: do not publish a league-wide claim off this run.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
