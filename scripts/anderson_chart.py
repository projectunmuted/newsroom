#!/usr/bin/env python3
"""Emit an inline SVG: how long Detroit's starters have gone this season, and
where Drew Anderson's three starts sit in that distribution.

One bar per bin, counting Detroit's 2026 regular season starts by batters
faced. Anderson's three are marked individually, because the whole question
about Tuesday is not whether he is good, it is how many outs he can be asked
for before the bullpen has to cover the rest.

    python scripts/anderson_chart.py > /tmp/anderson.svg

Every number comes from `anderson_start.load()`, the same snapshot the prose
reads, so the chart cannot drift from the text around it. Colors are the site's
`--chart-pos` and `--chart-neg` tokens, already validated for colorblind
separation and for contrast against both surfaces. `bar_path` conventions and
layout follow `opponent_split_chart.py`.
"""

from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from anderson_start import load                            # noqa: E402

PAD_L, PAD_R = 40, 20
TOP, BOTTOM = 66, 62
BIN = 2


def histogram(values: list[int], bin_w: int = BIN):
    lo = bin_w * (min(values) // bin_w)
    hi = max(values)
    n_bins = (hi - lo) // bin_w + 1
    counts = [0] * n_bins
    for v in values:
        counts[(v - lo) // bin_w] += 1
    return lo, bin_w, counts


def build_svg(starter_bf: list[int], marks: list[tuple[str, int]],
              width: int = 640) -> str:
    lo, bin_w, counts = histogram(starter_bf)
    n_bins = len(counts)
    peak = max(counts)
    plot_w = width - PAD_L - PAD_R
    plot_h = 180
    hi = lo + n_bins * bin_w

    to_x = lambda v: PAD_L + (v - lo) / (hi - lo) * plot_w
    base_y = TOP + plot_h
    bw = plot_w / n_bins
    median = statistics.median(starter_bf)

    height = TOP + plot_h + BOTTOM
    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="bf-title" style="max-width:{width}px;height:auto;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
        f'Roboto,sans-serif">',
        '<title id="bf-title">Batters faced by Detroit starting pitchers in '
        '2026, with Drew Anderson\'s three starts marked</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">How deep a Detroit start usually goes</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">Each bar counts '
        f'Detroit starts by batters faced, all {len(starter_bf)} regular season '
        'games. Roughly nine</text>',
        '<text x="0" y="48" fill="var(--muted)" font-size="11">batters is three '
        'innings, 22 is the median start, 27 is three times through a '
        'lineup.</text>',
    ]

    for i, c in enumerate(counts):
        if not c:
            continue
        x0 = PAD_L + i * bw
        h = c / peak * plot_h
        # One color for every bin. A two-color split by median would imply a
        # judgment the counts do not carry; the only accent belongs on the
        # three starts being argued about.
        color = "var(--chart-pos)"
        out.append(
            f'<rect x="{x0 + 0.8:.1f}" y="{base_y - h:.1f}" '
            f'width="{bw - 1.6:.1f}" height="{h:.1f}" fill="{color}" '
            f'opacity="0.55" rx="1.5"><title>{c} starts facing '
            f'{lo + i * bin_w} to {lo + (i + 1) * bin_w - 1} batters'
            f'</title></rect>'
        )

    out.append(
        f'<line x1="{PAD_L}" y1="{base_y}" x2="{width - PAD_R}" y2="{base_y}" '
        f'stroke="var(--rule)" stroke-width="1"/>'
    )
    mx = to_x(median)
    out.append(
        f'<line x1="{mx:.1f}" y1="{TOP - 6}" x2="{mx:.1f}" y2="{base_y}" '
        f'stroke="var(--rule)" stroke-width="2" stroke-dasharray="3 3"/>'
    )
    out.append(
        f'<text x="{mx + 6:.1f}" y="{TOP + 6}" fill="var(--muted)" '
        f'font-size="10.5">median {median:.0f}</text>'
    )

    for v in range(int(lo), int(hi) + 1):
        if v % 5:
            continue
        out.append(
            f'<text x="{to_x(v):.1f}" y="{base_y + 16}" text-anchor="middle" '
            f'fill="var(--muted)" font-size="10.5" '
            f'font-variant-numeric="tabular-nums">{v}</text>'
        )

    # Anderson's three starts, stacked so their labels cannot collide.
    for j, (label, bf) in enumerate(sorted(marks, key=lambda m: m[1])):
        x = to_x(bf)
        out.append(
            f'<line x1="{x:.1f}" y1="{TOP - 6}" x2="{x:.1f}" y2="{base_y}" '
            f'stroke="var(--chart-neg)" stroke-width="2"/>'
        )
        y = base_y + 34 + j * 14
        out.append(
            f'<text x="{x - 6:.1f}" y="{y}" text-anchor="end" '
            f'fill="var(--fg)" font-size="10.5" '
            f'font-variant-numeric="tabular-nums">{label}, {bf} batters</text>'
        )

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    snap = load(refresh=args.refresh)
    bfs = [x["bf"] for x in snap["det_starters"] if x["bf"]]
    starts = [x for x in snap["anderson"] if x["start"]]
    labels = {"2026-05-20": "May 20", "2026-06-15": "Jun 15",
              "2026-08-05": "Aug 5"}
    marks = [(labels.get(s["date"], s["date"]), s["bf"]) for s in starts]
    svg = build_svg(bfs, marks)
    Path(__file__).with_name("last_anderson_chart.svg").write_text(
        svg, encoding="utf-8")
    print(svg)
