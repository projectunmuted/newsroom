#!/usr/bin/env python3
"""Emit an inline SVG: blowout win rate minus close-game win rate, all 30 teams.

The companion figure to `close_games.py`. A team whose bar runs far to the
right beats people up when the game is not close and loses when it is, which
is the exact shape of the 2026 Tigers.

    python scripts/close_gap_chart.py > /tmp/gap.svg
    python scripts/close_gap_chart.py --margin 1 --highlight "Detroit Tigers"

Generated from live data on every run, so a number in a published piece cannot
drift from the number behind it. Colors are the site's `--chart-pos` and
`--chart-neg` tokens, already validated for colorblind separation and for
contrast against both the light and the dark surface. Drawing code
(`bar_path`) is imported from `pythag_chart.py` rather than copied.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from close_games import load_snapshot, rate, team_games       # noqa: E402
from pythag_chart import bar_path                          # noqa: E402

PAD_L, PAD_R = 150, 44
BAR_H, ROW_GAP = 16, 7
TOP, BOTTOM = 50, 30


def rows(max_margin: int) -> list[dict]:
    per_team = team_games(load_snapshot())
    out = []
    for team, games in per_team.items():
        close = [g for g in games if g["margin"] <= max_margin]
        blow = [g for g in games if g["margin"] > max_margin]
        if not close or not blow:
            continue
        out.append({
            "name": team, "close": rate(close), "blow": rate(blow),
            "gap": rate(blow) - rate(close),
            "n_close": len(close), "n_blow": len(blow),
        })
    return sorted(out, key=lambda t: -t["gap"])


def build(teams: list[dict], max_margin: int, highlight: str,
          width: int = 640) -> str:
    lo = min(-0.05, min(t["gap"] for t in teams)) - 0.04
    hi = max(0.05, max(t["gap"] for t in teams)) + 0.04
    plot_w = width - PAD_L - PAD_R
    to_x = lambda v: PAD_L + (v - lo) / (hi - lo) * plot_w
    zero = to_x(0)

    close_label = ("one-run games" if max_margin == 1
                   else f"games decided by {max_margin} or fewer")
    height = TOP + len(teams) * (BAR_H + ROW_GAP) - ROW_GAP + BOTTOM
    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="gap-title" style="max-width:{width}px;height:auto;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
        f'Roboto,sans-serif">',
        f'<title id="gap-title">Win rate in blowouts minus win rate in '
        f'{close_label}, all 30 teams, 2026</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">Blowout win rate minus close-game win rate</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">Right of the '
        f'line means a team wins when the game is not close and loses when it '
        f'is. Close = {close_label}.</text>',
        f'<line x1="{zero:.1f}" y1="{TOP-6}" x2="{zero:.1f}" '
        f'y2="{height-BOTTOM+4:.1f}" stroke="var(--rule)" stroke-width="2"/>',
    ]

    for i, t in enumerate(teams):
        y = TOP + i * (BAR_H + ROW_GAP)
        x_end = to_x(t["gap"])
        color = "var(--chart-pos)" if t["gap"] >= 0 else "var(--chart-neg)"
        is_hl = t["name"] == highlight
        x_start = zero + (1.5 if t["gap"] >= 0 else -1.5)

        out.append(
            f'<text x="{PAD_L-12}" y="{y+BAR_H/2+4:.1f}" text-anchor="end" '
            f'fill="var(--fg)" font-size="11.5" '
            f'font-weight="{700 if is_hl else 400}">{t["name"]}</text>'
        )
        out.append(
            f'<path d="{bar_path(x_start, x_end, y, BAR_H, r=3.0)}" '
            f'fill="{color}" opacity="{1 if is_hl else 0.62}">'
            f'<title>{t["name"]}: {t["blow"]:.3f} in {t["n_blow"]} blowouts, '
            f'{t["close"]:.3f} in {t["n_close"]} close games '
            f'({t["gap"]:+.3f})</title></path>'
        )
        anchor, dx = ("start", 7) if t["gap"] >= 0 else ("end", -7)
        out.append(
            f'<text x="{x_end+dx:.1f}" y="{y+BAR_H/2+4:.1f}" '
            f'text-anchor="{anchor}" fill="var(--muted)" font-size="11" '
            f'font-variant-numeric="tabular-nums" '
            f'font-weight="{700 if is_hl else 400}">{t["gap"]:+.3f}</text>'
        )

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--margin", type=int, default=3)
    ap.add_argument("--highlight", default="Detroit Tigers")
    args = ap.parse_args()
    print(build(rows(args.margin), args.margin, args.highlight))
