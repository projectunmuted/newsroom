#!/usr/bin/env python3
"""Put one starter's home/road ERA gap next to every other starter's.

A pitcher who is a run and a half worse at home than on the road looks like a
finding until you notice how wide that distribution is. Half a season of home
starts is 60-odd innings, and 60 innings is not enough to separate a real
platoon-of-venue effect from noise. So the only honest way to report a gap is
to report where it sits in the league's own spread of gaps.

    python scripts/venue_split.py 702070 > /tmp/chart.svg
    python scripts/venue_split.py 702070 --table
    python scripts/venue_split.py 702070 --starts        # the target's start log

Gap is home ERA minus road ERA, so a positive number means worse at home.
The population is every pitcher with at least --min-ip innings and --min-gs
starts this season, fetched once and cached in venue_split_cache.json; pass
--refresh to re-pull. Everything is derived from the MLB Stats API on every
run, so a figure in a published piece cannot drift from the numbers behind it.

Two different populations, on purpose. The gap and the ranking come from the
splits endpoint, which counts **every appearance**, so the league is compared
like for like. `--starts` filters to gamesStarted == 1, so the two totals will
disagree for anyone who has relieved. Noah Cameron threw 7 innings behind an
opener on 2026-07-24 and that game is in his road split and not in his start
log, which is correct in both places and confusing in neither if you know it.

Exit 2 if the target has no starts, or if any population fetch failed, because
a percentile computed against a partial league is worse than no percentile.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://statsapi.mlb.com/api/v1"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "venue_split_cache.json")

PAD_L, PAD_R = 20, 20
TOP, BOTTOM = 60, 52
PLOT_H = 190
DOT_R = 4.0


class NoStarts(Exception):
    pass


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def qualified(season, min_ip, min_gs):
    url = ("%s/stats?stats=season&group=pitching&season=%d&sportId=1"
           "&playerPool=All&limit=1000&gameType=R" % (API, season))
    out = []
    for s in get(url)["stats"][0]["splits"]:
        st = s["stat"]
        if float(st["inningsPitched"]) >= min_ip and int(st["gamesStarted"]) >= min_gs:
            out.append((s["player"]["id"], s["player"]["fullName"]))
    return out


def venue(pid, season):
    """(home_era, road_era, home_ip, road_ip) or None if a side is empty."""
    url = ("%s/people/%d/stats?stats=statSplits&sitCodes=h,a&group=pitching"
           "&season=%d" % (API, pid, season))
    d = get(url)
    if not d.get("stats"):
        return None
    got = {}
    for st in d["stats"]:
        for sp in st["splits"]:
            desc = sp.get("split", {}).get("description", "")
            key = "home" if desc.startswith("Home") else "road"
            got[key] = (float(sp["stat"]["era"]), float(sp["stat"]["inningsPitched"]))
    if "home" not in got or "road" not in got:
        return None
    return got["home"][0], got["road"][0], got["home"][1], got["road"][1]


def population(season, min_ip, min_gs, refresh):
    key = "%d-%g-%d" % (season, min_ip, min_gs)
    cache = {}
    if os.path.exists(CACHE) and not refresh:
        with open(CACHE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        if key in cache:
            return cache[key], 0

    rows, failed = [], 0
    for pid, name in qualified(season, min_ip, min_gs):
        try:
            v = venue(pid, season)
        except (urllib.error.URLError, ValueError, KeyError):
            failed += 1
            continue
        if v is None:
            continue
        rows.append({"id": pid, "name": name, "home": v[0], "road": v[1],
                     "home_ip": v[2], "road_ip": v[3], "gap": v[0] - v[1]})
    cache[key] = rows
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f)
    return rows, failed


def start_log(pid, season):
    url = ("%s/people/%d/stats?stats=gameLog&group=pitching&season=%d"
           % (API, pid, season))
    d = get(url)
    if not d.get("stats") or not d["stats"][0]["splits"]:
        raise NoStarts()
    out = []
    for s in d["stats"][0]["splits"]:
        st = s["stat"]
        if st["gamesStarted"] != 1:
            continue
        out.append({"date": s["date"], "opp": s["opponent"]["name"],
                    "home": bool(s.get("isHome")), "er": int(st["earnedRuns"]),
                    "outs": int(st["outs"]), "h": int(st["hits"]),
                    "k": int(st["strikeOuts"]), "bb": int(st["baseOnBalls"])})
    if not out:
        raise NoStarts()
    return out


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rank_of(rows, pid):
    order = sorted(rows, key=lambda r: -r["gap"])
    for i, r in enumerate(order, 1):
        if r["id"] == pid:
            return i, len(order), r
    return None, len(order), None


def render(rows, pid, width=640):
    rank, n, me = rank_of(rows, pid)
    gaps = sorted(r["gap"] for r in rows)
    lo, hi = gaps[0], gaps[-1]
    span = max(abs(lo), abs(hi))
    span = (int(span) + 1) if span == int(span) else (int(span) + 1)
    lo, hi = -span, span
    plot_w = width - PAD_L - PAD_R
    height = TOP + PLOT_H + BOTTOM
    axis_y = TOP + PLOT_H

    def x_of(g):
        return PAD_L + ((g - lo) / float(hi - lo)) * plot_w

    alt = ("All %d starters with enough innings this season, one dot each, "
           "placed by home ERA minus road ERA. Positive is worse at home. "
           "The league runs from %.2f to %.2f. %s sits at %+.2f, %d of %d."
           % (n, gaps[0], gaps[-1], me["name"], me["gap"], rank, n))

    out = [
        '<svg viewBox="0 0 %d %d" width="100%%" role="img" '
        'aria-labelledby="vs-title" style="max-width:%dpx;height:auto;'
        "font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,"
        'sans-serif">' % (width, height, width),
        '<title id="vs-title">%s</title>' % esc(alt),
        '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        'Home ERA minus road ERA, every qualified starter in baseball</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">'
        'One dot per pitcher. Right of the line is worse at home. %d starters, '
        '2026</text>' % n,
    ]

    for g in range(lo, hi + 1):
        gx = x_of(g)
        heavy = (g == 0)
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                   'stroke="var(--%s)" stroke-width="%s"%s/>'
                   % (gx, TOP - 12, gx, axis_y,
                      "fg" if heavy else "rule", "1.5" if heavy else "1",
                      "" if heavy else ' stroke-dasharray="3 5"'))
        out.append('<text x="%.1f" y="%.1f" text-anchor="middle" '
                   'fill="var(--muted)" font-size="10">%+d</text>'
                   % (gx, axis_y + 15, g))
    out.append('<text x="%.1f" y="%.1f" text-anchor="middle" '
               'fill="var(--muted)" font-size="10">home ERA minus road ERA'
               '</text>' % (PAD_L + plot_w / 2, axis_y + 31))

    # stack dots that land in the same 0.1-wide bucket
    stack = {}
    marked = None
    for r in sorted(rows, key=lambda r: r["gap"]):
        b = round(r["gap"], 1)
        k = stack.get(b, 0)
        stack[b] = k + 1
        cx, cy = x_of(r["gap"]), axis_y - 10 - k * (DOT_R * 2 + 1.5)
        if r["id"] == pid:
            marked = (cx, cy, r)
            continue
        hue = "--chart-neg" if r["gap"] > 0 else "--chart-pos"
        out.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="var(%s)" '
                   'opacity="0.45"><title>%s: %.2f home, %.2f road</title>'
                   '</circle>' % (cx, cy, DOT_R, hue, esc(r["name"]),
                                  r["home"], r["road"]))

    if marked:
        cx, cy, r = marked
        out.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="var(--chart-neg)"'
                   '><title>%s: %.2f home, %.2f road</title></circle>'
                   % (cx, cy, DOT_R + 2.5, esc(r["name"]), r["home"], r["road"]))
        out.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="none" '
                   'stroke="var(--fg)" stroke-width="1.5"/>'
                   % (cx, cy, DOT_R + 6))
        ty = max(cy - 22, TOP - 2)
        anchor, tx = ("end", cx - 12) if cx > PAD_L + plot_w * 0.6 else ("start", cx + 12)
        out.append('<text x="%.1f" y="%.1f" text-anchor="%s" fill="var(--fg)" '
                   'font-size="11" font-weight="600">%s, %+.2f (%d of %d)</text>'
                   % (tx, ty, anchor, esc(r["name"]), r["gap"], rank, n))

    out.append("</svg>")
    return "\n".join(out)


def table(rows, pid, top=6):
    rank, n, me = rank_of(rows, pid)
    order = sorted(rows, key=lambda r: -r["gap"])[:top]
    if me and me not in order:
        order.append(me)
    lines = ["| Starter | ERA at home | ERA on the road | Gap | Home IP |",
             "|---|---|---|---|---|"]
    for r in order:
        star = " **(%d of %d)**" % (rank, n) if r["id"] == pid else ""
        lines.append("| %s%s | %.2f | %.2f | %+.2f | %.1f |"
                     % (r["name"], star, r["home"], r["road"], r["gap"],
                        r["home_ip"]))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Home/road ERA gap for one starter, in league context.")
    ap.add_argument("player_id", type=int)
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--min-ip", type=float, default=100.0)
    ap.add_argument("--min-gs", type=int, default=15)
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--starts", action="store_true",
                    help="print the target's start log split by venue")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()

    if a.starts:
        try:
            log = start_log(a.player_id, a.season)
        except NoStarts:
            sys.stderr.write("player %d has no %d starts\n"
                             % (a.player_id, a.season))
            return 2
        for where in (True, False):
            side = [s for s in log if s["home"] == where]
            outs = sum(s["outs"] for s in side)
            er = sum(s["er"] for s in side)
            print("%s: %d starts, %d.%d IP, %d ER, %.2f"
                  % ("HOME" if where else "ROAD", len(side), outs // 3,
                     outs % 3, er, (er * 27.0 / outs) if outs else 0))
            for s in side:
                print("   %s  %-24s %d.%d IP  %d ER  %d H  %d K  %d BB"
                      % (s["date"], s["opp"], s["outs"] // 3, s["outs"] % 3,
                         s["er"], s["h"], s["k"], s["bb"]))
        return 0

    rows, failed = population(a.season, a.min_ip, a.min_gs, a.refresh)
    if failed:
        sys.stderr.write("%d population fetches failed; percentile would be "
                         "computed against a partial league\n" % failed)
        return 2
    if not any(r["id"] == a.player_id for r in rows):
        sys.stderr.write("player %d is not in the %g IP / %d GS population\n"
                         % (a.player_id, a.min_ip, a.min_gs))
        return 2
    sys.stdout.write((table(rows, a.player_id) if a.table
                      else render(rows, a.player_id)) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
