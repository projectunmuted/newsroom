"""Render the record-vs-run-differential tables as one PNG for Reddit.

Unlike the earlier make_series_image_*.py scripts, **this one pulls live and
hardcodes nothing.** That is deliberate. On 2026-08-21 a finished Reddit draft
was found carrying an ERA that had moved on its own while the draft sat in the
approval queue, because its numbers were frozen in a DATA block. A draft whose
image is regenerated from the API every time it is rendered cannot go quietly
stale; re-running the command is the diff.

    python scripts/make_pythag_image.py

Writes drafts/2026-08-24-pythag-extremes.png and prints every number it drew,
so the prose in the draft can be checked against the same pull.

Pythagorean exponent 1.83, Baseball Reference's standard for MLB.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import urllib.request

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_table_image as mti

EXP = 1.83
STANDINGS = ("https://statsapi.mlb.com/api/v1/standings"
             "?leagueId=103,104&season=2026&standingsTypes=regularSeason")
TEAM_STATS = ("https://statsapi.mlb.com/api/v1/teams/{tid}/stats"
              "?stats=season&group=pitching&season=2026&gameType=R")
SCHEDULE = ("https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={tid}"
            "&startDate=2026-03-01&endDate={end}&gameType=R")

# The 2 clubs the draft is about. Kept as ids so a later cycle can point this
# at a different pair without touching anything else.
PAIR = [(139, "Rays"), (116, "Tigers")]


def get(url: str):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def league() -> list[dict]:
    """Every team, with wins above or below its Pythagorean expectation."""
    teams = []
    for record in get(STANDINGS)["records"]:
        for t in record["teamRecords"]:
            rs, ra = t.get("runsScored"), t.get("runsAllowed")
            if not rs or not ra:
                continue
            w, l = t["wins"], t["losses"]
            exp = (rs ** EXP) / ((rs ** EXP) + (ra ** EXP)) * (w + l)
            teams.append({"name": t["team"]["name"], "w": w, "l": l,
                          "rs": rs, "ra": ra, "exp": exp, "gap": w - exp})
    return sorted(teams, key=lambda t: -t["gap"])


def margins(tid: int, end: str) -> dict[str, list[int]]:
    """Record split by margin of victory.

    'Completed Early' counts. A shortened game is a real result in the
    standings, and leaving it out once put this club's win total 1 short of
    what the standings said.
    """
    out = {"1 run": [0, 0], "2 to 4 runs": [0, 0], "5 or more": [0, 0]}
    for date in get(SCHEDULE.format(tid=tid, end=end))["dates"]:
        for g in date["games"]:
            if g["status"]["detailedState"] not in ("Final", "Completed Early"):
                continue
            a, h = g["teams"]["away"], g["teams"]["home"]
            us, them = (a, h) if a["team"]["id"] == tid else (h, a)
            if "score" not in us or "score" not in them:
                continue
            d = us["score"] - them["score"]
            k = ("1 run" if abs(d) == 1
                 else "2 to 4 runs" if abs(d) <= 4 else "5 or more")
            out[k][0 if d > 0 else 1] += 1
    return out


def bullpen(tid: int) -> dict:
    s = get(TEAM_STATS.format(tid=tid))["stats"][0]["splits"][0]["stat"]
    return {"era": s["era"], "sv": s["saves"], "svo": s["saveOpportunities"],
            "bs": s["blownSaves"], "holds": s["holds"]}


def main() -> None:
    today = dt.date.today().isoformat()
    lg = league()
    by_name = {t["name"]: t for t in lg}
    pair = [by_name[name] for _, name in PAIR]

    # Table 1: the extremes, with the 2 clubs in the draft at either end.
    ends = lg[:3] + lg[-3:]
    names = {t["name"] for t in ends}
    for t in pair:
        if t["name"] not in names:
            ends.append(t)
    ends = sorted({t["name"]: t for t in ends}.values(), key=lambda t: -t["gap"])
    t1_rows = [[t["name"], f'{t["w"]}-{t["l"]}', str(t["rs"]), str(t["ra"]),
                f'{t["exp"]:.1f}', f'{t["gap"]:+.1f}'] for t in ends]

    # Table 2: margin buckets, one column per club.
    marg = {name: margins(tid, today) for tid, name in PAIR}
    t2_rows = [[k] + [f'{marg[name][k][0]}-{marg[name][k][1]}'
                      for _, name in PAIR]
               for k in ("1 run", "2 to 4 runs", "5 or more")]

    # Table 3: the mechanism.
    pen = {name: bullpen(tid) for tid, name in PAIR}
    t3_rows = [
        ["Record"] + [f'{by_name[n]["w"]}-{by_name[n]["l"]}' for _, n in PAIR],
        ["Runs scored"] + [str(by_name[n]["rs"]) for _, n in PAIR],
        ["Runs allowed"] + [str(by_name[n]["ra"]) for _, n in PAIR],
        ["Team ERA"] + [pen[n]["era"] for _, n in PAIR],
        ["Saves / chances"] + [f'{pen[n]["sv"]} of {pen[n]["svo"]}'
                               for _, n in PAIR],
        ["Blown saves"] + [str(pen[n]["bs"]) for _, n in PAIR],
        ["Holds"] + [str(pen[n]["holds"]) for _, n in PAIR],
    ]

    t1_cols = ["Team", "W-L", "RS", "RA", "Expected W", "Gap"]
    t2_cols = ["Games decided by"] + [n for _, n in PAIR]
    t3_cols = [""] + [n for _, n in PAIR]
    hilite = {n for _, n in PAIR} | {"Saves / chances"}

    footer = (f"MLB Stats API, {today}. Expected wins use the Pythagorean "
              f"exponent 1.83. Regenerate with scripts/make_pythag_image.py.")

    total_h = (mti.PAD_TOP + mti.block_height(t1_rows) + mti.GAP
               + mti.block_height(t2_rows) + mti.GAP
               + mti.block_height(t3_rows) + mti.PAD_BOTTOM)
    fig = plt.figure(figsize=(mti.FIG_W, total_h), dpi=200,
                     facecolor=mti.SURFACE)

    y = mti.PAD_TOP
    y = mti.draw_block(fig, y, "Wins above or below run differential, the extremes",
                       t1_cols, ["left", "right", "right", "right", "right", "right"],
                       t1_rows, weights=[1.6, 1.0, 0.8, 0.8, 1.2, 0.9],
                       span_frac=0.95, hilite=hilite)
    y += mti.GAP
    y = mti.draw_block(fig, y, "Record by margin", t2_cols,
                       ["left", "right", "right"], t2_rows,
                       weights=[1.8, 1.0, 1.0], span_frac=0.70, hilite=hilite)
    y += mti.GAP
    y = mti.draw_block(fig, y, "Same runs scored, different seasons", t3_cols,
                       ["left", "right", "right"], t3_rows,
                       weights=[1.8, 1.0, 1.0], span_frac=0.70, hilite=hilite)

    fig.text(mti.SIDE / mti.FIG_W, 1.0 - (y + 0.26) / total_h, footer,
             fontsize=mti.FS_FOOT, color=mti.MUTED, ha="left", va="baseline")

    out = os.path.join(os.path.dirname(__file__), "..", "drafts",
                       "2026-08-24-pythag-extremes.png")
    fig.savefig(out, dpi=200, facecolor=mti.SURFACE)
    print("wrote", os.path.normpath(out))

    # Print everything drawn, so the prose can be checked against this pull.
    print(f"\npulled {today}")
    for row in t1_rows:
        print("  ", row)
    print()
    for row in t2_rows:
        print("  ", row)
    print()
    for row in t3_rows:
        print("  ", row)


if __name__ == "__main__":
    main()
