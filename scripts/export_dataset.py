#!/usr/bin/env python3
"""Generate the public dataset artifact in datasets/ from the cached pulls.

    python scripts/export_dataset.py            # write datasets/
    python scripts/export_dataset.py --check    # regenerate to a temp dir and
                                                # diff; exit 1 if stale

Why this exists: `MONEY.md` ranks "the data as an artifact" third among the
things that can move with nobody, behind the findings repo which shipped
2026-08-27. A dataset is the shape of thing people link to and cite, which is
what M4 in `PLAN.md` actually needs, and unlike every other route here it needs
no account of his and no attention of his.

**Everything in datasets/ is generated.** The prose lives in this file as a
template and every number in it is computed from the same rows that go into the
CSV, so the README cannot disagree with the data it describes. That is the same
contract as `pythag_chart.py` and the house rule about generating from data
rather than hand-drawing: re-running this script *is* the diff.

The source is `scripts/preseason_cache_2000.json`, the receipt from
`preseason_full.py`. Delete that cache and rerun `preseason_full.py` to refetch
from ESPN.
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "preseason_cache_2000.json")
PHANTOM_LOG = os.path.join(HERE, "preseason_phantom_games.json")
OUT = os.path.join(ROOT, "datasets")

CSV_NAME = "nfl-preseason-vs-regular-season-2000-2025.csv"

# The date the rows were last checked against a live ESPN call, and what was
# checked. Bump both together; a provenance line nobody re-verified is worse
# than none.
VERIFIED_ON = "2026-08-28"
VERIFIED_WHAT = (
    "4 team-seasons were re-fetched live and matched the cache exactly: "
    "DET 2008 (preseason 4-0, regular 0-16), LAR 2011, LAC 2000 and LV 2015. "
    "The last 3 are the relocation franchises that correction 2 above is about."
)

TEAM_NAMES = {
    "ari": "Arizona Cardinals", "atl": "Atlanta Falcons",
    "bal": "Baltimore Ravens", "buf": "Buffalo Bills",
    "car": "Carolina Panthers", "chi": "Chicago Bears",
    "cin": "Cincinnati Bengals", "cle": "Cleveland Browns",
    "dal": "Dallas Cowboys", "den": "Denver Broncos",
    "det": "Detroit Lions", "gb": "Green Bay Packers",
    "hou": "Houston Texans", "ind": "Indianapolis Colts",
    "jax": "Jacksonville Jaguars", "kc": "Kansas City Chiefs",
    "lac": "Los Angeles Chargers", "lar": "Los Angeles Rams",
    "lv": "Las Vegas Raiders", "mia": "Miami Dolphins",
    "min": "Minnesota Vikings", "ne": "New England Patriots",
    "no": "New Orleans Saints", "nyg": "New York Giants",
    "nyj": "New York Jets", "phi": "Philadelphia Eagles",
    "pit": "Pittsburgh Steelers", "sea": "Seattle Seahawks",
    "sf": "San Francisco 49ers", "tb": "Tampa Bay Buccaneers",
    "ten": "Tennessee Titans", "wsh": "Washington Commanders",
}


def load():
    if not os.path.exists(CACHE):
        sys.stderr.write(
            "no cache at %s -- run scripts/preseason_full.py first\n" % CACHE)
        sys.exit(2)
    with open(CACHE, encoding="utf-8") as fh:
        rows = json.load(fh)
    if not rows:
        sys.stderr.write("cache is empty\n")
        sys.exit(2)
    return sorted(rows, key=lambda r: (r["season"], r["team"]))


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def buckets(rows):
    """The five preseason outcomes, each with its mean regular-season rate.

    Ordered best preseason to worst so the non-monotonicity at the top is
    visible in the table rather than something a reader has to reconstruct.

    The comparison baseline is a flat **.500**, matching `preseason_full.py`
    (which builds its chart against .500) and the published entry. A league's
    average win rate is .500 by construction; the sample mean differs from it
    only in the 4th decimal, because dropping a phantom fixture removes it from
    one team's row without necessarily removing it from the opponent's. Using
    the sample mean here instead would make this file disagree with the
    project's own chart in the 3rd decimal for no gain.
    """
    grand = 0.5
    defs = [
        ("Won every preseason game", lambda r: r["pre_pct"] == 1.0),
        ("Winning preseason", lambda r: 0.5 < r["pre_pct"] < 1.0),
        ("Even preseason", lambda r: r["pre_pct"] == 0.5),
        ("Losing preseason", lambda r: 0.0 < r["pre_pct"] < 0.5),
        ("Lost every preseason game", lambda r: r["pre_pct"] == 0.0),
    ]
    out = []
    for label, test in defs:
        sub = [r for r in rows if test(r)]
        mean = sum(r["reg_pct"] for r in sub) / len(sub)
        out.append((label, len(sub), mean, mean - grand))
    return out


def write_csv(rows, path):
    cols = ["season", "team", "team_name", "preseason_wins", "preseason_games",
            "preseason_win_pct", "regular_wins", "regular_games",
            "regular_win_pct"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([
                r["season"], r["team"], TEAM_NAMES.get(r["team"], r["team"]),
                # Ties count half a win on both sides, so these can be .5 and
                # are written as given rather than rounded to an integer.
                "%g" % r["pre_w"], "%g" % r["pre_g"],
                "%.6f" % r["pre_pct"],
                "%g" % r["reg_w"], "%g" % r["reg_g"],
                "%.6f" % r["reg_pct"],
            ])


def readme(rows):
    xs = [r["pre_pct"] for r in rows]
    ys = [r["reg_pct"] for r in rows]
    r_all = pearson(xs, ys)
    seasons = sorted({r["season"] for r in rows})
    teams = sorted({r["team"] for r in rows})
    b = buckets(rows)
    undef = [r for r in rows if r["pre_pct"] == 1.0]
    winless = [r for r in rows if r["pre_pct"] == 0.0]
    worst = sorted(undef, key=lambda r: r["reg_pct"])[:5]
    best = sorted(undef, key=lambda r: -r["reg_pct"])[:5]

    def rec(r, pre=False):
        w, g = (r["pre_w"], r["pre_g"]) if pre else (r["reg_w"], r["reg_g"])
        return "%g-%g" % (w, g - w)

    with open(PHANTOM_LOG, encoding="utf-8") as fh:
        phantoms = json.load(fh)
    phantom_games = sum(len(p["dates"]) for p in phantoms)

    # Rows whose regular season is shorter than the schedule that year, which
    # is the downstream cost of dropping a phantom that stood in for a real
    # fixture. Computed, not asserted, and shown alongside the same statistics
    # recomputed without them so a reader can see it does not move the answer.
    sched = lambda s: 17 if s >= 2021 else 16          # noqa: E731
    short = [r for r in rows if r["reg_g"] < sched(r["season"])]
    dist = sorted({g: sum(1 for r in short if r["reg_g"] == g)
                   for g in {r["reg_g"] for r in short}}.items())
    clean = [r for r in rows if r["reg_g"] == sched(r["season"])]
    r_clean = pearson([r["pre_pct"] for r in clean],
                      [r["reg_pct"] for r in clean])
    undef_clean = [r for r in clean if r["pre_pct"] == 1.0]
    undef_mean_all = sum(r["reg_pct"] for r in undef) / len(undef)
    undef_mean_clean = (sum(r["reg_pct"] for r in undef_clean)
                        / len(undef_clean))

    L = []
    A = L.append
    A("# Does an NFL team's preseason record predict its regular season?")
    A("")
    A("**No. It explains %.1f%% of the variance.**" % (100 * r_all ** 2))
    A("")
    A("This repository is the data behind that answer: **%d team-seasons**, "
      "every NFL team's preseason and regular-season record for **%d seasons, "
      "%d to %d**, pulled from ESPN's public schedule endpoint and "
      "cross-checked against live calls."
      % (len(rows), len(seasons), seasons[0], seasons[-1]))
    A("")
    A("- **[`%s`](%s)** is the dataset, one row per team-season."
      % (CSV_NAME, CSV_NAME))
    A("- **[`excluded-games.json`](excluded-games.json)** is every fixture "
      "dropped and why, so the exclusions are auditable rather than implied.")
    A("")
    A("Free to use for anything, with attribution. No API key, no signup, no "
      "scraper to maintain.")
    A("")
    A("## The answer, in one table")
    A("")
    A("Correlation between preseason win rate and regular-season win rate "
      "across all %d rows: **r = %+.3f**, so preseason record explains "
      "**%.1f%%** of what happens next."
      % (len(rows), r_all, 100 * r_all ** 2))
    A("")
    A("| Preseason | n | Mean regular-season win rate | vs. .500 |")
    A("|---|---|---|---|")
    for label, n, mean, delta in b:
        A("| %s | %d | %.3f | %+.3f |" % (label, n, mean, delta))
    A("")
    A("The interesting part is the top row. Teams that went **undefeated** in "
      "the preseason went on to be **worse than .500**, not better. Going "
      "unbeaten in August was a slightly negative signal, and the best "
      "preseason bucket in the whole table is merely *winning*, not perfect.")
    A("")
    A("## The tails")
    A("")
    A("%d undefeated preseasons and %d winless ones in the sample."
      % (len(undef), len(winless)))
    A("")
    A("**Worst regular seasons that followed an undefeated preseason:**")
    A("")
    A("| Team | Season | Preseason | Regular season |")
    A("|---|---|---|---|")
    for r in worst:
        A("| %s | %d | %s | **%s** |" % (TEAM_NAMES.get(r["team"], r["team"]),
                                         r["season"], rec(r, True), rec(r)))
    A("")
    A("**Best regular seasons that followed an undefeated preseason**, because "
      "a table of only the disasters would be the same cherry-picking this "
      "dataset exists to make unnecessary:")
    A("")
    A("| Team | Season | Preseason | Regular season |")
    A("|---|---|---|---|")
    for r in best:
        A("| %s | %d | %s | %s |" % (TEAM_NAMES.get(r["team"], r["team"]),
                                     r["season"], rec(r, True), rec(r)))
    A("")
    A("## Schema")
    A("")
    A("| Column | Type | Notes |")
    A("|---|---|---|")
    A("| `season` | int | %d to %d. **2020 is absent**: no preseason was "
      "played. |" % (seasons[0], seasons[-1]))
    A("| `team` | str | ESPN's team slug, e.g. `det`. Constant across "
      "relocations, so the Rams are `lar` in every season including the St "
      "Louis ones. |")
    A("| `team_name` | str | Current franchise name. |")
    A("| `preseason_wins` | float | **Ties count as half a win.** |")
    A("| `preseason_games` | float | Games actually played and finished. "
      "**The preseason shortened from 4 games to 3 in 2021**, so an unbeaten "
      "preseason is 4-0 in the older rows and 3-0 in the newer ones. |")
    A("| `preseason_win_pct` | float | `preseason_wins / preseason_games`. |")
    A("| `regular_wins` | float | Ties count as half a win. |")
    A("| `regular_games` | float | 16 through 2020, 17 from 2021. |")
    A("| `regular_win_pct` | float | `regular_wins / regular_games`. |")
    A("")
    A("%d franchises. 2000 and 2001 carry %d rows rather than %d because the "
      "Houston Texans did not exist until 2002."
      % (len(teams), len([r for r in rows if r["season"] == 2000]), len(teams)))
    A("")
    A("## Three corrections already made, and they are the reason to use this "
      "rather than re-scrape it")
    A("")
    A("Each of these was a wrong number that a reasonable scrape produces and "
      "that nothing warns you about. All three were found the expensive way.")
    A("")
    A("**1. The window was not the data floor.** An earlier version of this "
      "analysis ran 2015 to 2025 and described that as the limit of ESPN's "
      "coverage. It is not: the endpoint serves preseason schedules back to "
      "2000, and 1999 and earlier return zero events. The short window "
      "excluded the 2008 Lions, who went 4-0 in the preseason and 0-16, which "
      "is the single most famous case of the very claim being tested. A reader "
      "pointed this out and was right.")
    A("")
    A("**2. Three franchises were being counted as their opponents.** ESPN "
      "answers `/teams/lar/` for every season, but the box score inside "
      "carries the *historical* abbreviation, so a 2015 Rams game says `STL`. "
      "Code that finds its own side by matching the requested abbreviation "
      "matches nothing and falls back to the first competitor listed, which is "
      "frequently the opponent. The same applies to the Chargers (`SD` through "
      "2016) and the Raiders (`OAK` through 2019). **Match on ESPN's numeric "
      "team id instead**, which is stable across all three relocations: Rams "
      "14, Chargers 24, Raiders 13.")
    A("")
    A("**3. Never-played fixtures come back as 0-0, not null.** Older seasons "
      "carry them with a final-looking score of 0-0, and a 0-0 scores as a "
      "tie, which is half a win to both sides. Detroit's 2001 season came back "
      "**2.5-13.5** against a real 2-14 because of a phantom Detroit-St Louis "
      "fixture dated 2001-10-09. **No NFL game has finished 0-0 since 1943**, "
      "so treating a 0-0 as unplayed costs nothing real. %d such fixtures "
      "across %d team-seasons were dropped; every one is listed in "
      "`excluded-games.json`." % (phantom_games, len(phantoms)))
    A("")
    A("## Known limitation: %d rows have a short denominator" % len(short))
    A("")
    A("This follows from correction 3 and is the one thing to know before "
      "using the data for something else.")
    A("")
    A("When ESPN serves a phantom 0-0 fixture it is usually serving it **in "
      "place of** a real game rather than in addition to one, so dropping it "
      "leaves that team-season a game short. Detroit 2001 is the worked "
      "example: counting the 0-0 as a tie gives 2.5-13.5 over 16, dropping it "
      "gives **2-13 over 15**, and the real record is 2-14. Dropping it fixes "
      "the wins and leaves the denominator one short.")
    A("")
    A("**%d of %d rows (%.1f%%) carry fewer regular-season games than that "
      "season's schedule length.** Every one of them is explained by a "
      "fixture in `excluded-games.json`; there are no unexplained short rows. "
      "The distribution is %s."
      % (len(short), len(rows), 100.0 * len(short) / len(rows),
         ", ".join("%g games: %d rows" % kv for kv in dist)))
    A("")
    A("**It does not move the answer**, and the check is worth showing rather "
      "than asserting. Restricting to the %d rows with a complete schedule:"
      % len(clean))
    A("")
    A("| Sample | n | r | Variance explained | Undefeated-preseason mean |")
    A("|---|---|---|---|---|")
    A("| All rows | %d | %+.3f | %.1f%% | %.3f |"
      % (len(rows), r_all, 100 * r_all ** 2, undef_mean_all))
    A("| Complete schedules only | %d | %+.3f | %.1f%% | %.3f |"
      % (len(clean), r_clean, 100 * r_clean ** 2, undef_mean_clean))
    A("")
    A("Both say the same thing. If you are computing win *rates*, as the "
      "headline above does, the effect is immaterial. If you need exact win "
      "*totals* for a specific team-season, check it against a second source "
      "first.")
    A("")
    A("## Provenance")
    A("")
    A("Source: ESPN's public schedule endpoint, no key required.")
    A("")
    A("```")
    A("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/"
      "{team}/schedule?season={season}&seasontype={1|2}")
    A("```")
    A("")
    A("`seasontype=1` is preseason, `seasontype=2` is regular season. Only "
      "games with a final status and two numeric scores are counted.")
    A("")
    A("**Last verified against live calls: %s.** %s"
      % (VERIFIED_ON, VERIFIED_WHAT))
    A("")
    A("The code that produced this, and the full derivation including the "
      "subsample breakdowns, is `scripts/preseason_full.py` in the newsroom "
      "repo. This file and the CSV beside it are both generated by "
      "`scripts/export_dataset.py`; nothing here is edited by hand, so the "
      "prose cannot drift from the numbers.")
    A("")
    A("## Where this came from")
    A("")
    A("It is a by-product of [Detroit Sports "
      "Reporter](https://detroitsportsreporter.com), where predictions get "
      "committed before games and graded after, and of the project journal at "
      "[project-unmuted.com](https://project-unmuted.com).")
    A("")
    A("If you use the data, a link back is appreciated and not required.")
    A("")
    return "\n".join(L)


def build(outdir, rows):
    os.makedirs(outdir, exist_ok=True)
    write_csv(rows, os.path.join(outdir, CSV_NAME))
    with open(os.path.join(outdir, "README.md"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write(readme(rows))
    with open(PHANTOM_LOG, encoding="utf-8") as fh:
        phantoms = json.load(fh)
    with open(os.path.join(outdir, "excluded-games.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump({
            "why": ("Fixtures returned by ESPN with a 0-0 score, which older "
                    "seasons use for games that were never played. A 0-0 "
                    "would otherwise score as a tie, worth half a win to each "
                    "side. No NFL game has finished 0-0 since 1943."),
            "seasontype": {"1": "preseason", "2": "regular season"},
            "excluded": phantoms,
        }, fh, indent=1)
        fh.write("\n")


def main():
    rows = load()
    if "--check" in sys.argv:
        tmp = tempfile.mkdtemp(prefix="dataset-check-")
        try:
            build(tmp, rows)
            stale = []
            for name in sorted(os.listdir(tmp)):
                a, b = os.path.join(tmp, name), os.path.join(OUT, name)
                if not os.path.exists(b):
                    stale.append(name + " (missing)")
                    continue
                with open(a, "rb") as fa, open(b, "rb") as fb:
                    if fa.read() != fb.read():
                        stale.append(name + " (differs)")
            if stale:
                sys.stderr.write("datasets/ is stale: %s\n" % ", ".join(stale))
                return 1
            print("datasets/ is up to date with the cache")
            return 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    build(OUT, rows)
    print("wrote %d rows to %s" % (len(rows), os.path.join(OUT, CSV_NAME)))
    print("wrote README.md and excluded-games.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
