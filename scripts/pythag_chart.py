#!/usr/bin/env python3
"""Emit an inline SVG: wins above/below Pythagorean expectation, one division.

The chart is derived from live data every time rather than hand-drawn, so the
numbers in a published piece can never drift from the numbers behind it.

    python scripts/pythag_chart.py 202 > /tmp/chart.svg
    python scripts/pythag_chart.py all > /tmp/chart.svg   # all 30 teams

Division ids: 200 AL West, 201 AL East, 202 AL Central,
              203 NL West, 204 NL East, 205 NL Central

Pass "all" instead of a division id for the whole league. That mode exists
because the interesting comparison is sometimes across divisions: on 2026-08-24
the Tigers and the Rays sat at opposite ends of this distribution and played
each other, which the AL Central view cannot show.

Colors come from CSS custom properties the site defines (--chart-pos,
--chart-neg, --fg, --muted), so the figure follows light and dark mode without
a second copy. Those two hues were validated for colorblind separation and
contrast against both surfaces before use.

Pythagorean exponent 1.83 (Baseball Reference's standard for MLB).
"""

from __future__ import annotations

import json
import sys
import urllib.request

EXP = 1.83
PAD_L, PAD_R = 118, 34          # room for team names, room for value labels
BAR_H, ROW_GAP = 22, 12
TOP, BOTTOM = 46, 34


def fetch(division: int | None) -> list[dict]:
    """division=None means every team in both leagues."""
    url = ("https://statsapi.mlb.com/api/v1/standings"
           "?leagueId=103,104&season=2026&standingsTypes=regularSeason")
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)

    teams = []
    for record in data["records"]:
        if division is not None and record.get("division", {}).get("id") != division:
            continue
        for t in record["teamRecords"]:
            rs, ra = t.get("runsScored"), t.get("runsAllowed")
            if not rs or not ra:
                continue
            w, l = t["wins"], t["losses"]
            expected = (rs ** EXP) / ((rs ** EXP) + (ra ** EXP)) * (w + l)
            teams.append({
                "name": t["team"]["name"], "w": w, "l": l,
                "rs": rs, "ra": ra, "expected": expected, "gap": w - expected,
            })
    return sorted(teams, key=lambda t: -t["gap"])


def bar_path(x0: float, x1: float, y: float, h: float, r: float = 4.0) -> str:
    """Rect with only the data end rounded; the baseline end stays square so the
    bar reads as anchored to zero rather than floating."""
    if abs(x1 - x0) < r:                       # too short to round cleanly
        return f"M{x0},{y}H{x1}V{y+h}H{x0}Z"
    if x1 > x0:                                 # extends right
        return (f"M{x0},{y}H{x1-r}A{r},{r} 0 0 1 {x1},{y+r}"
                f"V{y+h-r}A{r},{r} 0 0 1 {x1-r},{y+h}H{x0}Z")
    return (f"M{x0},{y}H{x1+r}A{r},{r} 0 0 0 {x1},{y+r}"
            f"V{y+h-r}A{r},{r} 0 0 0 {x1+r},{y+h}H{x0}Z")


def build(teams: list[dict], width: int = 640, subtitle: str = "AL Central",
          highlight: tuple[str, ...] = ()) -> str:
    global BAR_H, ROW_GAP
    if len(teams) > 8:                          # 30 rows need thinner bars
        BAR_H, ROW_GAP = 16, 7
    lo = min(-1.0, min(t["gap"] for t in teams)) - 0.8
    hi = max(1.0, max(t["gap"] for t in teams)) + 0.8
    plot_w = width - PAD_L - PAD_R
    span = hi - lo
    to_x = lambda v: PAD_L + (v - lo) / span * plot_w
    zero = to_x(0)

    height = TOP + len(teams) * (BAR_H + ROW_GAP) - ROW_GAP + BOTTOM
    out: list[str] = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" '
        f'role="img" aria-labelledby="pythag-title" '
        f'style="max-width:{width}px;height:auto;font-family:ui-sans-serif,'
        f'system-ui,-apple-system,\'Segoe UI\',Roboto,sans-serif">',
        f'<title id="pythag-title">Wins above or below Pythagorean expectation, '
        f'{subtitle}</title>',
        f'<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        f'Wins above or below expectation</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">'
        f'Based on runs scored and allowed. Zero means the record matches the '
        f'run differential.</text>',
    ]

    # Zero baseline, drawn first so bars sit on top of it.
    out.append(f'<line x1="{zero:.1f}" y1="{TOP-6}" x2="{zero:.1f}" '
               f'y2="{height-BOTTOM+6:.1f}" stroke="var(--rule)" stroke-width="2"/>')

    for i, t in enumerate(teams):
        y = TOP + i * (BAR_H + ROW_GAP)
        x_end = to_x(t["gap"])
        color = "var(--chart-pos)" if t["gap"] >= 0 else "var(--chart-neg)"
        label = f'{t["gap"]:+.1f}'
        # 2px surface gap keeps a bar from touching the zero rule.
        x_start = zero + (2 if t["gap"] >= 0 else -2)

        out.append(
            f'<text x="{PAD_L-12}" y="{y+BAR_H/2+4:.1f}" text-anchor="end" '
            f'fill="var(--fg)" font-size="12.5" '
            f'font-weight="{600 if t["name"] in highlight else 400}"'
            f'>{t["name"]}</text>'
        )
        out.append(
            f'<path d="{bar_path(x_start, x_end, y, BAR_H)}" fill="{color}">'
            f'<title>{t["name"]}: {t["w"]}-{t["l"]}, expected '
            f'{t["expected"]:.1f} wins from {t["rs"]} runs scored and '
            f'{t["ra"]} allowed ({label} wins)</title></path>'
        )
        anchor, dx = ("start", 8) if t["gap"] >= 0 else ("end", -8)
        out.append(
            f'<text x="{x_end+dx:.1f}" y="{y+BAR_H/2+4:.1f}" '
            f'text-anchor="{anchor}" fill="var(--muted)" font-size="12" '
            f'font-variant-numeric="tabular-nums">{label}</text>'
        )

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "202"
    if arg == "all":
        division, subtitle = None, "all 30 teams"
    else:
        division, subtitle = int(arg), "one division"
    print(build(fetch(division), subtitle=subtitle,
                highlight=("Tigers", "Rays")))
