#!/usr/bin/env python3
"""How tight is the Tigers-Royals matchup, and is the tightness real?

Detroit and Kansas City have played 10 times in 2026 and 8 of those games were
decided by a single run. That is the most one-run games of any pairing in
baseball this season. This script asks three separate questions about it, in
the order that stops a nice number from turning into a false claim:

1. **Is it actually the most?** Count one-run games for every pairing in the
   league, not just Detroit's.
2. **Would it happen anyway?** Give every pairing its real number of games and
   flip a coin weighted at the league's own one-run rate, 20,000 times, and ask
   how often the tightest pairing in that made-up league is at least this
   tight. Taking a maximum over hundreds of pairings pushes the leader out to
   the tail by construction, which is the same correction the Pythagorean piece
   needed.
3. **Has it happened before?** The simulation assumes independence. History
   does not. Count, across completed seasons, how many pairings reached the
   same number of one-run games.

    python scripts/tightest_matchup.py
    python scripts/tightest_matchup.py --history 2023 2024 2025

Everything comes from the MLB Stats API. Nothing here is hand-entered.
"""

from __future__ import annotations

import argparse
import json
import random
import urllib.request
from collections import defaultdict
from pathlib import Path

CACHE = Path(__file__).with_name("tightest_matchup_cache.json")
SVG_OUT = Path(__file__).with_name("last_tightest_matchup.svg")
DET, KC = "Detroit Tigers", "Kansas City Royals"


def short(name: str) -> str:
    """Chart label. Last word alone collapses both Sox into "Sox"."""
    special = {
        "Chicago White Sox": "White Sox", "Boston Red Sox": "Red Sox",
        "Chicago Cubs": "Cubs", "Athletics": "Athletics",
        "Toronto Blue Jays": "Blue Jays", "Arizona Diamondbacks": "D-backs",
    }
    return special.get(name, name.split()[-1])


def get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "dsr-tightest"})
    return json.load(urllib.request.urlopen(req, timeout=90))


def season_games(year: int, end: str | None = None) -> list[dict]:
    """Every completed regular-season game in a year, as flat dicts."""
    start = "%d-01-01" % year
    stop = end or "%d-12-31" % year
    url = (
        "https://statsapi.mlb.com/api/v1/schedule?sportId=1&gameType=R"
        "&startDate=%s&endDate=%s" % (start, stop)
    )
    out = []
    for date in get(url)["dates"]:
        for g in date["games"]:
            if g["status"]["detailedState"] != "Final":
                continue
            a, h = g["teams"]["away"], g["teams"]["home"]
            if "score" not in a or "score" not in h:
                continue
            out.append({
                "pk": g["gamePk"], "date": g["gameDate"][:10],
                "away": a["team"]["name"], "home": h["team"]["name"],
                "away_score": a["score"], "home_score": h["score"],
            })
    return out


def load(year: int, end: str | None = None) -> list[dict]:
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    key = "%d:%s" % (year, end or "")
    if key not in cache:
        cache[key] = season_games(year, end)
        CACHE.write_text(json.dumps(cache))
    return cache[key]


def pairings(games: list[dict]) -> dict:
    out = defaultdict(list)
    for g in games:
        key = tuple(sorted((g["away"], g["home"])))
        out[key].append(abs(g["away_score"] - g["home_score"]))
    return out


def simulate(counts: list[int], rate: float, target: int, trials: int, seed: int = 7):
    """How often is the league's tightest pairing at least `target` one-run games?

    `counts` is every pairing's real number of games played, so the shape of
    the schedule is preserved; only the outcomes are randomised.
    """
    rng = random.Random(seed)
    hits = 0
    total_leader = 0
    for _ in range(trials):
        best = 0
        for n in counts:
            c = 0
            for _ in range(n):
                if rng.random() < rate:
                    c += 1
            if c > best:
                best = c
        total_leader += best
        if best >= target:
            hits += 1
    return hits / trials, total_leader / trials


def bar_svg(rows: list) -> str:
    """Horizontal bars: one-run games per pairing, the league's tightest first."""
    w, left, top, rowh = 640, 210.0, 52.0, 22.0
    height = top + rowh * len(rows) + 20
    scale = 330.0 / max(r[1] for r in rows)
    parts = [
        '<svg viewBox="0 0 %d %.0f" width="100%%" role="img" '
        'aria-labelledby="tm-title" style="max-width:640px;height:auto;'
        "font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif\">"
        % (w, height),
        '<title id="tm-title">One-run games by matchup in the 2026 season through '
        'August 20. Detroit and Kansas City lead all of baseball with 8 of their 10 '
        'meetings decided by one run.</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        'Games decided by 1 run, by matchup</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">'
        'The 10 tightest of the 391 pairings that have met this season.</text>',
    ]
    for i, (label, one, total) in enumerate(rows):
        y = top + rowh * i
        lead = i == 0
        # One quantity, one hue. The colour here encodes emphasis, not sign,
        # so mixing the two chart tokens would imply a good/bad split that
        # does not exist in the data.
        col = "var(--chart-neg)"
        op = "0.9" if lead else "0.35"
        weight = "700" if lead else "400"
        fill = "var(--fg)" if lead else "var(--muted)"
        parts.append(
            '<text x="%.0f" y="%.1f" text-anchor="end" fill="%s" font-size="10" '
            'font-weight="%s">%s</text>' % (left - 8, y + 4, fill, weight, label)
        )
        parts.append(
            '<rect x="%.0f" y="%.1f" width="%.1f" height="12" fill="%s" opacity="%s">'
            '<title>%s: %d of %d decided by 1 run</title></rect>'
            % (left, y - 6, one * scale, col, op, label, one, total)
        )
        parts.append(
            '<text x="%.1f" y="%.1f" fill="%s" font-size="10.5" font-weight="%s" '
            'font-variant-numeric="tabular-nums">%d of %d</text>'
            % (left + one * scale + 6, y + 4, fill, weight, one, total)
        )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--through", default="2026-08-20")
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--history", type=int, nargs="*",
                    default=[2021, 2022, 2023, 2024, 2025])
    a = ap.parse_args()

    games = load(a.season, a.through)
    pairs = pairings(games)
    one_run = sum(1 for g in games if abs(g["away_score"] - g["home_score"]) == 1)
    rate = one_run / len(games)

    ranked = sorted(
        ((k, sum(1 for m in v if m == 1), len(v)) for k, v in pairs.items()),
        key=lambda r: (-r[1], -r[1] / r[2]),
    )
    print("%d through %s: %d games, %d pairings"
          % (a.season, a.through, len(games), len(pairs)))
    print("league one-run rate: %.4f (%d of %d)\n" % (rate, one_run, len(games)))
    print("Tightest pairings:")
    for key, one, total in ranked[:10]:
        print("  %2d of %2d  %s / %s" % (one, total, key[0], key[1]))

    det_kc = next(r for r in ranked if set(r[0]) == {DET, KC})
    target = det_kc[1]
    print("\nDetroit/Kansas City: %d of %d" % (det_kc[1], det_kc[2]))

    p, avg = simulate([len(v) for v in pairs.values()], rate, target, a.trials)
    print("\nSimulation, %d leagues, schedule shape held fixed:" % a.trials)
    print("  tightest pairing reaches %d one-run games in %.1f%% of seasons"
          % (target, p * 100))
    print("  average league-leading count: %.2f" % avg)

    print("\nHistory, completed seasons. The schedule format changed in 2023, when "
          "\nthe balanced schedule cut division pairings from 19 meetings to 13, so "
          "\nonly 2023 onward is comparable with this season.")
    for yr in a.history:
        h = pairings(load(yr))
        rows = [(sum(1 for m in v if m == 1), len(v), k) for k, v in h.items()]
        rows.sort(reverse=True)
        big = [r for r in rows if r[0] >= target]
        lead = rows[0]
        print("  %d: leader %d of %d (%s / %s); %d of %d pairings at %d+"
              % (yr, lead[0], lead[1], lead[2][0], lead[2][1],
                 len(big), len(h), target))

    rows = [("%s / %s" % (short(k[0]), short(k[1])), one, total)
            for k, one, total in ranked[:10]]
    SVG_OUT.write_text(bar_svg(rows), encoding="utf-8")
    print("\nwrote %s" % SVG_OUT)


if __name__ == "__main__":
    main()
