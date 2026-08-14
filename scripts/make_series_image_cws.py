"""Render the White Sox-Tigers series preview tables as one PNG.

Every number here came out of one run of `python scripts/series_preview.py
--opp CWS` on 2026-08-14. Nothing is read off a box score by eye. Re-run that
script and paste into the DATA blocks if this is ever refreshed.

Drawing code is imported from make_table_image, not forked.

    python scripts/make_series_image_cws.py

Writes drafts/2026-08-14-whitesox-tigers-series.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import make_table_image as mti

# --- DATA (series_preview.py --opp CWS, 2026-08-14) ------------------------

T1_TITLE = "Every meeting this season"
T1_COLS = ["Date", "Result", "Where"]
T1_ALIGN = ["left", "left", "right"]
T1_ROWS = [
    ["May 29", "Chicago 4, Detroit 3", "Chicago"],
    ["May 30", "Chicago 7, Detroit 1", "Chicago"],
    ["May 31", "Chicago 2, Detroit 1", "Chicago"],
    ["Jun 19", "Detroit 4, Chicago 3", "Detroit"],
    ["Jun 20", "Detroit 4, Chicago 1", "Detroit"],
    ["Jun 21", "Detroit 5, Chicago 4", "Detroit"],
    ["Total", "Chicago 21, Detroit 18", "3-3"],
]

T2_TITLE = "How the two teams compare"
T2_COLS = ["", "Tigers", "White Sox"]
T2_ALIGN = ["left", "right", "right"]
T2_ROWS = [
    ["Record", "60-61", "62-58"],
    ["Last 14 days", "9-3", "5-7"],
    ["Season series", "3-3", "3-3"],
    ["Runs in those 6", "18", "21"],
    ["Runs per game", "3.0", "3.5"],
    ["In this series at home", "3-0", "3-0"],
]

T3_TITLE = "Probables at Comerica"
T3_COLS = ["Game", "White Sox", "Tigers"]
T3_ALIGN = ["left", "left", "left"]
T3_ROWS = [
    ["Fri 6:40", "Newcomb 2.66 / 1.13 (1 GS)", "Jobe 0.00 / 0.40 (1 GS)"],
    ["Sat", "Kay 3.96 / 1.34 (22 GS)", "not announced"],
    ["Sun", "Burke 2.99 / 1.08 (20 GS)", "Anderson 3.91 / 1.30 (4 GS)"],
]

FOOTER = ("MLB Stats API via series_preview.py, 2026-08-14. Pitcher line is "
          "season ERA / WHIP with games started. Opener 6:40pm ET at Comerica.")


def main():
    total_h = (mti.PAD_TOP + mti.block_height(T1_ROWS) + mti.GAP
               + mti.block_height(T2_ROWS) + mti.GAP
               + mti.block_height(T3_ROWS) + mti.PAD_BOTTOM)
    fig = plt.figure(figsize=(mti.FIG_W, total_h), dpi=200, facecolor=mti.SURFACE)

    y = mti.PAD_TOP
    y = mti.draw_block(fig, y, T1_TITLE, T1_COLS, T1_ALIGN, T1_ROWS,
                       weights=[1.0, 2.2, 1.0], span_frac=0.82,
                       hilite={"Total"})
    y += mti.GAP
    y = mti.draw_block(fig, y, T2_TITLE, T2_COLS, T2_ALIGN, T2_ROWS,
                       weights=[1.9, 1.0, 1.0], span_frac=0.72,
                       hilite={"In this series at home"})
    y += mti.GAP
    y = mti.draw_block(fig, y, T3_TITLE, T3_COLS, T3_ALIGN, T3_ROWS,
                       weights=[0.9, 2.3, 2.3], span_frac=1.0,
                       hilite={"Fri 6:40"})

    fig.text(mti.SIDE / mti.FIG_W, 1.0 - (y + 0.26) / total_h, FOOTER,
             fontsize=mti.FS_FOOT, color=mti.MUTED, ha="left", va="baseline")

    out = os.path.join(os.path.dirname(__file__), "..", "drafts",
                       "2026-08-14-whitesox-tigers-series.png")
    fig.savefig(out, dpi=200, facecolor=mti.SURFACE)
    print("wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
