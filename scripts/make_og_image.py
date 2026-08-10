#!/usr/bin/env python3
"""Generate the 1200x630 share card for each site.

Why: every link to either site shared to Reddit, Discord, iMessage or anywhere
else rendered as a bare grey text box, because neither site had an og:image.
For a project whose only realistic distribution for months is somebody sharing a
link, that card is worth more than any amount of schema markup.

Writes docs/og.png and docs_dsr/og.png. Run after build.py; build.py does not
overwrite them, but it does delete the output directories, so the order is:

    python build.py && python scripts/make_og_image.py

Matplotlib only, which is already a dependency of the chart scripts. build.py
itself stays stdlib-only.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).parent.parent

CARDS = [
    {
        "out": ROOT / "docs_dsr" / "og.png",
        "bg": "#0f1720",
        "accent": "#6db3e8",
        "kicker": "DETROITSPORTSREPORTER.COM",
        "title": "Every call made before the game.\nEvery grade published after.",
        "sub": "Tigers  ·  Lions  ·  Pistons  ·  Red Wings",
    },
    {
        "out": ROOT / "docs" / "og.png",
        "bg": "#17130f",
        "accent": "#d9a06a",
        "kicker": "PROJECT-UNMUTED.COM",
        "title": "An AI agent trying to earn\none dollar, in public.",
        "sub": "The reasoning, the failures, and the working log",
    },
]

W, H = 1200, 630
DPI = 100


def card(spec: dict) -> None:
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=spec["bg"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_facecolor(spec["bg"])

    # Accent bar down the left edge, the one piece of brand in the card.
    ax.add_patch(Rectangle((0, 0), 14, H, color=spec["accent"]))

    ax.text(80, H - 96, spec["kicker"], color=spec["accent"], fontsize=17,
            fontweight="bold", va="top", family="DejaVu Sans")
    # Shrink until the longest line actually fits inside the card. The first
    # version was sized by eye and ran off the right edge, which is exactly the
    # failure a share card cannot have: nobody sees it before it is public.
    fig.canvas.draw()
    limit = W - 160
    size = 54
    while size > 24:
        probe = ax.text(80, H - 150, spec["title"], color="#ffffff",
                        fontsize=size, fontweight="bold", va="top",
                        linespacing=1.25, family="DejaVu Sans")
        fig.canvas.draw()
        width = probe.get_window_extent(fig.canvas.get_renderer()).width
        if width <= limit:
            break
        probe.remove()
        size -= 2
    ax.text(80, 96, spec["sub"], color="#9fb0bf", fontsize=22, va="bottom",
            family="DejaVu Sans")

    spec["out"].parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(spec["out"], dpi=DPI, facecolor=spec["bg"])
    plt.close(fig)
    print(f"wrote {spec['out'].relative_to(ROOT)}  {W}x{H}")


def main() -> int:
    for spec in CARDS:
        card(spec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
