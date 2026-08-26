#!/usr/bin/env python3
"""Emit an inline SVG: the unbroken run of games each NFL club plays after its bye.

Pulled live from ESPN's public JSON on every run, same source and same shape as
scripts/nfl_bye_structure.py, so a published figure cannot drift from the numbers
behind it. Every value drawn is also printed to stderr, which makes re-running
this the diff.

    python scripts/nfl_bye_chart.py > /tmp/chart.svg

Colors are the site's validated --chart-pos / --chart-neg tokens plus --fg,
--muted and --rule, so the figure follows light and dark mode.
"""
from __future__ import annotations

import json
import sys
import urllib.request

TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
SCHED_URL = ("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/"
             "{abbr}/schedule?season=2026&seasontype=2")
LAST_WEEK = 18
HIGHLIGHT = "Detroit Lions"

PAD_L, PAD_R = 150, 44
BAR_H, ROW_GAP = 15, 6
TOP, BOTTOM = 50, 30
WIDTH = 720


def fetch() -> list[dict]:
    with urllib.request.urlopen(TEAMS_URL, timeout=30) as r:
        roster = json.load(r)["sports"][0]["leagues"][0]["teams"]

    out = []
    for t in roster:
        abbr = t["team"]["abbreviation"]
        name = t["team"]["displayName"]
        with urllib.request.urlopen(
                SCHED_URL.format(abbr=abbr.lower()), timeout=30) as r:
            data = json.load(r)
        weeks = sorted({(e.get("week") or {}).get("number")
                        for e in data.get("events", [])} - {None})
        if len(weeks) != LAST_WEEK - 1:
            raise SystemExit(
                "PARTIAL: %s returned %d weeks, expected %d. Nothing drawn."
                % (abbr, len(weeks), LAST_WEEK - 1))
        byes = [w for w in range(1, LAST_WEEK + 1) if w not in weeks]
        if len(byes) != 1:
            raise SystemExit("PARTIAL: %s has byes %s. Nothing drawn." % (abbr, byes))
        out.append({"abbr": abbr, "name": name, "bye": byes[0],
                    "after": LAST_WEEK - byes[0]})
    return sorted(out, key=lambda t: (-t["after"], t["name"]))


def render(teams: list[dict]) -> str:
    hi = max(t["after"] for t in teams)
    plot_w = WIDTH - PAD_L - PAD_R
    to_w = lambda v: v / hi * plot_w
    height = TOP + len(teams) * (BAR_H + ROW_GAP) - ROW_GAP + BOTTOM

    out = [
        f'<svg viewBox="0 0 {WIDTH} {height}" width="100%" role="img" '
        f'aria-labelledby="bye-title" '
        f'style="max-width:{WIDTH}px;height:auto;font-family:ui-sans-serif,'
        f'system-ui,-apple-system,\'Segoe UI\',Roboto,sans-serif">',
        '<title id="bye-title">Games played after the bye week, all 32 NFL clubs, '
        '2026</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        'Games left after the bye, 2026</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">'
        'An earlier bye means a longer unbroken run to finish the season. '
        'Bye week in brackets.</text>',
        f'<line x1="{PAD_L}" y1="{TOP-8}" x2="{PAD_L}" y2="{height-BOTTOM+4}" '
        f'stroke="var(--rule)" stroke-width="2"/>',
    ]

    for i, t in enumerate(teams):
        y = TOP + i * (BAR_H + ROW_GAP)
        w = to_w(t["after"])
        me = t["name"] == HIGHLIGHT
        color = "var(--chart-neg)" if me else "var(--chart-pos)"
        out.append(
            f'<text x="{PAD_L-10}" y="{y+BAR_H/2+4:.1f}" text-anchor="end" '
            f'fill="var(--fg)" font-size="11.5" '
            f'font-weight="{700 if me else 400}">{t["name"]} ({t["bye"]})</text>')
        out.append(
            f'<rect x="{PAD_L+2}" y="{y}" width="{w:.1f}" height="{BAR_H}" '
            f'rx="2" fill="{color}"><title>{t["name"]}: bye in week {t["bye"]}, '
            f'{t["after"]} games after it</title></rect>')
        out.append(
            f'<text x="{PAD_L+w+10:.1f}" y="{y+BAR_H/2+4:.1f}" '
            f'fill="var(--muted)" font-size="11.5" '
            f'font-variant-numeric="tabular-nums">{t["after"]}</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    data = fetch()
    for t in data:
        print("%-24s bye wk%-3d %2d after" % (t["name"], t["bye"], t["after"]),
              file=sys.stderr)
    sys.stdout.write(render(data) + "\n")
