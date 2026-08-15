#!/usr/bin/env python3
"""Every number behind the Pick 7 entry, derived in one run.

On 2026-08-08 this site published that Troy Melton's ERA was a mirage, on the
grounds that his BABIP was the lowest of any qualifying starter in baseball.
Six days and one start later the ERA is lower. This script exists to answer the
only honest follow-up question: has the thing that was supposed to correct
moved at all?

    python scripts/melton_mirage.py            # prose numbers
    python scripts/melton_mirage.py --chart    # the inline SVG

One execution derives the chart and the prose together, so the two cannot
disagree with each other. Colors are the site's --chart-pos / --chart-neg
tokens.
"""

from __future__ import annotations

import argparse
import json
import statistics
import urllib.request

import babip_chart

SEASON = 2026
MELTON = 675512
KAY = 641743
DET, CWS = 116, 145
API = "https://statsapi.mlb.com/api/v1"


def _ip(text: str) -> float:
    whole, _, part = text.partition(".")
    return int(whole) + {"": 0, "0": 0, "1": 1 / 3, "2": 2 / 3}[part]


def _avg(value: float) -> str:
    return f"{value:.3f}".lstrip("0")


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def game_log(pid: int) -> list[dict]:
    """Start-by-start, with BABIP and ERA accumulated as the season went."""
    url = (f"{API}/people/{pid}?hydrate=stats(group=[pitching],"
           f"type=[gameLog],season={SEASON})")
    splits = _get(url)["people"][0]["stats"][0]["splits"]

    rows, run = [], dict(h=0, hr=0, ab=0, k=0, sf=0, ip=0.0, er=0)
    for split in splits:
        s = split["stat"]
        run["h"] += s["hits"]
        run["hr"] += s["homeRuns"]
        run["ab"] += s["atBats"]
        run["k"] += s["strikeOuts"]
        run["sf"] += s["sacFlies"]
        run["ip"] += _ip(s["inningsPitched"])
        run["er"] += s["earnedRuns"]
        den = run["ab"] - run["k"] - run["hr"] + run["sf"]
        rows.append({
            "date": split["date"],
            "opp": split["opponent"]["name"],
            "ip": s["inningsPitched"],
            "er": s["earnedRuns"],
            "cum_ip": run["ip"],
            "cum_era": run["er"] * 9 / run["ip"],
            "cum_babip": (run["h"] - run["hr"]) / den if den else 0.0,
        })
    return rows


def league_fip_constant() -> tuple[float, float]:
    """Derived from this season's own totals rather than a remembered 3.10."""
    d = _get(f"{API}/teams/stats?stats=season&group=pitching"
             f"&season={SEASON}&sportId=1")
    ip = hr = bb = hbp = k = er = 0.0
    for split in d["stats"][0]["splits"]:
        s = split["stat"]
        ip += _ip(s["inningsPitched"])
        hr += s["homeRuns"]
        bb += s["baseOnBalls"]
        hbp += s["hitByPitch"]
        k += s["strikeOuts"]
        er += s["earnedRuns"]
    era = er * 9 / ip
    return era, era - (13 * hr + 3 * (bb + hbp) - 2 * k) / ip


def season_line(pid: int) -> dict:
    url = (f"{API}/people/{pid}?hydrate=stats(group=[pitching],"
           f"type=[season],season={SEASON})")
    p = _get(url)["people"][0]
    return p["stats"][0]["splits"][0]["stat"] | {"name": p["fullName"]}


def versus(pid: int, opp_id: int) -> dict:
    """This pitcher's starts against one club, from the game log."""
    url = (f"{API}/people/{pid}?hydrate=stats(group=[pitching],"
           f"type=[gameLog],season={SEASON})")
    splits = _get(url)["people"][0]["stats"][0]["splits"]
    ip = er = starts = 0.0
    dates = []
    for split in splits:
        if split["opponent"]["id"] != opp_id:
            continue
        ip += _ip(split["stat"]["inningsPitched"])
        er += split["stat"]["earnedRuns"]
        starts += 1
        dates.append(split["date"])
    return {"starts": int(starts), "ip": ip, "er": int(er),
            "era": er * 9 / ip if ip else None, "dates": dates}


def hbp_leaders() -> list[tuple[str, int, float]]:
    """Hit batsmen, over the same qualifying population as the BABIP chart."""
    d = _get(f"{API}/stats?stats=season&group=pitching&season={SEASON}"
             f"&sportId=1&limit=2000&playerPool=All")
    rows = []
    for split in d["stats"][0]["splits"]:
        s = split["stat"]
        ip = _ip(s["inningsPitched"])
        if s["gamesStarted"] < babip_chart.MIN_GS or ip < babip_chart.MIN_IP:
            continue
        rows.append((split["player"]["fullName"], s["hitByPitch"], ip))
    return sorted(rows, key=lambda r: -r[1])


def handedness_splits(team_id: int) -> dict:
    d = _get(f"{API}/teams/{team_id}/stats?stats=statSplits&sitCodes=vl,vr"
             f"&group=hitting&season={SEASON}&sportId=1")
    return {s["split"]["description"]: s["stat"] for s in d["stats"][0]["splits"]}


def build_chart(rows: list[dict], median: float, width: int = 640) -> str:
    """Cumulative BABIP after each start, against the median starter's line.

    A line rather than bars: the argument is that the value never travelled,
    and travel over time is what a line encodes. The median is drawn as the
    reference the correction was supposed to arrive at.
    """
    pad_l, pad_r, top, bottom = 46, 22, 52, 46
    plot_w = width - pad_l - pad_r
    height = 250
    plot_h = height - top - bottom

    lo, hi = 0.12, max(median, max(r["cum_babip"] for r in rows)) + 0.02
    to_x = lambda i: pad_l + (i / max(1, len(rows) - 1)) * plot_w
    to_y = lambda v: top + (hi - v) / (hi - lo) * plot_h

    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="mel-title" style="max-width:{width}px;height:auto;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
        f'Roboto,sans-serif">',
        '<title id="mel-title">Troy Melton\'s season-to-date batting average '
        'on balls in play after each of his 13 starts, against the median '
        'major league starter</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">Melton\'s season-to-date BABIP, after every '
        'start</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">The dashed '
        f'line is the median qualifying starter at {_avg(median)}. Thirteen '
        f'starts, and the gap has never closed.</text>',
    ]

    y_med = to_y(median)
    out.append(f'<line x1="{pad_l}" y1="{y_med:.1f}" x2="{width-pad_r}" '
               f'y2="{y_med:.1f}" stroke="var(--rule)" stroke-width="1.5" '
               f'stroke-dasharray="5 4"/>')
    out.append(f'<text x="{width-pad_r}" y="{y_med-7:.1f}" text-anchor="end" '
               f'fill="var(--muted)" font-size="11">median starter '
               f'{_avg(median)}</text>')

    for value in (0.15, 0.20, 0.25):
        y = to_y(value)
        out.append(f'<text x="{pad_l-8}" y="{y+4:.1f}" text-anchor="end" '
                   f'fill="var(--muted)" font-size="11" '
                   f'font-variant-numeric="tabular-nums">{_avg(value)}</text>')

    points = " ".join(f"{to_x(i):.1f},{to_y(r['cum_babip']):.1f}"
                      for i, r in enumerate(rows))
    out.append(f'<polyline points="{points}" fill="none" '
               f'stroke="var(--chart-pos)" stroke-width="2.5" '
               f'stroke-linejoin="round"/>')

    for i, r in enumerate(rows):
        out.append(
            f'<circle cx="{to_x(i):.1f}" cy="{to_y(r["cum_babip"]):.1f}" '
            f'r="3.5" fill="var(--chart-pos)"><title>After {r["date"]} vs '
            f'{r["opp"]}: {r["cum_ip"]:.1f} innings, BABIP '
            f'{_avg(r["cum_babip"])}, ERA {r["cum_era"]:.2f}</title></circle>')

    first, last = rows[0], rows[-1]
    out.append(f'<text x="{pad_l}" y="{height-bottom+20}" '
               f'fill="var(--muted)" font-size="11">{first["date"]}</text>')
    out.append(f'<text x="{width-pad_r}" y="{height-bottom+20}" '
               f'text-anchor="end" fill="var(--muted)" font-size="11">'
               f'{last["date"]}</text>')
    out.append(f'<text x="{to_x(len(rows)-1):.1f}" '
               f'y="{to_y(last["cum_babip"])+22:.1f}" text-anchor="end" '
               f'fill="var(--chart-pos)" font-size="12.5" font-weight="700">'
               f'{_avg(last["cum_babip"])}</text>')
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chart", action="store_true")
    args = ap.parse_args()

    rows = game_log(MELTON)
    field = babip_chart.fetch()
    median = statistics.median(r["babip"] for r in field)

    if args.chart:
        print(build_chart(rows, median))
        return

    print(f"Qualifying starters ({babip_chart.MIN_IP:.0f}+ IP, "
          f"{babip_chart.MIN_GS}+ GS): {len(field)}, median BABIP "
          f"{_avg(median)}")
    for rank, r in enumerate(field[:3], 1):
        print(f"  {rank}. {r['name']:<20} {_avg(r['babip'])}  "
              f"{r['ip']:.1f} IP  ERA {r['era']}")

    print("\nMelton, start by start")
    for r in rows:
        print(f"  {r['date']}  vs {r['opp'][:22]:<22} {r['ip']:>4} IP  "
              f"{r['er']} ER   cum {r['cum_ip']:5.1f} IP  "
              f"ERA {r['cum_era']:4.2f}  BABIP {_avg(r['cum_babip'])}")
    band = [r["cum_babip"] for r in rows[2:]]
    print(f"  range after 3 starts: {_avg(min(band))} to {_avg(max(band))}")

    lg_era, const = league_fip_constant()
    print(f"\nLeague ERA {lg_era:.2f}, derived FIP constant {const:.3f}")
    for pid in (MELTON, KAY):
        s = season_line(pid)
        ip = _ip(s["inningsPitched"])
        fip = (13 * s["homeRuns"] + 3 * (s["baseOnBalls"] + s["hitByPitch"])
               - 2 * s["strikeOuts"]) / ip + const
        print(f"  {s['name']:<14} {ip:5.1f} IP  ERA {s['era']:>5}  "
              f"FIP {fip:4.2f}  gap {fip - float(s['era']):+.2f}  "
              f"HR {s['homeRuns']} BB {s['baseOnBalls']} HBP {s['hitByPitch']} "
              f"K {s['strikeOuts']}  WHIP {s['whip']}  BAA {s['avg']}")

    print("\nMost hit batsmen, same qualifying population")
    for name, hbp, ip in hbp_leaders()[:5]:
        print(f"  {name:<20} {hbp:>3} HBP  {ip:.1f} IP")

    print("\nHead to head")
    print("  Melton vs Chicago:", versus(MELTON, CWS))
    print("  Kay vs Detroit:   ", versus(KAY, DET))

    print("\nHitting by opposing hand")
    for tid, name in ((DET, "Detroit"), (CWS, "Chicago")):
        for desc, s in handedness_splits(tid).items():
            print(f"  {name:<8} {desc:<12} {s['plateAppearances']:>5} PA  "
                  f"OPS {s['ops']}  AVG {s['avg']}  SLG {s['slg']}")


if __name__ == "__main__":
    main()
