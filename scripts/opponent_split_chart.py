#!/usr/bin/env python3
"""Emit an inline SVG: the distribution of every team-opponent offensive split.

One bar per bin, counting how many of baseball's team-opponent pairs sit at
each level of "runs per game in this matchup, minus runs per game for the
season." Detroit-vs-Cleveland is marked at the left tail and
Detroit-vs-Athletics at the right, because the entire argument of the piece is
that the same team owns both ends of the same distribution in the same season.

    python scripts/opponent_split_chart.py > /tmp/splits.svg
    python scripts/opponent_split_chart.py --min-games 6

Generated from live data on every run, so a number in a published piece cannot
drift from the number behind it. Colors are the site's `--chart-pos` and
`--chart-neg` tokens, already validated for colorblind separation and for
contrast against both the light and the dark surface. Drawing code (`bar_path`)
is imported from `pythag_chart.py` rather than copied.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from opponent_splits import build, fetch_season          # noqa: E402
from pythag_chart import bar_path                        # noqa: E402

PAD_L, PAD_R = 40, 20
TOP, BOTTOM = 62, 58
BIN = 0.5


def histogram(rows: list[dict], bin_w: float = BIN):
    lo = min(r["delta"] for r in rows)
    hi = max(r["delta"] for r in rows)
    start = bin_w * (lo // bin_w)
    n_bins = int((hi - start) // bin_w) + 1
    counts = [0] * n_bins
    for r in rows:
        counts[min(n_bins - 1, int((r["delta"] - start) // bin_w))] += 1
    return start, bin_w, counts


def build_svg(rows: list[dict], marks: list[tuple[str, str]],
              width: int = 640) -> str:
    start, bin_w, counts = histogram(rows)
    n_bins = len(counts)
    peak = max(counts)
    plot_w = width - PAD_L - PAD_R
    plot_h = 190
    bw = plot_w / n_bins

    lo = start
    hi = start + n_bins * bin_w
    to_x = lambda v: PAD_L + (v - lo) / (hi - lo) * plot_w
    base_y = TOP + plot_h
    zero = to_x(0)

    height = TOP + plot_h + BOTTOM
    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="split-title" style="max-width:{width}px;height:auto;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
        f'Roboto,sans-serif">',
        '<title id="split-title">Distribution of offensive performance by '
        'opponent across all team-opponent pairs in MLB, 2026</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">How much every team\'s offense changes by '
        'opponent</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">Each bar counts '
        f'team-opponent pairs. Horizontal axis is runs per game in that '
        f'matchup</text>',
        '<text x="0" y="48" fill="var(--muted)" font-size="11">minus that '
        'team\'s runs per game for the season. Pairs of six games or more.</text>',
    ]

    for i, c in enumerate(counts):
        if not c:
            continue
        x0 = PAD_L + i * bw
        h = c / peak * plot_h
        center = start + (i + 0.5) * bin_w
        color = "var(--chart-pos)" if center >= 0 else "var(--chart-neg)"
        out.append(
            f'<rect x="{x0 + 0.8:.1f}" y="{base_y - h:.1f}" '
            f'width="{bw - 1.6:.1f}" height="{h:.1f}" fill="{color}" '
            f'opacity="0.55" rx="1.5"><title>{c} pairs between '
            f'{center - bin_w / 2:+.1f} and {center + bin_w / 2:+.1f}'
            f'</title></rect>'
        )

    out.append(
        f'<line x1="{PAD_L}" y1="{base_y}" x2="{width - PAD_R}" y2="{base_y}" '
        f'stroke="var(--rule)" stroke-width="1"/>'
    )
    out.append(
        f'<line x1="{zero:.1f}" y1="{TOP - 4}" x2="{zero:.1f}" '
        f'y2="{base_y}" stroke="var(--rule)" stroke-width="2" '
        f'stroke-dasharray="3 3"/>'
    )

    for v in range(int(lo), int(hi) + 1):
        x = to_x(v)
        out.append(
            f'<text x="{x:.1f}" y="{base_y + 16}" text-anchor="middle" '
            f'fill="var(--muted)" font-size="10.5" '
            f'font-variant-numeric="tabular-nums">{v:+d}</text>'
        )

    # The two Detroit pairs, called out where they land.
    for j, (label, opp) in enumerate(marks):
        row = next(r for r in rows
                   if r["team"] == "Detroit Tigers" and r["opp"] == opp)
        x = to_x(row["delta"])
        y_top = TOP - 2
        color = "var(--chart-pos)" if row["delta"] >= 0 else "var(--chart-neg)"
        out.append(
            f'<line x1="{x:.1f}" y1="{y_top}" x2="{x:.1f}" y2="{base_y}" '
            f'stroke="{color}" stroke-width="2"/>'
        )
        anchor = "start" if row["delta"] < 0 else "end"
        dx = 6 if row["delta"] < 0 else -6
        out.append(
            f'<text x="{x + dx:.1f}" y="{base_y + 34}" text-anchor="{anchor}" '
            f'fill="var(--fg)" font-size="11" font-weight="600">{label}</text>'
        )
        out.append(
            f'<text x="{x + dx:.1f}" y="{base_y + 48}" text-anchor="{anchor}" '
            f'fill="var(--muted)" font-size="10.5" '
            f'font-variant-numeric="tabular-nums">{row["delta"]:+.2f} runs/game'
            f'</text>'
        )

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-games", type=int, default=6)
    ap.add_argument("--season", type=int, default=2026)
    args = ap.parse_args()
    _, rows = build(fetch_season(args.season), args.min_games)
    print(build_svg(rows, [("Tigers vs Cleveland", "Cleveland Guardians"),
                           ("Tigers vs Athletics", "Athletics")]))
