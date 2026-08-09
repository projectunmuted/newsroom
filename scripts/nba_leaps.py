"""Two-year win swings in the NBA, and what happens the year after.

Detroit went 14-68, then 44-38, then 60-22. That is a two-season swing of +46
wins. This script finds every comparable swing in the league's modern history
and reports what each of those teams did the following season.

Shortened seasons are the trap here. 2012 was 66 games, 2020 was suspended at
between 64 and 75 games per team, and 2021 was 72. Raw win totals across those
years are not comparable to an 82-game season, so everything below works in
win percentage and reports it as a wins-per-82 pace. Any span touching a
shortened season is still included, because the pace conversion is what makes
it comparable, but the flag is kept so a reader can see which ones they are.

Source: ESPN public standings JSON, one request per season, cached to disk.
"""

import json
import os
import random
import urllib.request
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "nba_standings_cache.json")

FIRST_SEASON = 1991
LAST_SEASON = 2026

# Seasons that did not run a full 82 games for every team.
SHORTENED = {1999: "lockout, 50 games", 2012: "lockout, 66 games",
             2020: "covid, 64-75 games", 2021: "covid, 72 games"}

# The peer band. Detroit's own +46 is unmatched in the sample, so the nearest
# honest comparison is every team that swung 30 or more wins per 82 across two
# seasons. Set here rather than buried in the function so it is one number a
# reader can argue with.
THRESHOLD = 30.0

# Franchises whose ESPN abbreviation changed when they relocated. Joining
# seasons on the raw abbreviation silently drops any three-year span crossing a
# move, which cost the sample a qualifying leaper (Seattle 2008 to Oklahoma
# City 2010, a +30.0 swing) before this map existed. The rule is one entry per
# relocation, mapping the old code onto the surviving one.
#
# Charlotte is the awkward case and needs the season bound. ESPN reuses "CHA"
# for two different franchises: the original Hornets through 2002, who became
# New Orleans in 2003, and the expansion Bobcats who arrive in 2005 and later
# take the Hornets name back. So CHA before 2003 is the New Orleans franchise
# and CHA from 2005 on is its own thing. The empty 2003-2004 gap breaks any
# span across it on its own, which is the correct behaviour.
RELOCATED = {
    "SEA": ("OKC", None),      # Seattle -> Oklahoma City, 2008
    "VAN": ("MEM", None),      # Vancouver -> Memphis, 2001
    "NJ": ("BKN", None),       # New Jersey -> Brooklyn, 2012
    "CHA": ("NO", 2003),       # original Hornets -> New Orleans, 2003
}


def canonical(abbrev, season):
    """Franchise key that survives a relocation."""
    move = RELOCATED.get(abbrev)
    if not move:
        return abbrev
    new, before = move
    if before is not None and season >= before:
        return abbrev
    return new


def _fetch(season):
    url = ("https://site.api.espn.com/apis/v2/sports/basketball/nba/"
           "standings?season=%d" % season)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    doc = json.load(urllib.request.urlopen(req, timeout=30))
    out = {}
    for group in doc.get("children", []):
        for entry in group.get("standings", {}).get("entries", []):
            stats = {}
            for stat in entry.get("stats", []):
                if stat.get("value") is not None:
                    stats[stat["name"]] = stat["value"]
            wins, losses = stats.get("wins"), stats.get("losses")
            if wins is None or losses is None or wins + losses == 0:
                continue
            out[entry["team"]["abbreviation"]] = {
                "name": entry["team"]["displayName"],
                "wins": int(wins),
                "losses": int(losses),
            }
    return out


def load(refresh=False):
    """Season -> team abbrev -> record. Cached; ESPN is rate sensitive."""
    cache = {}
    if os.path.exists(CACHE) and not refresh:
        with open(CACHE) as handle:
            cache = json.load(handle)
    changed = False
    for season in range(FIRST_SEASON, LAST_SEASON + 1):
        key = str(season)
        if key in cache and not refresh:
            continue
        try:
            got = _fetch(season)
        except Exception as exc:  # a missing season is data, not a crash
            print("  season %d unavailable: %s" % (season, exc))
            got = {}
        if got:
            cache[key] = got
            changed = True
    if changed:
        with open(CACHE, "w") as handle:
            json.dump(cache, handle)
    return {int(k): v for k, v in cache.items() if v}


def median(values):
    """Median of an already-sorted sequence."""
    n = len(values)
    if not n:
        return float("nan")
    if n % 2:
        return values[n // 2]
    return (values[n // 2 - 1] + values[n // 2]) / 2.0


def pace(record):
    """Wins per 82 games, so shortened seasons compare honestly."""
    total = record["wins"] + record["losses"]
    return 82.0 * record["wins"] / total


def by_franchise(data):
    """Season -> franchise key -> record, with relocations bridged."""
    return {season: {canonical(ab, season): rec for ab, rec in teams.items()}
            for season, teams in data.items()}


def spans(data):
    """Every (team, y0, y1, y2) three-season run, with the year-after if it exists."""
    data = by_franchise(data)
    out = []
    for season in sorted(data):
        if season - 2 not in data or season - 1 not in data:
            continue
        for abbrev, rec2 in data[season].items():
            rec0 = data[season - 2].get(abbrev)
            rec1 = data[season - 1].get(abbrev)
            if not rec0 or not rec1:
                continue
            after = data.get(season + 1, {}).get(abbrev)
            out.append({
                "team": abbrev,
                "name": rec2["name"],
                "end": season,
                "start_pace": pace(rec0),
                "mid_pace": pace(rec1),
                "peak_pace": pace(rec2),
                "swing": pace(rec2) - pace(rec0),
                "start_record": "%d-%d" % (rec0["wins"], rec0["losses"]),
                "peak_record": "%d-%d" % (rec2["wins"], rec2["losses"]),
                "start_wins": rec0["wins"],
                "peak_wins": rec2["wins"],
                "after_pace": pace(after) if after else None,
                "after_wins": after["wins"] if after else None,
                "after_record": ("%d-%d" % (after["wins"], after["losses"])
                                 if after else None),
                "shortened": sorted(s for s in (season - 2, season - 1, season)
                                    if s in SHORTENED),
            })
    return out


def report():
    data = load()
    print("seasons loaded: %d (%d-%d)" % (len(data), min(data), max(data)))
    all_spans = spans(data)
    print("three-season spans: %d" % len(all_spans))

    det = [s for s in all_spans if s["team"] == "DET" and s["end"] == 2026][0]
    print("\nDETROIT 2024-2026")
    print("  %.1f -> %.1f -> %.1f pace, swing %+.1f, record %s"
          % (det["start_pace"], det["mid_pace"], det["peak_pace"],
             det["swing"], det["peak_record"]))

    # Where Detroit's swing sits in the whole distribution. This is the first
    # thing to know, because if nothing comes close there are no comparables
    # and the piece has to say so rather than manufacture a peer group.
    others = [s for s in all_spans if not (s["team"] == "DET" and s["end"] == 2026)]
    bigger = [s for s in others if s["swing"] >= det["swing"]]
    print("\n  spans with a swing at least as large: %d of %d"
          % (len(bigger), len(others)))
    ranked = sorted(others, key=lambda s: -s["swing"])
    print("  ten largest two-year swings on record:")
    for s in ranked[:10]:
        after = ("%+.1f" % (s["after_pace"] - s["peak_pace"])
                 if s["after_pace"] is not None else "n/a")
        print("    %-26s %d  %4.1f -> %4.1f  %+5.1f   next year %s"
              % (s["name"], s["end"], s["start_pace"], s["peak_pace"],
                 s["swing"], after))

    # Comparables: the nearest real peer group. Detroit's own swing is
    # unmatched, so the honest move is a band that actually has members.
    threshold = THRESHOLD
    comps = [s for s in others
             if s["swing"] >= threshold and s["after_pace"] is not None]
    comps.sort(key=lambda s: -s["swing"])

    print("\nCOMPARABLES: two-year swing of at least %+.1f wins per 82,"
          " with a following season on record" % threshold)
    print("  n = %d" % len(comps))
    print("  %-26s %-6s %6s %6s %6s %7s %8s"
          % ("team", "end", "from", "to", "swing", "after", "change"))
    for s in comps:
        # Raw records alongside the pace, because the conversion does not only
        # rescue shortened seasons from looking like collapses, it also invents
        # climbs that nobody watched. San Antonio 1999 reads as a 61-win team
        # and won 37 games.
        flag = ("  [raw %d -> %d, then %d]"
                % (s["start_wins"], s["peak_wins"], s["after_wins"])
                if s["shortened"] else "")
        print("  %-26s %-6d %6.1f %6.1f %+6.1f %7.1f %+8.1f%s"
              % (s["name"], s["end"], s["start_pace"], s["peak_pace"],
                 s["swing"], s["after_pace"],
                 s["after_pace"] - s["peak_pace"], flag))

    if comps:
        changes = sorted(s["after_pace"] - s["peak_pace"] for s in comps)
        mid = changes[len(changes) // 2] if len(changes) % 2 else \
            (changes[len(changes) // 2 - 1] + changes[len(changes) // 2]) / 2.0
        held = sum(1 for c in changes if c > -5)
        print("\n  median change the following year: %+.1f wins" % mid)
        print("  mean change: %+.1f wins" % (sum(changes) / len(changes)))
        print("  range: %+.1f to %+.1f" % (changes[0], changes[-1]))
        print("  held within five wins of the peak: %d of %d" % (held, len(comps)))
        print("  declined at all: %d of %d"
              % (sum(1 for c in changes if c < 0), len(comps)))

    # Baseline: what does EVERY team do the year after any season, as a
    # function of how good that season was? A 60-win team regressing is not
    # news unless it regresses more than 60-win teams usually do.
    sixty = [s for s in all_spans
             if s["peak_pace"] >= 58 and s["after_pace"] is not None]
    if sixty:
        ch = sorted(s["after_pace"] - s["peak_pace"] for s in sixty)
        print("\nBASELINE: every 58-win-pace-or-better season, n = %d" % len(sixty))
        print("  median change the following year: %+.1f wins" % median(ch))
        print("  declined at all: %d of %d" % (sum(1 for c in ch if c < 0), len(ch)))

    # The control that makes the comparison fair. The leapers above peak at a
    # median well under 58, and a 47-win team regresses less than a 62-win team
    # for reasons that have nothing to do with how it got there. So match each
    # leaper against every non-leaping season within three wins of its own peak
    # and ask whether the leaper beat that matched group.
    pool = [s for s in all_spans if s["after_pace"] is not None]
    nonleap = [s for s in pool if s["swing"] < THRESHOLD]
    print("\nMATCHED CONTROL: each leaper against non-leapers at the same peak")
    print("  leaper peaks: median %.1f wins per 82"
          % median(sorted(s["peak_pace"] for s in comps)))
    print("  %-26s %-6s %6s %8s %8s %8s"
          % ("team", "end", "peak", "actual", "matched", "diff"))
    diffs = []
    for s in comps:
        near = [t["after_pace"] - t["peak_pace"] for t in nonleap
                if abs(t["peak_pace"] - s["peak_pace"]) <= 3.0]
        if len(near) < 10:
            continue
        expected = median(sorted(near))
        actual = s["after_pace"] - s["peak_pace"]
        diffs.append(actual - expected)
        print("  %-26s %-6d %6.1f %+8.1f %+8.1f %+8.1f"
              % (s["name"], s["end"], s["peak_pace"], actual, expected,
                 actual - expected))
    if diffs:
        print("\n  leapers beat their matched control by a median of %+.1f wins"
              % median(sorted(diffs)))
        print("  mean %+.1f wins" % (sum(diffs) / len(diffs)))
        up = sum(1 for d in diffs if d > 0)
        print("  beat the control: %d of %d" % (up, len(diffs)))

        # Is that anything? With fourteen cases, it had better be tested
        # rather than eyeballed, because fourteen of anything can look like a
        # pattern. Sign test on the count, bootstrap on the size.
        n = len(diffs)
        tail = sum(comb(n, k) for k in range(up, n + 1)) / float(2 ** n)
        print("  sign test: %d or more positive by chance alone, p = %.2f"
              % (up, tail))
        rng = random.Random(7)
        boot = sorted(median(sorted(rng.choice(diffs) for _ in range(n)))
                      for _ in range(20000))
        lo, hi = boot[int(.025 * 20000)], boot[int(.975 * 20000)]
        print("  bootstrap 95%% interval on the median: %+.1f to %+.1f" % (lo, hi))
        print("  interval contains zero: %s" % (lo <= 0 <= hi))

    # Sensitivity: does the answer depend on the pace conversion at all? Throw
    # out every span that touches a shortened season and re-run. If the answer
    # moves, the conversion is doing the work and the finding is an artifact.
    clean = [s for s in comps if not s["shortened"]]
    clean_diffs = []
    for s in clean:
        near = [t["after_pace"] - t["peak_pace"] for t in nonleap
                if abs(t["peak_pace"] - s["peak_pace"]) <= 3.0]
        if len(near) >= 10:
            clean_diffs.append((s["after_pace"] - s["peak_pace"])
                               - median(sorted(near)))
    if clean_diffs:
        print("\n  SENSITIVITY, dropping every span touching a shortened season")
        print("    n = %d, median %+.1f, positive %d of %d"
              % (len(clean_diffs), median(sorted(clean_diffs)),
                 sum(1 for d in clean_diffs if d > 0), len(clean_diffs)))

    # And the number that actually applies to Detroit: what a 60-win-pace team
    # does next, leaper or not.
    at_det = [s["after_pace"] - s["peak_pace"] for s in pool
              if abs(s["peak_pace"] - det["peak_pace"]) <= 3.0]
    print("\nTEAMS AT DETROIT'S LEVEL: peak within three wins of %.0f, n = %d"
          % (det["peak_pace"], len(at_det)))
    print("  median change the following year: %+.1f wins" % median(sorted(at_det)))
    print("  declined at all: %d of %d"
          % (sum(1 for c in at_det if c < 0), len(at_det)))
    print("  fell below 50: %d of %d"
          % (sum(1 for s in pool
                 if abs(s["peak_pace"] - det["peak_pace"]) <= 3.0
                 and s["after_pace"] < 50), len(at_det)))

    return det, comps, sixty, diffs


if __name__ == "__main__":
    report()
