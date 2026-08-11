#!/usr/bin/env python3
"""How often does each team hold a lead it has after 7 innings?

Written 2026-08-11 to test a claim from r/motorcitykitties: that Detroit's whole
season is the blown save number, and that at 20 blown saves instead of 26 they
would be in first place.

A blown save is not the same as a loss, so counting them proves nothing on its
own. What matters is leads that turned into losses. This reconstructs the score
after 7 innings from every game's linescore, for all 30 teams, and reports how
many of those leads survived.

    python scripts/late_leads.py            # table plus the chart
    python scripts/late_leads.py --json     # raw numbers

Writes scripts/last_leads_chart.svg, which entries embed through the ```svg
fence. One request per team; results cached for an hour in logs/leads-cache.json
so a re-run costs nothing.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "logs" / "leads-cache.json"
CACHE_MINUTES = 60
END = "2026-08-11"


def get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def team_leads(tid: int) -> tuple[int, int, int, int]:
    """(led after 7, lost those, led after 8, lost those)"""
    sched = get(f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={tid}"
                f"&gameType=R&startDate=2026-03-01&endDate={END}&hydrate=linescore")
    led7 = lost7 = led8 = lost8 = 0
    for day in sched["dates"]:
        for g in day["games"]:
            if g["status"]["detailedState"] != "Final":
                continue
            innings = g.get("linescore", {}).get("innings", [])
            a, h = g["teams"]["away"], g["teams"]["home"]
            if not innings or "score" not in a or "score" not in h:
                continue
            home = h["team"]["id"] == tid
            won = (h["score"] if home else a["score"]) > (a["score"] if home else h["score"])

            def after(n: int) -> tuple[int, int]:
                us = them = 0
                for i, inn in enumerate(innings[:n]):
                    us += (inn.get("home", {}) if home else inn.get("away", {})).get("runs", 0) or 0
                    them += (inn.get("away", {}) if home else inn.get("home", {})).get("runs", 0) or 0
                return us, them

            u7, t7 = after(7)
            u8, t8 = after(8)
            if u7 > t7:
                led7 += 1
                lost7 += not won
            if u8 > t8:
                led8 += 1
                lost8 += not won
    return led7, lost7, led8, lost8


def collect() -> dict:
    if CACHE.exists() and (time.time() - CACHE.stat().st_mtime) / 60 < CACHE_MINUTES:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    teams = get("https://statsapi.mlb.com/api/v1/teams?sportId=1&season=2026")["teams"]
    out = {}
    for t in teams:
        led7, lost7, led8, lost8 = team_leads(t["id"])
        out[t["name"]] = {"led7": led7, "lost7": lost7, "led8": led8, "lost8": lost8}
        print(f"  {t['name']:24} {lost7:2} of {led7:2}", file=sys.stderr)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def chart(data: dict) -> str:
    """Held-lead rate, worst to best. Generated, never hand drawn."""
    rows = [(n, v["led7"], v["lost7"]) for n, v in data.items() if v["led7"] >= 35]
    rows.sort(key=lambda r: (r[1] - r[2]) / r[1])
    show = rows[:5] + rows[-3:]
    lg_led = sum(v["led7"] for v in data.values())
    lg_lost = sum(v["lost7"] for v in data.values())
    lg = (lg_led - lg_lost) / lg_led

    W, rowh, top = 640, 26, 54
    H = top + rowh * len(show) + 26
    lo, hi = 0.74, 1.0
    x0, x1 = 190, 600

    def x(p):
        return x0 + (p - lo) / (hi - lo) * (x1 - x0)

    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="lead-t" '
           f'style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,'
           f'-apple-system,\'Segoe UI\',Roboto,sans-serif">',
           '<title id="lead-t">Share of leads after 7 innings that each team held</title>',
           '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
           'How often a lead after 7 innings survives</text>',
           '<text x="0" y="34" fill="var(--muted)" font-size="11">'
           'Teams with at least 35 such leads. The line is the league rate.</text>']
    out.append(f'<line x1="{x(lg):.1f}" y1="{top - 6}" x2="{x(lg):.1f}" y2="{H - 20}" '
               f'stroke="var(--rule)" stroke-width="2"/>')
    for i, (name, led, lost) in enumerate(show):
        held = (led - lost) / led
        y = top + i * rowh
        colour = "var(--chart-neg)" if held < lg else "var(--chart-pos)"
        out.append(f'<text x="182" y="{y + 13}" text-anchor="end" fill="var(--fg)" '
                   f'font-size="12">{name}</text>')
        out.append(f'<rect x="{x0}" y="{y + 3}" width="{max(2, x(held) - x0):.1f}" height="15" '
                   f'rx="4" fill="{colour}"><title>{name}: held {led - lost} of {led}</title></rect>')
        out.append(f'<text x="{x(held) + 6:.1f}" y="{y + 15}" fill="var(--muted)" font-size="11" '
                   f'font-variant-numeric="tabular-nums">{held * 100:.1f}%</text>')
    out.append("</svg>")
    return "\n".join(out)


def main(argv):
    data = collect()
    if "--json" in argv:
        print(json.dumps(data, indent=1))
        return 0
    lg_led = sum(v["led7"] for v in data.values())
    lg_lost = sum(v["lost7"] for v in data.values())
    det = data["Detroit Tigers"]
    print(f"League: {lg_led} leads after 7, {lg_lost} lost, "
          f"{(lg_led - lg_lost) / lg_led * 100:.1f}% held")
    print(f"Detroit: {det['led7']} leads, {det['lost7']} lost, "
          f"{(det['led7'] - det['lost7']) / det['led7'] * 100:.1f}% held")
    print(f"Detroit after 8: {det['led8']} leads, {det['lost8']} lost")
    at_league = det["led7"] * (lg_lost / lg_led)
    print(f"At league rate Detroit loses {at_league:.1f} of those leads, "
          f"so {det['lost7'] - at_league:.1f} extra losses")
    svg = ROOT / "scripts" / "last_leads_chart.svg"
    svg.write_text(chart(data), encoding="utf-8")
    print(f"wrote {svg.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
