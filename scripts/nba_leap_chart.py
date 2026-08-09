#!/usr/bin/env python3
"""Emit an inline SVG: the biggest two-year win swings in the NBA, and what
each of those teams did the following season.

The bar is the swing. The number in the right-hand column is what happened
next. Detroit sits on top with a swing nothing else in the sample matches, and
its next-year cell is empty because the season has not been played, which is
the whole point of the piece: the column that would tell you something is the
one that does not exist yet, and the column that does exist has no pattern in
it.

    python scripts/nba_leap_chart.py > /tmp/leaps.svg

Generated from live standings on every run via `nba_leaps.py`, so a number in
a published piece cannot drift from the number behind it. Colors are the site's
`--chart-pos` and `--chart-neg` tokens, already validated for colorblind
separation and for contrast against both the light and the dark surface.
Drawing code (`bar_path`) is imported from `pythag_chart.py` rather than copied.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from nba_leaps import load, spans                          # noqa: E402
from pythag_chart import bar_path                          # noqa: E402

PAD_L, PAD_R = 150, 96
TOP, BOTTOM = 74, 34
ROW_H = 21


def collect(top_n: int = 12):
    """Detroit plus the largest other climbs, keeping every tie at the cutoff.

    Slicing to a fixed length here was a real bug rather than a cosmetic one.
    Three teams sit at exactly +32.0, and a plain `[:n]` kept the one with a
    negative following season and dropped both with positive ones, purely on
    sort order. The chart then read as a column of declines under a caption
    saying there was no pattern. Ties come in together or not at all.
    """
    data = load()
    all_spans = spans(data)
    det = [s for s in all_spans if s["team"] == "DET" and s["end"] == 2026][0]
    others = sorted((s for s in all_spans
                     if not (s["team"] == "DET" and s["end"] == 2026)),
                    key=lambda s: -s["swing"])
    keep = max(0, top_n - 1)
    if keep < len(others):
        cutoff = others[keep - 1]["swing"] if keep else None
        while keep < len(others) and others[keep]["swing"] == cutoff:
            keep += 1
    return [det] + others[:keep]


def build_svg(rows: list[dict], width: int = 640) -> str:
    plot_w = width - PAD_L - PAD_R
    hi = max(r["swing"] for r in rows)
    to_x = lambda v: PAD_L + v / hi * plot_w
    height = TOP + len(rows) * ROW_H + BOTTOM

    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="leap-title" style="max-width:{width}px;height:auto;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
        f'Roboto,sans-serif">',
        '<title id="leap-title">The largest two-season win swings in the NBA '
        'since 1993, with each team\'s change in the following season</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">The biggest two-year climbs since 1993</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">Bar is the gain '
        'in wins per 82 games across two seasons. Right column is what that '
        'team</text>',
        '<text x="0" y="48" fill="var(--muted)" font-size="11">did the '
        'following season. A dot marks a span touching a lockout or covid '
        'season, converted to an 82-game pace.</text>',
        f'<text x="{width - PAD_R + 46}" y="62" text-anchor="middle" '
        f'fill="var(--muted)" font-size="10">next year</text>',
    ]

    for i, r in enumerate(rows):
        y = TOP + i * ROW_H
        det = r["team"] == "DET" and r["end"] == 2026
        weight = "600" if det else "400"
        fill = "var(--fg)" if det else "var(--muted)"
        out.append(
            f'<text x="0" y="{y + 13}" fill="{fill}" font-size="11" '
            f'font-weight="{weight}">{r["name"]}</text>'
        )
        out.append(
            f'<text x="{PAD_L - 8}" y="{y + 13}" text-anchor="end" '
            f'fill="var(--muted)" font-size="10" '
            f'font-variant-numeric="tabular-nums">{r["end"]}</text>'
        )
        if r["shortened"]:
            out.append(
                f'<circle cx="{PAD_L - 40}" cy="{y + 9.5}" r="2.4" '
                f'fill="var(--muted)"><title>{r["name"]} {r["end"]}: this span '
                f'includes a shortened season, so the figures are a per-82 '
                f'pace rather than games actually won. Raw: '
                f'{r["start_wins"]} to {r["peak_wins"]} wins</title></circle>'
            )
        out.append(
            f'<path d="{bar_path(to_x(0), to_x(r["swing"]), y + 3, ROW_H - 9)}" '
            f'fill="var(--chart-pos)" opacity="{0.85 if det else 0.4}">'
            f'<title>{r["name"]} {r["end"]}: {r["start_pace"]:.0f} to '
            f'{r["peak_pace"]:.0f} wins per 82, a gain of {r["swing"]:+.1f}'
            f'</title></path>'
        )
        out.append(
            f'<text x="{to_x(r["swing"]) + 6:.1f}" y="{y + 13}" '
            f'fill="var(--fg)" font-size="10.5" font-weight="{weight}" '
            f'font-variant-numeric="tabular-nums">{r["swing"]:+.0f}</text>'
        )

        # What happened next, in its own column.
        x_next = width - PAD_R + 46
        if r["after_pace"] is None:
            out.append(
                f'<text x="{x_next}" y="{y + 13}" text-anchor="middle" '
                f'fill="var(--muted)" font-size="10.5">not played</text>'
            )
        else:
            change = r["after_pace"] - r["peak_pace"]
            color = "var(--chart-pos)" if change >= 0 else "var(--chart-neg)"
            out.append(
                f'<text x="{x_next}" y="{y + 13}" text-anchor="middle" '
                f'fill="{color}" font-size="10.5" font-weight="600" '
                f'font-variant-numeric="tabular-nums">{change:+.0f}</text>'
            )

    base_y = TOP + len(rows) * ROW_H
    out.append(
        f'<line x1="{to_x(0):.1f}" y1="{TOP - 2}" x2="{to_x(0):.1f}" '
        f'y2="{base_y}" stroke="var(--rule)" stroke-width="1"/>'
    )
    out.append(
        f'<text x="{PAD_L}" y="{base_y + 18}" fill="var(--muted)" '
        f'font-size="10.5">No other team in the sample gained as much as '
        f'Detroit. What each of them did next runs both ways.</text>'
    )
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()
    svg = build_svg(collect(args.top))
    (Path(__file__).resolve().parent / "last_nba_leap_chart.svg").write_text(
        svg, encoding="utf-8")
    print(svg)
