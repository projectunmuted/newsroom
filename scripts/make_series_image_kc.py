"""Render the Royals-Tigers series preview tables as one PNG for Reddit.

Numbers from one run of `python scripts/tightest_matchup.py` and one run of
`python scripts/series_preview.py --opp KC`, both 2026-08-20, plus the MLB Stats
API standings and team pitching pulls the same morning. Re-run those and paste
into the DATA blocks if this is ever refreshed.

    python scripts/make_series_image_kc.py

Writes drafts/2026-08-21-royals-tigers-series.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import make_table_image as mti

# --- DATA (MLB Stats API, 2026-08-20) --------------------------------------

T1_TITLE = "Every meeting this season"
T1_COLS = ["Date", "Where", "Result", "Margin"]
T1_ALIGN = ["left", "left", "left", "right"]
T1_ROWS = [
    ["Apr 14", "Comerica", "Detroit 2, Kansas City 1", "1"],
    ["Apr 15", "Comerica", "Detroit 2, Kansas City 1", "1"],
    ["Apr 16", "Comerica", "Detroit 10, Kansas City 9", "1"],
    ["May 8", "Kauffman", "Kansas City 4, Detroit 3", "1"],
    ["May 9", "Kauffman", "Kansas City 5, Detroit 1", "4"],
    ["May 10", "Kauffman", "Detroit 6, Kansas City 3", "3"],
    ["Jul 23", "Comerica", "Detroit 4, Kansas City 3", "1"],
    ["Jul 24", "Comerica", "Detroit 2, Kansas City 1", "1"],
    ["Jul 25", "Comerica", "Kansas City 3, Detroit 2", "1"],
    ["Jul 26", "Comerica", "Kansas City 5, Detroit 4", "1"],
    ["Total", "", "Detroit 36-35, and won 6 of 10", "8 by 1"],
]

T2_TITLE = "The tightest matchups in baseball"
T2_COLS = ["Matchup (top 5 are this season)", "Decided by 1 run"]
T2_ALIGN = ["left", "right"]
T2_ROWS = [
    ["Tigers / Royals", "8 of 10"],
    ["White Sox / Guardians", "6 of 10"],
    ["D-backs / Dodgers", "6 of 13"],
    ["Royals / Twins", "6 of 13"],
    ["Brewers / Twins", "5 of 6"],
    ["Tightest in all of 2025", "7 of 14"],
    ["Tightest in all of 2024", "7 of 13"],
    ["Tightest in all of 2023", "7 of 13"],
]

T3_TITLE = "How the two teams compare"
T3_COLS = ["", "Tigers", "Royals"]
T3_ALIGN = ["left", "right", "right"]
T3_ROWS = [
    ["Record", "61-66", "54-74"],
    ["Run differential", "+82", "-104"],
    ["Team ERA", "3.57 (4th)", "4.79 (28th)"],
    ["Saves / chances", "26 of 54", "31 of 54"],
    ["Blown saves", "28", "23"],
    ["1-run games", "12-22", "18-22"],
    ["At home", "32-31", "32-30"],
    ["On the road", "29-35", "22-44"],
]

FOOTER = ("MLB Stats API, 2026-08-20. All 1,909 completed games this season for "
          "the matchup counts. Opener 8:10pm ET Friday at Kauffman.")


def main():
    total_h = (mti.PAD_TOP + mti.block_height(T1_ROWS) + mti.GAP
               + mti.block_height(T2_ROWS) + mti.GAP
               + mti.block_height(T3_ROWS) + mti.PAD_BOTTOM)
    fig = plt.figure(figsize=(mti.FIG_W, total_h), dpi=200, facecolor=mti.SURFACE)

    y = mti.PAD_TOP
    y = mti.draw_block(fig, y, T1_TITLE, T1_COLS, T1_ALIGN, T1_ROWS,
                       weights=[0.9, 1.1, 2.4, 0.8], span_frac=0.95,
                       hilite={"Total"})
    y += mti.GAP
    y = mti.draw_block(fig, y, T2_TITLE, T2_COLS, T2_ALIGN, T2_ROWS,
                       weights=[2.2, 1.2], span_frac=0.78,
                       hilite={"Tigers / Royals"})
    y += mti.GAP
    y = mti.draw_block(fig, y, T3_TITLE, T3_COLS, T3_ALIGN, T3_ROWS,
                       weights=[1.9, 1.0, 1.0], span_frac=0.76,
                       hilite={"Saves / chances"})

    fig.text(mti.SIDE / mti.FIG_W, 1.0 - (y + 0.26) / total_h, FOOTER,
             fontsize=mti.FS_FOOT, color=mti.MUTED, ha="left", va="baseline")

    out = os.path.join(os.path.dirname(__file__), "..", "drafts",
                       "2026-08-21-royals-tigers-series.png")
    fig.savefig(out, dpi=200, facecolor=mti.SURFACE)
    print("wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
