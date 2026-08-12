#!/usr/bin/env python3
"""Which starters do runners simply not go on?

Written 2026-08-13 for the Thursday finale, Parker Messick against Keider
Montero, and as the committed version of a number the 08-12 entry quoted from an
ad hoc query: "Messick is 3rd and Montero 2nd of 57 qualified starters at
suppressing steal attempts." That figure was correct and it lived nowhere, which
means the next cycle to want it would have had to re-derive it by hand and could
have got a different answer. It lives here now.

The measure is **steal attempts allowed per 9 innings**, not stolen bases and
not the rate runners are caught:

  - Stolen bases alone punish a pitcher for a catcher who cannot throw, and
    reward one who never lets a runner reach.
  - Caught-stealing rate is mostly the catcher. The decision to *go* is mostly
    the pitcher: his time to the plate, his pickoff, his handedness.

So attempts per 9 is the closest free proxy for "do runners even try against
this man", which is the question a preview actually wants answered.

The pool is `playerPool=qualified`, which is the league's own innings threshold,
so nothing here depends on a cutoff I chose. It returns 58 starters today.

    python scripts/starter_running.py            # table plus the chart
    python scripts/starter_running.py --json     # raw numbers

Writes scripts/last_starter_running.svg, embedded through the ```svg fence.
Cached for an hour in logs/starter-running-cache.json so a re-run is free.
"""

from __future__ import annotations

import json
import statistics
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "logs" / "starter-running-cache.json"
CACHE_MINUTES = 60
SEASON = 2026
API = "https://statsapi.mlb.com/api/v1"

# The two starters this was written for, plus last night's Cleveland starter as
# the contrast: the entry's whole point is that the same series produced
# opposite answers on consecutive days.
HIGHLIGHT = {
    "Keider Montero": "pos",
    "Parker Messick": "pos",
    "Framber Valdez": "neg",
}


def get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def innings(ip: str) -> float:
    """MLB writes innings as 136.2 meaning 136 and two thirds, not 136.2."""
    whole, _, thirds = ip.partition(".")
    return int(whole) + int(thirds or 0) / 3


def collect(refresh: bool = False) -> dict:
    if CACHE.exists() and not refresh:
        cached = json.loads(CACHE.read_text(encoding="utf-8"))
        if time.time() - cached.get("read_at_epoch", 0) < CACHE_MINUTES * 60:
            return cached

    url = (f"{API}/stats?stats=season&group=pitching&season={SEASON}&gameType=R"
           f"&sportIds=1&playerPool=qualified&limit=500")
    rows = []
    for block in get(url)["stats"]:
        for split in block["splits"]:
            st = split["stat"]
            ip = innings(st["inningsPitched"])
            sb = int(st.get("stolenBases", 0) or 0)
            cs = int(st.get("caughtStealing", 0) or 0)
            rows.append({
                "name": split["player"]["fullName"],
                "id": split["player"]["id"],
                "team": split["team"]["name"],
                # Both forms on purpose. `ip` is real thirds and is what the
                # arithmetic uses; `ip_text` is the league's own notation, where
                # 136.2 means 136 and two thirds. A prose table written off the
                # decimal would print innings totals no box score agrees with.
                "ip": round(ip, 1),
                "ip_text": st["inningsPitched"],
                "starts": int(st.get("gamesStarted", 0) or 0),
                "era": st.get("era"),
                "sb": sb,
                "cs": cs,
                "attempts": sb + cs,
                "per9": round((sb + cs) / ip * 9, 4) if ip else 0.0,
            })

    rows.sort(key=lambda r: (r["per9"], r["attempts"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    data = {
        "read_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "read_at_epoch": time.time(),
        "season": SEASON,
        "n": len(rows),
        "median_per9": round(statistics.median(r["per9"] for r in rows), 4),
        "mean_per9": round(statistics.fmean(r["per9"] for r in rows), 4),
        "total_attempts": sum(r["attempts"] for r in rows),
        "total_ip": round(sum(r["ip"] for r in rows), 1),
        "starters": rows,
    }
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(data, indent=1), encoding="utf-8")
    return data


def chart(data: dict) -> str:
    """A strip plot, one dot per qualified starter, on a full axis from zero.

    Deliberately not a bar chart of the top ten. The claim is that the two men
    starting this game sit at the empty end of a distribution whose bulk is
    somewhere else entirely, and only the whole distribution can show that. A
    top-ten bar chart would put Montero and Messick beside their neighbours and
    make the gap look ordinary, which is the opposite of the argument.
    """
    rows = data["starters"]
    xs = [r["per9"] for r in rows]
    xhi = max(xs) * 1.04
    W = 640
    l, r, t, b = 16, 16, 74, 54
    step = 11.0

    def X(v):
        return l + v / xhi * (W - l - r)

    # Stack overlapping dots vertically so the pile-up is visible rather than
    # hidden underneath itself. Anything within 6px of an occupied slot moves
    # up one row. Placement happens before the canvas is sized, because the
    # height that fits is whatever the stacking turned out to need: a fixed
    # height either clips the tallest column or leaves a band of dead space
    # above it, and the dead-space version is what shipped first.
    slots: list[float] = []
    placed = []
    for row in rows:
        if row["name"] in HIGHLIGHT:
            continue
        x = X(row["per9"])
        lane = 0
        while lane < len(slots) and abs(slots[lane] - x) < 6:
            lane += 1
        if lane == len(slots):
            slots.append(x)
        else:
            slots[lane] = x
        placed.append((row, x, lane))

    # The marked starters get a reserved row each, on top, leftmost highest.
    # The vertical axis carries no meaning here, it only spreads ties apart, so
    # lifting them out costs nothing and it is the only way the labels fit
    # without landing on somebody else's dot. Two earlier versions failed here:
    # stacking them with everyone put the Messick label on the Montero dot, and
    # sharing one reserved row put the two labels on top of each other, because
    # Montero and Messick are 18px apart on this axis and their names are not.
    top = len(slots)
    marked = sorted((r for r in rows if r["name"] in HIGHLIGHT),
                    key=lambda r: -r["per9"])
    placed += [(row, X(row["per9"]), top + i) for i, row in enumerate(marked)]

    lanes = max(p[2] for p in placed) + 1
    H = int(t + (lanes - 1) * step + 12 + b)
    lane_b = H - b

    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
           f'aria-labelledby="sr-t" style="max-width:640px;height:auto;'
           f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
           f'Roboto,sans-serif">',
           f'<title id="sr-t">Steal attempts allowed per 9 innings by each of the '
           f'{data["n"]} qualified starting pitchers in 2026</title>',
           '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
           'Nobody runs on these two</text>',
           f'<text x="0" y="34" fill="var(--muted)" font-size="11">'
           f'Each dot is 1 of the {data["n"]} qualified starters. Left means runners '
           f'almost never try.</text>',
           f'<text x="0" y="50" fill="var(--muted)" font-size="11">'
           f'Steal attempts allowed per 9 innings.</text>']

    med = data["median_per9"]
    out.append(f'<line x1="{X(med):.1f}" y1="{t - 4}" x2="{X(med):.1f}" '
               f'y2="{lane_b + 8}" stroke="var(--rule)" stroke-width="1"/>')
    out.append(f'<text x="{X(med):.1f}" y="{t - 10}" text-anchor="middle" '
               f'fill="var(--muted)" font-size="10">median {med:.2f}</text>')

    for row, x, lane in placed:
        kind = HIGHLIGHT.get(row["name"])
        colour = {"pos": "var(--chart-pos)", "neg": "var(--chart-neg)"}.get(
            kind, "var(--rule)")
        y = lane_b - lane * step
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if kind else 3}" '
                   f'fill="{colour}"><title>{row["name"]}, {row["team"]}: '
                   f'{row["attempts"]} attempts in {row["ip"]} innings, '
                   f'{row["per9"]:.2f} per 9, rank {row["rank"]} of {data["n"]}'
                   f'</title></circle>')

    # Labels for the marked starters, drawn last so nothing sits on top of them.
    for row, x, lane in placed:
        if row["name"] not in HIGHLIGHT:
            continue
        y = lane_b - lane * step
        surname = row["name"].split()[-1]
        # Beside the dot, not above it. Above put the Messick label straight
        # through the Montero dot, because the two sit 18px apart on this axis.
        out.append(f'<text x="{x + 9:.1f}" y="{y + 4:.1f}" '
                   f'fill="var(--fg)" font-size="11" font-weight="600">'
                   f'{surname}</text>')

    for v in (0, med, xhi):
        out.append(f'<text x="{X(v):.1f}" y="{H - 22}" text-anchor="middle" '
                   f'fill="var(--muted)" font-size="10" '
                   f'font-variant-numeric="tabular-nums">{v:.1f}</text>')
    out.append(f'<text x="{W / 2:.0f}" y="{H - 6}" text-anchor="middle" '
               f'fill="var(--muted)" font-size="11">'
               f'Steal attempts allowed per 9 innings</text>')
    out.append("</svg>")
    return "\n".join(out)


def main(argv):
    data = collect(refresh="--refresh" in argv)
    if "--json" in argv:
        print(json.dumps(data, indent=1))
        return 0

    rows = data["starters"]
    print(f"{data['n']} qualified starters, {SEASON}, read {data['read_at']}")
    print(f"league median {data['median_per9']:.3f} attempts allowed per 9, "
          f"mean {data['mean_per9']:.3f}")
    print(f"pool totals: {data['total_attempts']} attempts in {data['total_ip']} "
          f"innings\n")

    print("Hardest to run on:")
    for r in rows[:8]:
        print(f"  {r['rank']:2}. {r['name'][:22]:22} {r['team'][:20]:20} "
              f"{r['attempts']:3} att / {r['ip']:6} IP = {r['per9']:.3f} per 9")
    print("Easiest:")
    for r in rows[-3:]:
        print(f"  {r['rank']:2}. {r['name'][:22]:22} {r['team'][:20]:20} "
              f"{r['attempts']:3} att / {r['ip']:6} IP = {r['per9']:.3f} per 9")

    print("\nMarked in the chart:")
    for r in rows:
        if r["name"] in HIGHLIGHT:
            print(f"  {r['name']:20} rank {r['rank']:2} of {data['n']}  "
                  f"{r['sb']} SB / {r['cs']} CS in {r['ip']} IP  "
                  f"{r['per9']:.3f} per 9  ERA {r['era']}")

    marked = [r for r in rows if r["name"] in ("Keider Montero", "Parker Messick")]
    if len(marked) == 2:
        ip = sum(r["ip"] for r in marked)
        att = sum(r["attempts"] for r in marked)
        print(f"\nMessick + Montero: {att} attempts in {ip:.1f} innings. "
              f"A median pair over the same innings: "
              f"{ip / 9 * data['median_per9']:.1f} attempts.")

    out = ROOT / "scripts" / "last_starter_running.svg"
    out.write_text(chart(data), encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
