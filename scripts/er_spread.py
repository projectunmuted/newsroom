#!/usr/bin/env python3
"""Compare two starters by the SHAPE of their start log, not their ERA.

An ERA is a mean, and a mean hides the tail. Two pitchers can sit half a run
apart on the back of the card while one of them has never given you a disaster
and the other hands you one every fifth time out. For a single game that
difference matters more than the average does, because you are buying one draw
from the distribution rather than the distribution itself.

    python scripts/er_spread.py 672456 677952 > /tmp/chart.svg
    python scripts/er_spread.py 672456 677952 --table

Emits a strip plot: one dot per start, x is earned runs allowed. Dots are
colored with --chart-pos below the blow-up line and --chart-neg at or above it,
using the two hues already validated for colorblind separation and contrast on
both surfaces. Overlapping starts stack vertically so the density is visible
rather than hidden behind a single mark.

Everything is derived from the MLB Stats API game log on every run, so a figure
in a published piece cannot drift from the numbers behind it.

Exit 2 if either pitcher has no starts this season, because a comparison with
an empty side is worse than no chart.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request

PAD_L, PAD_R = 116, 20
TOP, BOTTOM = 52, 34
LANE_H = 112          # vertical space per pitcher
DOT_R = 5.5
DOT_GAP = 13          # vertical spacing when starts stack on the same ER value
BLOWUP = 5            # at or above this many earned runs is the bad bucket


class NoStarts(Exception):
    pass


def fetch(player_id, season):
    url = ("https://statsapi.mlb.com/api/v1/people/%d"
           "/stats?stats=gameLog&group=pitching&season=%d" % (player_id, season))
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    if not data.get("stats") or not data["stats"][0]["splits"]:
        raise NoStarts()

    splits = data["stats"][0]["splits"]
    name = splits[0]["player"]["fullName"]
    starts = []
    for s in splits:
        st = s["stat"]
        if st["gamesStarted"] != 1:
            continue
        starts.append({
            "date": s["date"],
            "opp": s["opponent"]["name"],
            "er": int(st["earnedRuns"]),
            "outs": int(st["outs"]),
        })
    if not starts:
        raise NoStarts()
    return name, starts


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def summarize(name, starts):
    outs = sum(s["outs"] for s in starts)
    er = sum(s["er"] for s in starts)
    bad = [s for s in starts if s["er"] >= BLOWUP]
    return {
        "name": name,
        "n": len(starts),
        "blowups": len(bad),
        "worst": max(s["er"] for s in starts),
        "era": (er * 27.0 / outs) if outs else 0.0,
    }


def render(rows, width=640):
    max_er = max(s["er"] for _, st in rows for s in st)
    span = max(max_er, BLOWUP + 1)
    plot_w = width - PAD_L - PAD_R
    height = TOP + LANE_H * len(rows) + BOTTOM
    axis_y = TOP + LANE_H * len(rows) - 20

    def x_of(er):
        return PAD_L + (float(er) / span) * plot_w

    caps = []
    for name, st in rows:
        s = summarize(name, st)
        caps.append("%s: %d starts, worst %d earned, %d of %d at %d or more"
                    % (s["name"], s["n"], s["worst"], s["blowups"], s["n"], BLOWUP))
    alt = ("Every 2026 start by each pitcher, one dot per start, placed by "
           "earned runs allowed. " + ". ".join(caps) + ".")

    out = [
        '<svg viewBox="0 0 %d %d" width="100%%" role="img" '
        'aria-labelledby="es-title" style="max-width:%dpx;height:auto;'
        "font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,"
        'sans-serif">' % (width, height, width),
        '<title id="es-title">%s</title>' % esc(alt),
        '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        'One dot per start, placed by earned runs allowed</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">'
        '2026 starts only. Dots at %d or more earned runs are the tail</text>' % BLOWUP,
    ]

    for er in range(0, span + 1):
        gx = x_of(er)
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                   'stroke="var(--rule)" stroke-width="1" stroke-dasharray="3 5"/>'
                   % (gx, TOP - 10, gx, axis_y))
        out.append('<text x="%.1f" y="%.1f" text-anchor="middle" '
                   'fill="var(--muted)" font-size="10">%d</text>'
                   % (gx, axis_y + 14, er))
    out.append('<text x="%.1f" y="%.1f" text-anchor="middle" '
               'fill="var(--muted)" font-size="10">earned runs allowed in the '
               'start</text>' % (PAD_L + plot_w / 2, axis_y + 30))

    for i, (name, st) in enumerate(rows):
        s = summarize(name, st)
        base = TOP + LANE_H * i
        out.append('<text x="0" y="%.1f" fill="var(--fg)" font-size="11.5" '
                   'font-weight="600">%s</text>' % (base + 6, esc(s["name"])))
        out.append('<text x="0" y="%.1f" fill="var(--muted)" font-size="10" '
                   'font-variant-numeric="tabular-nums">%d starts, %.2f</text>'
                   % (base + 22, s["n"], s["era"]))

        stack = {}
        for start in sorted(st, key=lambda r: r["date"]):
            er = start["er"]
            k = stack.get(er, 0)
            stack[er] = k + 1
            cx = x_of(er)
            cy = base + 12 + k * DOT_GAP
            hue = "--chart-neg" if er >= BLOWUP else "--chart-pos"
            ip = "%d.%d" % (start["outs"] // 3, start["outs"] % 3)
            out.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="var(%s)" '
                       'opacity="0.85"><title>%s vs %s: %s IP, %d ER</title>'
                       '</circle>'
                       % (cx, cy, DOT_R, hue, start["date"], esc(start["opp"]),
                          ip, er))

    out.append("</svg>")
    return "\n".join(out)


def table(rows):
    lines = ["| Pitcher | Starts | ERA as a starter | Starts of %d+ earned | Worst |"
             % BLOWUP,
             "|---|---|---|---|---|"]
    for name, st in rows:
        s = summarize(name, st)
        lines.append("| %s | %d | %.2f | %d | %d |"
                     % (s["name"], s["n"], s["era"], s["blowups"], s["worst"]))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Strip plot of earned runs per start.")
    ap.add_argument("player_ids", type=int, nargs="+", help="MLB player ids")
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--table", action="store_true",
                    help="print the markdown summary table instead of the SVG")
    a = ap.parse_args()

    rows = []
    for pid in a.player_ids:
        try:
            rows.append(fetch(pid, a.season))
        except NoStarts:
            sys.stderr.write("player %d has no %d starts\n" % (pid, a.season))
            return 2
    sys.stdout.write((table(rows) if a.table else render(rows)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
