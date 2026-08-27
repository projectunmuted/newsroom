#!/usr/bin/env python3
"""Inline SVG: run differential by month for two clubs, side by side.

    python scripts/monthly_diff_chart.py 116 119 > /tmp/chart.svg

Pulled live from the schedule endpoint on every run and every value it draws is
printed to stderr, so re-running the script is the diff (WOODWARD-TODO,
2026-08-24). Colors are the site's validated --chart-pos / --chart-neg tokens
and encode sign only; the clubs are told apart by the row label, which keeps the
figure readable in greyscale and for a colorblind reader.

'Completed Early' is a real shortened game and counts. 'Postponed' carries
abstractGameState Final and must not.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from collections import OrderedDict

MONTHS = {"03": "March", "04": "April", "05": "May",
          "06": "June", "07": "July", "08": "August"}
PAD_L, PAD_R = 150, 44
BAR_H, PAIR_GAP, MONTH_GAP = 15, 3, 11
TOP, BOTTOM = 50, 30


def fetch(team_id: int, end: str) -> tuple[str, "OrderedDict[str, list[int]]"]:
    url = (f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={team_id}"
           f"&startDate=2026-03-01&endDate={end}&gameType=R")
    req = urllib.request.Request(url, headers={"User-Agent": "dsr-chart"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
    name, months = None, OrderedDict()
    for date in data["dates"]:
        for g in date["games"]:
            if g["status"]["detailedState"] not in ("Final", "Completed Early"):
                continue
            home = g["teams"]["home"]["team"]["id"] == team_id
            us = g["teams"]["home" if home else "away"]
            them = g["teams"]["away" if home else "home"]
            if "score" not in us or "score" not in them:
                continue
            name = us["team"]["name"]
            b = months.setdefault(date["date"][5:7], [0, 0, 0, 0])
            b[0] += us["score"] > them["score"]
            b[1] += us["score"] < them["score"]
            b[2] += us["score"] - them["score"]
            b[3] += 1
    return name, months


def bar_path(x0: float, x1: float, y: float, h: float, r: float = 3.0) -> str:
    if abs(x1 - x0) < r:
        return f"M{x0},{y}H{x1}V{y+h}H{x0}Z"
    if x1 > x0:
        return (f"M{x0},{y}H{x1-r}A{r},{r} 0 0 1 {x1},{y+r}"
                f"V{y+h-r}A{r},{r} 0 0 1 {x1-r},{y+h}H{x0}Z")
    return (f"M{x0},{y}H{x1+r}A{r},{r} 0 0 0 {x1},{y+r}"
            f"V{y+h-r}A{r},{r} 0 0 0 {x1+r},{y+h}H{x0}Z")


def build(clubs, width: int = 640) -> str:
    keys = sorted({k for _, m in clubs for k in m})
    rows = []
    for k in keys:
        for i, (name, months) in enumerate(clubs):
            w, l, diff, gp = months.get(k, [0, 0, 0, 0])
            rows.append({"month": MONTHS.get(k, k), "club": name, "w": w, "l": l,
                         "diff": diff, "gp": gp, "first": i == 0})

    lo = min(-5, min(r["diff"] for r in rows)) - 6
    hi = max(5, max(r["diff"] for r in rows)) + 6
    plot_w = width - PAD_L - PAD_R
    to_x = lambda v: PAD_L + (v - lo) / (hi - lo) * plot_w
    zero = to_x(0)

    height = TOP + BOTTOM
    for r in rows:
        height += BAR_H + (MONTH_GAP if r["first"] else PAIR_GAP)

    out = [
        f'<svg viewBox="0 0 {width} {height:.0f}" width="100%" role="img" '
        f'aria-labelledby="mdiff-title" style="max-width:{width}px;height:auto;'
        f"font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,"
        f'sans-serif">',
        '<title id="mdiff-title">Run differential by month, Detroit and Los '
        'Angeles, 2026</title>',
        '<text x="0" y="17" fill="var(--fg)" font-size="13" font-weight="600">'
        'Run differential by month, 2026</text>',
        '<text x="0" y="35" fill="var(--muted)" font-size="11">'
        'Runs scored minus runs allowed, regular season games only.</text>',
        f'<line x1="{zero:.1f}" y1="{TOP-8}" x2="{zero:.1f}" '
        f'y2="{height-BOTTOM+2:.0f}" stroke="var(--rule)" stroke-width="2"/>',
    ]

    y = TOP
    for r in rows:
        y += MONTH_GAP if r["first"] else PAIR_GAP
        x_end = to_x(r["diff"])
        x_start = zero + (2 if r["diff"] >= 0 else -2)
        color = "var(--chart-pos)" if r["diff"] >= 0 else "var(--chart-neg)"
        label = f'{r["month"]} {r["club"]}' if r["first"] else r["club"]
        out.append(
            f'<text x="{PAD_L-12}" y="{y+BAR_H/2+4:.1f}" text-anchor="end" '
            f'fill="var(--{"fg" if r["first"] else "muted"})" font-size="11.5">'
            f'{label}</text>')
        out.append(
            f'<path d="{bar_path(x_start, x_end, y, BAR_H)}" fill="{color}">'
            f'<title>{r["club"]}, {r["month"]}: {r["w"]}-{r["l"]}, '
            f'{r["diff"]:+d} runs over {r["gp"]} games</title></path>')
        anchor, dx = ("start", 7) if r["diff"] >= 0 else ("end", -7)
        out.append(
            f'<text x="{x_end+dx:.1f}" y="{y+BAR_H/2+4:.1f}" '
            f'text-anchor="{anchor}" fill="var(--muted)" font-size="11" '
            f'font-variant-numeric="tabular-nums">{r["diff"]:+d}</text>')
        y += BAR_H

    out.append("</svg>")

    print("Values drawn:", file=sys.stderr)
    for r in rows:
        print(f"  {r['month']:<8} {r['club']:<20} {r['w']}-{r['l']} "
              f"{r['diff']:+d} over {r['gp']} G", file=sys.stderr)
    return "\n".join(out)


if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:3]] or [116, 119]
    end = sys.argv[3] if len(sys.argv) > 3 else "2026-08-27"
    clubs = [fetch(i, end) for i in ids]
    if any(not c[0] or len(c[1]) < 2 for c in clubs):
        sys.exit("partial read; not drawing")
    print(build(clubs))
