#!/usr/bin/env python3
"""Emit an inline SVG: one bar per start for a pitcher, length = innings pitched.

Built for the case where a season ERA is a blend of two different jobs. A
swingman's headline number says nothing about what he does as a starter, and
the shape that matters is how far into a game he actually gets.

    python scripts/start_lengths.py 669387 > /tmp/chart.svg
    python scripts/start_lengths.py 669387 --table

Bars are colored by outcome: --chart-pos for a start of 3 earned runs or
fewer, --chart-neg otherwise. Those two hues were validated for colorblind
separation and contrast against both the light and dark surfaces. Everything
is derived from the MLB Stats API game log on every run, so a figure in a
published piece cannot drift from the numbers behind it.

Exit 2 if the player has no starts, because an empty chart is worse than none.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request

PAD_L, PAD_R = 96, 52
BAR_H, ROW_GAP = 17, 7
TOP, BOTTOM = 48, 30
ER_GOOD = 3          # a start of 3 earned or fewer reads as the good bucket


def fetch(player_id: int, season: int) -> tuple[str, list[dict], dict]:
    url = (f"https://statsapi.mlb.com/api/v1/people/{player_id}"
           f"/stats?stats=gameLog&group=pitching&season={season}")
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    if not data.get("stats"):
        raise SystemExit(f"no 2026 pitching game log for player {player_id}")

    splits = data["stats"][0]["splits"]
    name = splits[0]["player"]["fullName"] if splits else str(player_id)

    starts, relief = [], []
    for s in splits:
        st = s["stat"]
        row = {
            "date": s["date"],
            "opp": s["opponent"]["name"],
            "outs": int(st["outs"]),
            "ip": int(st["outs"]) / 3,
            "er": st["earnedRuns"],
            "h": st["hits"],
            "bb": st["baseOnBalls"],
            "k": st["strikeOuts"],
        }
        (starts if st["gamesStarted"] == 1 else relief).append(row)

    def agg(rows):
        if not rows:
            return None
        outs = sum(r["outs"] for r in rows)
        ip = outs / 3
        er = sum(r["er"] for r in rows)
        onbase = sum(r["h"] + r["bb"] for r in rows)
        return {"g": len(rows), "ip": ip, "er": er,
                "era": er * 9 / ip, "whip": onbase / ip}

    return name, starts, {"starter": agg(starts), "reliever": agg(relief)}


def ip_label(outs: int) -> str:
    return f"{outs // 3}.{outs % 3}"


def render(name: str, starts: list[dict], splits: dict) -> str:
    n = len(starts)
    width = 640
    height = TOP + n * (BAR_H + ROW_GAP) + BOTTOM
    max_outs = max(max(s["outs"] for s in starts), 21)   # always show 7 innings
    span = width - PAD_L - PAD_R

    def x_of(outs: int) -> float:
        return PAD_L + span * outs / max_outs

    st = splits["starter"]
    rel = splits["reliever"]
    sub = f'{st["g"]} starts, {st["era"]:.2f} ERA'
    if rel:
        sub += f'. Same season in relief: {rel["g"]} outings, {rel["era"]:.2f} ERA'

    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="sl-title" style="max-width:{width}px;height:auto;'
        f"font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,"
        f'sans-serif">',
        f'<title id="sl-title">Every 2026 start by {name}, bar length is innings '
        f'pitched. Longest is {ip_label(max(s["outs"] for s in starts))}. {sub}.</title>',
        f'<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        f'How far {name} gets when he starts</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">{sub}</text>',
    ]

    # inning gridlines at 3, 5, 6, 7
    for inn in (3, 5, 6, 7):
        if inn * 3 > max_outs:
            continue
        x = x_of(inn * 3)
        out.append(f'<line x1="{x:.1f}" y1="{TOP - 8:.1f}" x2="{x:.1f}" '
                   f'y2="{height - BOTTOM + 4:.1f}" stroke="var(--rule)" '
                   f'stroke-width="1" stroke-dasharray="4 4"/>')
        out.append(f'<text x="{x:.1f}" y="{height - BOTTOM + 18:.1f}" '
                   f'text-anchor="middle" fill="var(--muted)" font-size="10">'
                   f'{inn} inn</text>')

    for i, s in enumerate(starts):
        y = TOP + i * (BAR_H + ROW_GAP)
        color = "var(--chart-pos)" if s["er"] <= ER_GOOD else "var(--chart-neg)"
        out.append(f'<text x="{PAD_L - 10}" y="{y + BAR_H - 4:.1f}" '
                   f'text-anchor="end" fill="var(--muted)" font-size="10" '
                   f'font-variant-numeric="tabular-nums">{s["date"][5:]}</text>')
        out.append(f'<rect x="{PAD_L}" y="{y:.1f}" width="{x_of(s["outs"]) - PAD_L:.1f}" '
                   f'height="{BAR_H}" fill="{color}" opacity="0.85" rx="2">'
                   f'<title>{s["date"]} vs {s["opp"]}: {ip_label(s["outs"])} IP, '
                   f'{s["er"]} ER</title></rect>')
        out.append(f'<text x="{x_of(s["outs"]) + 8:.1f}" y="{y + BAR_H - 4:.1f}" '
                   f'fill="var(--fg)" font-size="10.5" '
                   f'font-variant-numeric="tabular-nums">'
                   f'{ip_label(s["outs"])} IP, {s["er"]} ER</text>')

    out.append("</svg>")
    return "\n".join(out)


def table(name: str, starts: list[dict], splits: dict) -> str:
    lines = ["| Date | Opponent | IP | H | BB | K | ER |",
             "|---|---|---|---|---|---|---|"]
    for s in starts:
        lines.append(f'| {s["date"]} | {s["opp"]} | {ip_label(s["outs"])} | '
                     f'{s["h"]} | {s["bb"]} | {s["k"]} | {s["er"]} |')
    st, rel = splits["starter"], splits["reliever"]
    lines.append("")
    lines.append("| Role | Outings | IP | ERA | WHIP |")
    lines.append("|---|---|---|---|---|")
    lines.append(f'| Starting | {st["g"]} | {st["ip"]:.1f} | {st["era"]:.2f} | '
                 f'{st["whip"]:.2f} |')
    if rel:
        lines.append(f'| Relieving | {rel["g"]} | {rel["ip"]:.1f} | '
                     f'{rel["era"]:.2f} | {rel["whip"]:.2f} |')
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("player_id", type=int)
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--table", action="store_true",
                    help="print the markdown table instead of the SVG")
    a = ap.parse_args()

    name, starts, splits = fetch(a.player_id, a.season)
    if not starts:
        print(f"{name} has no {a.season} starts; nothing to chart",
              file=sys.stderr)
        return 2

    print(table(name, starts, splits) if a.table
          else render(name, starts, splits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
