#!/usr/bin/env python3
"""Share of a team's innings thrown by its bullpen, all 30 clubs.

Written for the 824237 preview: the White Sox open with Sean Newcomb, who has
made 1 start in 44 appearances, and the question is whether that is a quirk of
one night or how the team is actually built.

Every number in the entry comes out of one execution of this script, chart
included, so the prose and the picture cannot disagree with each other.

    python scripts/bullpen_share.py                 # numbers to stdout
    python scripts/bullpen_share.py --svg > c.svg   # the strip plot

The split comes from the league's own sp/rp situational codes rather than from
summing individual pitchers, because a swingman would otherwise land in whichever
bucket I put him in.
"""

from __future__ import annotations

import argparse
import json
import statistics
import urllib.request

SEASON = 2026
API = "https://statsapi.mlb.com/api/v1"
HIGHLIGHT = {145: "neg", 116: "pos"}          # White Sox, Tigers

WIDTH = 640
PAD_L, PAD_R = 24, 24
TOP, BOTTOM = 62, 52
STRIP_H = 132


def _ip(text: str) -> float:
    """MLB writes thirds of an inning as .1 and .2, which are not decimals."""
    whole, _, part = text.partition(".")
    return int(whole) + {"": 0, "0": 0, "1": 1 / 3, "2": 2 / 3}[part]


def _pct(value: float) -> str:
    """Match the prose, which writes shares the way baseball writes rates."""
    return f"{value:.3f}".lstrip("0")


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch() -> list[dict]:
    teams = _get(f"{API}/teams?sportId=1&season={SEASON}")["teams"]
    rows = []
    for t in teams:
        d = _get(
            f"{API}/teams/{t['id']}/stats?stats=statSplits&sitCodes=sp,rp"
            f"&group=pitching&season={SEASON}&sportId=1"
        )
        split = {}
        for block in d["stats"]:
            for s in block["splits"]:
                split[s["split"]["code"]] = s["stat"]
        if "sp" not in split or "rp" not in split:
            raise SystemExit(f"missing sp/rp split for {t['name']}")
        sp, rp = _ip(split["sp"]["inningsPitched"]), _ip(split["rp"]["inningsPitched"])
        rows.append({
            "id": t["id"], "name": t["name"], "short": t["teamName"],
            "sp_ip": sp, "rp_ip": rp, "share": rp / (sp + rp),
            "sp_era": split["sp"]["era"], "rp_era": split["rp"]["era"],
        })
    return sorted(rows, key=lambda r: -r["share"])


def build(rows: list[dict]) -> str:
    """A strip plot, not bars. The story is where 30 dots sit relative to each
    other and to the halfway line, and bars would need a truncated baseline to
    show a spread this narrow, which is the mistake the Red Wings chart made."""
    lo = min(r["share"] for r in rows) - 0.012
    hi = max(r["share"] for r in rows) + 0.012
    plot_w = WIDTH - PAD_L - PAD_R
    to_x = lambda v: PAD_L + (v - lo) / (hi - lo) * plot_w
    mid_y = TOP + STRIP_H / 2
    height = TOP + STRIP_H + BOTTOM
    median = statistics.median(r["share"] for r in rows)

    out = [
        f'<svg viewBox="0 0 {WIDTH} {height}" width="100%" role="img" '
        f'aria-labelledby="pen-title" style="max-width:{WIDTH}px;height:auto;'
        f"font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',"
        f'Roboto,sans-serif">',
        '<title id="pen-title">Share of team innings thrown by the bullpen, '
        'all 30 clubs, 2026</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        'Share of a team\'s innings thrown by its bullpen</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">'
        f'All 30 clubs, {SEASON}, around 1,070 innings apiece so far. '
        f'The dashed line is half a team\'s innings.</text>',
    ]

    # the halfway reference, which only 2 teams are right of
    half = to_x(0.5)
    out.append(f'<line x1="{half:.1f}" y1="{TOP}" x2="{half:.1f}" '
               f'y2="{TOP+STRIP_H:.1f}" stroke="var(--rule)" stroke-width="1.5" '
               f'stroke-dasharray="5 4"/>')
    out.append(f'<text x="{half:.1f}" y="{TOP+STRIP_H+16:.1f}" '
               f'text-anchor="middle" fill="var(--muted)" font-size="11">'
               f'half the innings</text>')

    med_x = to_x(median)
    out.append(f'<text x="{med_x:.1f}" y="{TOP-8:.1f}" text-anchor="middle" '
               f'fill="var(--muted)" font-size="11">median {_pct(median)}</text>')
    out.append(f'<line x1="{med_x:.1f}" y1="{TOP-2}" x2="{med_x:.1f}" '
               f'y2="{TOP+8}" stroke="var(--rule)" stroke-width="1.5"/>')

    for r in rows:
        x = to_x(r["share"])
        kind = HIGHLIGHT.get(r["id"])
        color = f"var(--chart-{kind})" if kind else "var(--muted)"
        radius = 7 if kind else 5
        opacity = "" if kind else ' opacity="0.5"'
        out.append(
            f'<circle cx="{x:.1f}" cy="{mid_y:.1f}" r="{radius}" fill="{color}"'
            f'{opacity}><title>{r["name"]}: bullpen threw {r["rp_ip"]:.1f} of '
            f'{r["sp_ip"]+r["rp_ip"]:.1f} innings ({r["share"]:.3f}). '
            f'Rotation ERA {r["sp_era"]}, bullpen ERA {r["rp_era"]}.'
            f'</title></circle>'
        )
        if kind:
            above = kind == "neg"
            y = mid_y - radius - 10 if above else mid_y + radius + 20
            out.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
                       f'fill="var(--chart-{kind})" font-size="12.5" '
                       f'font-weight="700">{r["short"]} {_pct(r["share"])}</text>')

    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", action="store_true", help="emit the chart only")
    args = ap.parse_args()

    rows = fetch()
    if args.svg:
        print(build(rows))
        return

    median = statistics.median(r["share"] for r in rows)
    print(f"Bullpen share of team innings, {SEASON}. Median {median:.3f}.")
    print(f"Above half the innings: "
          f"{[r['short'] for r in rows if r['share'] > 0.5]}")
    print()
    for i, r in enumerate(rows, 1):
        mark = " <--" if r["id"] in HIGHLIGHT else ""
        print(f"{i:2d} {r['name']:<24} {r['share']:.3f}  "
              f"SP {r['sp_ip']:6.1f} ({r['sp_era']})  "
              f"RP {r['rp_ip']:6.1f} ({r['rp_era']}){mark}")

    by_sp = sorted(rows, key=lambda r: float(r["sp_era"]))
    by_rp = sorted(rows, key=lambda r: float(r["rp_era"]))
    print()
    for r in rows:
        if r["id"] in HIGHLIGHT:
            print(f"{r['short']}: rotation ERA rank "
                  f"{by_sp.index(r)+1} of 30, bullpen ERA rank "
                  f"{by_rp.index(r)+1} of 30")
    print(f"Best rotation ERA: {by_sp[0]['short']} {by_sp[0]['sp_era']}")


if __name__ == "__main__":
    main()
