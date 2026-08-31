#!/usr/bin/env python3
"""Emit an inline SVG: Pistons and Red Wings wins per 82 games, 2015 to 2026.

Two Detroit rebuilds started in roughly the same place and ended in completely
different ones. The Pistons bottomed out at 14 wins and just won 60. The Red
Wings have not won more than 41 in any season since 2015, and have landed on
exactly 41 three times.

    python scripts/two_rebuilds_chart.py > /tmp/chart.svg

Counted from ESPN's schedule endpoint on every run rather than from a record
field, because the record field carries the current season and reads 0-0
between seasons. Shortened seasons (the 2020 and 2021 covid years, the 2013 NHL
lockout) are converted to an 82-game pace and marked with a dot, so a bar is
never comparing 56 games to 82 without saying so.

Colors are the site's `--chart-pos` and `--chart-neg` tokens, already validated
for colorblind separation and for contrast against both surfaces.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pythag_chart import bar_path                          # noqa: E402

FIRST, LAST = 2015, 2026
CLUBS = (
    ("Pistons", "basketball", "nba", "var(--chart-pos)"),
    ("Red Wings", "hockey", "nhl", "var(--chart-neg)"),
)
PAD_L, PAD_R = 74, 52
TOP, BOTTOM = 78, 42
ROW_H, BAR_H = 15, 11


def get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def season(sport: str, league: str, year: int) -> tuple[int, int]:
    """(wins, decisions) for Detroit in one completed regular season.

    Wins are counted off the competitor `winner` flag, which is the league's
    own win column: an NHL overtime loss is not a win here, same as the
    standings.
    """
    d = get(f"https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}"
            f"/teams/det/schedule?season={year}&seasontype=2")
    w = n = 0
    for e in d.get("events", []):
        c = e["competitions"][0]
        if not c.get("status", {}).get("type", {}).get("completed"):
            continue
        for x in c["competitors"]:
            if x["team"]["abbreviation"].lower() == "det":
                n += 1
                if x.get("winner"):
                    w += 1
    return w, n


def load() -> list[dict]:
    rows = []
    for year in range(FIRST, LAST + 1):
        row = {"year": year}
        for name, sport, league, _ in CLUBS:
            w, n = season(sport, league, year)
            if n == 0:                     # 2005 NHL lockout shape, no games
                row[name] = None
                continue
            row[name] = {"w": w, "n": n, "pace": w / n * 82, "short": n < 78}
        rows.append(row)
    return rows


def build_svg(rows: list[dict], width: int = 640) -> str:
    plot_w = width - PAD_L - PAD_R
    hi = 66.0
    to_x = lambda v: PAD_L + v / hi * plot_w
    height = TOP + len(rows) * (ROW_H * 2 + 6) + BOTTOM

    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="reb-title" style="max-width:{width}px;height:auto;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
        f'Roboto,sans-serif">',
        '<title id="reb-title">Detroit Pistons and Detroit Red Wings wins per '
        '82 games, season by season, 2015 through 2026</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">Two rebuilds, same city, same twelve years</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">Wins per 82 '
        'games. A dot marks a shortened season converted to an 82 game '
        'pace.</text>',
        '<text x="0" y="48" fill="var(--muted)" font-size="11">Seasons are '
        'labelled by the year they finished.</text>',
    ]
    for i, (name, _, _, color) in enumerate(CLUBS):
        x = 0 + i * 110
        out.append(f'<rect x="{x}" y="{58}" width="9" height="9" '
                   f'fill="{color}" rx="2"/>')
        out.append(f'<text x="{x + 14}" y="{66}" fill="var(--muted)" '
                   f'font-size="11">{name}</text>')

    for i, row in enumerate(rows):
        y0 = TOP + i * (ROW_H * 2 + 6)
        out.append(
            f'<text x="0" y="{y0 + ROW_H + 4}" fill="var(--muted)" '
            f'font-size="11" font-variant-numeric="tabular-nums">'
            f'{row["year"]}</text>'
        )
        for j, (name, _, _, color) in enumerate(CLUBS):
            v = row[name]
            y = y0 + j * ROW_H
            if v is None:
                out.append(f'<text x="{PAD_L}" y="{y + BAR_H}" '
                           f'fill="var(--muted)" font-size="10">no season'
                           f'</text>')
                continue
            out.append(
                f'<path d="{bar_path(to_x(0), to_x(v["pace"]), y + 1, BAR_H)}" '
                f'fill="{color}" opacity="0.75"><title>{name} {row["year"]}: '
                f'{v["w"]} wins in {v["n"]} games, a pace of '
                f'{v["pace"]:.0f} per 82</title></path>'
            )
            label = f'{v["w"]}' if not v["short"] else f'{v["pace"]:.0f}*'
            out.append(
                f'<text x="{to_x(v["pace"]) + 6:.1f}" y="{y + BAR_H}" '
                f'fill="var(--fg)" font-size="10" '
                f'font-variant-numeric="tabular-nums">{label}</text>'
            )
            if v["short"]:
                out.append(
                    f'<circle cx="{PAD_L - 10}" cy="{y + BAR_H / 2 + 1}" '
                    f'r="2.4" fill="var(--muted)"><title>{row["year"]}: only '
                    f'{v["n"]} games played, shown as a per 82 pace</title>'
                    f'</circle>'
                )

    base_y = TOP + len(rows) * (ROW_H * 2 + 6)
    out.append(f'<line x1="{to_x(0):.1f}" y1="{TOP - 4}" '
               f'x2="{to_x(0):.1f}" y2="{base_y}" stroke="var(--rule)" '
               f'stroke-width="1"/>')
    out.append(f'<line x1="{to_x(41):.1f}" y1="{TOP - 4}" '
               f'x2="{to_x(41):.1f}" y2="{base_y}" stroke="var(--muted)" '
               f'stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>')
    out.append(f'<text x="{to_x(41):.1f}" y="{base_y + 16}" '
               f'text-anchor="middle" fill="var(--muted)" font-size="10">41'
               f'</text>')
    out.append(f'<text x="0" y="{base_y + 32}" fill="var(--muted)" '
               f'font-size="10.5">The dashed line is 41 wins. The Red Wings '
               f'have not cleared it since 2015.</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    data = load()
    svg = build_svg(data)
    (Path(__file__).resolve().parent / "last_two_rebuilds.svg").write_text(
        svg, encoding="utf-8")
    for r in data:
        bits = []
        for name, _, _, _ in CLUBS:
            v = r[name]
            bits.append(f'{name} {v["w"]}-{v["n"]-v["w"]}'
                        + (" *" if v["short"] else "") if v else f"{name} none")
        print(r["year"], " | ".join(bits), file=sys.stderr)
    print(svg)
