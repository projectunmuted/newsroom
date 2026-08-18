#!/usr/bin/env python3
"""Where a team's goals came from: the top 3 scorers against everybody else.

Written 2026-08-18 for the Red Wings floor. r/DetroitRedWings spent the week
arguing about whether Dylan Larkin is on the roster in October, and one thread
title made the checkable claim: with or without Larkin, Detroit still has to fix
the offense. This splits every team's 2025-26 goal total into 2 buckets, the 3
leading goal scorers and the whole rest of the roster, so "fix the offense" can
be pointed at a specific part of the roster instead of the whole thing.

Concentration on its own is not a finding. Colorado is one of the most top-heavy
teams in the league and scored 298 goals. What matters is the level of the
second bucket, which is why the chart plots both axes and the table ranks the
second one.

Sources, both free and keyless:

    api-web.nhle.com/v1/standings/2026-04-17        (final 2025-26 standings)
    api-web.nhle.com/v1/club-stats/<ABBREV>/20252026/2   (skater goals)

    python scripts/nhl_depth_scoring.py            # the SVG
    python scripts/nhl_depth_scoring.py --table    # the markdown table
    python scripts/nhl_depth_scoring.py --json     # every number, raw

33 requests, cached in logs/nhl-depth-cache.json for a day, so a re-run is free.
Exit 2 if any team returns no skaters, because a silently short roster would
move a rank without saying so.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "logs" / "nhl-depth-cache.json"
CACHE_HOURS = 24
SEASON = "20252026"
FINAL_STANDINGS = "2026-04-17"
TOP_N = 3


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as fh:
        return json.load(fh)


def load(force=False):
    """Every team's skater goal list, cached for a day."""
    if CACHE.exists() and not force:
        blob = json.loads(CACHE.read_text(encoding="utf-8"))
        if time.time() - blob.get("fetched_at", 0) < CACHE_HOURS * 3600:
            return blob["teams"]

    standings = get("https://api-web.nhle.com/v1/standings/%s" % FINAL_STANDINGS)
    teams = {}
    for row in standings["standings"]:
        ab = row["teamAbbrev"]["default"]
        club = get("https://api-web.nhle.com/v1/club-stats/%s/%s/2" % (ab, SEASON))
        skaters = club.get("skaters", [])
        if not skaters:
            sys.stderr.write("no skaters returned for %s\n" % ab)
            raise SystemExit(2)
        teams[ab] = {
            "name": row["teamName"]["default"],
            "points": row["points"],
            "goals_for": row["goalFor"],
            "goals_against": row["goalAgainst"],
            "scorers": sorted(
                ((s["goals"], s["firstName"]["default"] + " " + s["lastName"]["default"])
                 for s in skaters), reverse=True),
        }
        time.sleep(0.25)

    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps({"fetched_at": time.time(), "teams": teams}),
                     encoding="utf-8")
    return teams


def split(teams):
    """Per team: top-N goals, rest-of-roster goals, and the rank of each."""
    rows = {}
    for ab, t in teams.items():
        goals = [g for g, _ in t["scorers"]]
        top = sum(goals[:TOP_N])
        total = sum(goals)
        rows[ab] = {
            "team": t["name"], "points": t["points"],
            "skater_goals": total, "top": top, "rest": total - top,
            "top_names": [n for _, n in t["scorers"][:TOP_N]],
            "top_goals": [g for g, _ in t["scorers"][:TOP_N]],
        }

    for key in ("top", "rest", "skater_goals"):
        order = sorted(rows, key=lambda ab: -rows[ab][key])
        for i, ab in enumerate(order, 1):
            rows[ab][key + "_rank"] = i
    return rows


# --- chart -----------------------------------------------------------------

W, H = 640, 400
PAD_L, PAD_R, PAD_T, PAD_B = 44, 12, 46, 46


def render(rows, focus="DET"):
    xs = [r["top"] for r in rows.values()]
    ys = [r["rest"] for r in rows.values()]
    x0, x1 = min(xs) - 6, max(xs) + 6
    y0, y1 = min(ys) - 8, max(ys) + 8
    pw, ph = W - PAD_L - PAD_R, H - PAD_T - PAD_B

    def px(v):
        return PAD_L + (v - x0) / (x1 - x0) * pw

    def py(v):
        return PAD_T + ph - (v - y0) / (y1 - y0) * ph

    f = rows[focus]
    # Ties are broken arbitrarily by the sort, so say so rather than let a rank
    # imply a separation that is not in the data.
    tied = [r["team"] for ab, r in rows.items()
            if ab != focus and r["rest"] == f["rest"]]
    tie_note = (" tied with %s" % " and ".join(tied)) if tied else ""
    alt = ("Every NHL team's 2025-26 goals split in 2: the 3 leading goal "
           "scorers on the horizontal axis, the whole rest of the roster on the "
           "vertical. Skater goals only. %s sits at %d from its top 3, which is "
           "%d of 32, and %d from everybody else, which is %d of 32%s."
           % (f["team"], f["top"], f["top_rank"], f["rest"], f["rest_rank"],
              tie_note))

    out = [
        '<svg viewBox="0 0 %d %d" width="100%%" role="img" '
        'aria-labelledby="nds-title" style="max-width:%dpx;height:auto;'
        "font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,"
        'sans-serif">' % (W, H, W),
        '<title id="nds-title">%s</title>' % esc(alt),
        '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        'Goals from the top 3 scorers, against goals from everybody else</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">'
        '2025-26 regular season, all 32 teams. Skater goals only</text>',
    ]

    # gridlines every 20 goals on each axis
    step = 20
    gx = int(x0 / step + 1) * step
    while gx < x1:
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                   'stroke="var(--rule)" stroke-width="1" stroke-dasharray="3 5"/>'
                   % (px(gx), PAD_T, px(gx), PAD_T + ph))
        out.append('<text x="%.1f" y="%.1f" text-anchor="middle" '
                   'fill="var(--muted)" font-size="10">%d</text>'
                   % (px(gx), PAD_T + ph + 15, gx))
        gx += step
    gy = int(y0 / step + 1) * step
    while gy < y1:
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                   'stroke="var(--rule)" stroke-width="1" stroke-dasharray="3 5"/>'
                   % (PAD_L, py(gy), PAD_L + pw, py(gy)))
        out.append('<text x="%.1f" y="%.1f" text-anchor="end" '
                   'fill="var(--muted)" font-size="10">%d</text>'
                   % (PAD_L - 6, py(gy) + 3, gy))
        gy += step

    for ab, r in sorted(rows.items(), key=lambda kv: kv[0] == focus):
        is_f = ab == focus
        hue = "--chart-neg" if is_f else "--chart-pos"
        out.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="var(%s)" '
                   'opacity="%s"><title>%s: %d from the top 3, %d from the '
                   'rest</title></circle>'
                   % (px(r["top"]), py(r["rest"]), "6.5" if is_f else "4.5",
                      hue, "1" if is_f else "0.55", esc(r["team"]),
                      r["top"], r["rest"]))
        if is_f:
            out.append('<text x="%.1f" y="%.1f" fill="var(--fg)" font-size="11.5" '
                       'font-weight="600">%s</text>'
                       % (px(r["top"]) + 11, py(r["rest"]) + 4, ab))

    out.append('<text x="%.1f" y="%.1f" text-anchor="middle" fill="var(--muted)" '
               'font-size="10">goals from the 3 leading scorers</text>'
               % (PAD_L + pw / 2, H - 10))
    out.append('<text transform="translate(11,%.1f) rotate(-90)" '
               'text-anchor="middle" fill="var(--muted)" font-size="10">'
               'goals from the rest of the roster</text>' % (PAD_T + ph / 2))
    out.append("</svg>")
    return "\n".join(out)


def table(rows, n=8, focus="DET"):
    order = sorted(rows.items(), key=lambda kv: kv[1]["rest"])
    keep = order[:n]
    if focus not in [ab for ab, _ in keep]:
        keep.append((focus, rows[focus]))
    lines = ["| | Team | Top 3 | Rest of roster | Rest, rank of 32 | Points |",
             "|---|---|---|---|---|---|"]
    for ab, r in keep:
        mark = "**%d**" % r["rest_rank"] if ab == focus else str(r["rest_rank"])
        name = "**%s**" % r["team"] if ab == focus else r["team"]
        lines.append("| %s | %s | %d | %d | %s | %d |"
                     % (ab, name, r["top"], r["rest"], mark, r["points"]))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--team", default="DET")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    rows = split(load(force=a.refresh))
    if a.team not in rows:
        sys.stderr.write("unknown team %s\n" % a.team)
        return 2
    if a.json:
        sys.stdout.write(json.dumps(rows, indent=1) + "\n")
    elif a.table:
        sys.stdout.write(table(rows, focus=a.team) + "\n")
    else:
        sys.stdout.write(render(rows, focus=a.team) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
