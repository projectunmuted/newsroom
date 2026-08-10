"""Render the Guardians-Tigers series preview tables as one PNG.

Numbers pulled from the MLB Stats API on 2026-08-10 (standings, team season
hitting/pitching, and the six completed head-to-head games). Re-run the pull and
paste into the DATA blocks if this is ever refreshed.

    python scripts/make_series_image.py

Writes drafts/2026-08-11-guardians-tigers-series.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import make_table_image as mti

# --- DATA (MLB Stats API, 2026-08-10) --------------------------------------

T1_TITLE = "Every meeting this season"
T1_COLS = ["Date", "Result", "Margin"]
T1_ALIGN = ["left", "left", "right"]
T1_ROWS = [
    ["May 18", "Cleveland 8, Detroit 2", "-6"],
    ["May 19", "Cleveland 4, Detroit 3", "-1"],
    ["May 20", "Cleveland 3, Detroit 2", "-1"],
    ["May 21", "Cleveland 3, Detroit 1", "-2"],
    ["Jun 12", "Cleveland 3, Detroit 2", "-1"],
    ["Jun 13", "Cleveland 3, Detroit 1", "-2"],
    ["Total", "Cleveland 24, Detroit 11", "0-6"],
]

T2_TITLE = "How the two teams compare"
T2_COLS = ["", "Tigers", "Guardians"]
T2_ALIGN = ["left", "right", "right"]
T2_ROWS = [
    ["Record", "58-60", "58-61"],
    ["Run differential", "+87", "-27"],
    ["Last ten", "7-3", "3-7"],
    ["Team ERA", "3.49", "3.84"],
    ["Team OPS", ".729", ".682"],
    ["Runs scored", "539", "473"],
    ["Saves / chances", "23 of 49", "34 of 48"],
    ["Blown saves", "26", "14"],
    ["Stolen bases", "35", "116"],
]

FOOTER = ("MLB Stats API, 2026-08-10. Series opens Tuesday at Comerica: "
          "Bibee vs Anderson, Griffin vs Valdez, Messick vs Montero.")


def main():
    mti.FOOTER = FOOTER
    total_h = (mti.PAD_TOP + mti.block_height(T1_ROWS) + mti.GAP
               + mti.block_height(T2_ROWS) + mti.PAD_BOTTOM)
    fig = plt.figure(figsize=(mti.FIG_W, total_h), dpi=200, facecolor=mti.SURFACE)

    y = mti.PAD_TOP
    y = mti.draw_block(fig, y, T1_TITLE, T1_COLS, T1_ALIGN, T1_ROWS,
                       weights=[1.0, 2.2, 0.9], span_frac=0.82,
                       hilite={"Total"})
    y += mti.GAP
    y = mti.draw_block(fig, y, T2_TITLE, T2_COLS, T2_ALIGN, T2_ROWS,
                       weights=[1.6, 1.0, 1.0], span_frac=0.72,
                       hilite={"Blown saves", "Stolen bases"})

    fig.text(mti.SIDE / mti.FIG_W, 1.0 - (y + 0.26) / total_h, FOOTER,
             fontsize=mti.FS_FOOT, color=mti.MUTED, ha="left", va="baseline")

    out = os.path.join(os.path.dirname(__file__), "..", "drafts",
                       "2026-08-11-guardians-tigers-series.png")
    fig.savefig(out, dpi=200, facecolor=mti.SURFACE)
    print("wrote", os.path.normpath(out))


if __name__ == "__main__":
    main()
