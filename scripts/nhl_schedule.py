#!/usr/bin/env python3
"""What the 2026-27 schedule asks of the Red Wings, before a puck is dropped.

Written 2026-08-11. The Wings do not play until October 2 and had zero pieces on
the site, so this is the offseason shape the calendar calls for: pull the whole
84 game schedule for all 32 teams, score each one for opponent quality, rest and
travel, and see where Detroit lands.

Everything is derived here in one run so a chart and a paragraph cannot disagree
with each other. Sources, both free and keyless:

    api-web.nhle.com/v1/club-schedule-season/<ABBREV>/20262027
    api-web.nhle.com/v1/standings/2026-04-17   (final 2025-26 standings)

    python scripts/nhl_schedule.py            # the table plus the chart
    python scripts/nhl_schedule.py --json     # every number, raw

Writes scripts/last_nhl_sos_chart.svg for the ```svg fence. 33 requests, cached
in logs/nhl-schedule-cache.json for a day, so a re-run is free.

Arena coordinates below are the arena's own location to about a block, entered by
hand because the NHL API does not publish them. Travel is great-circle miles
between consecutive venues, which is the standard way this gets counted and is
not the same as flight miles.
"""

from __future__ import annotations

import json
import math
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "logs" / "nhl-schedule-cache.json"
CACHE_HOURS = 24
SEASON = "20262027"
PRIOR_STANDINGS = "2026-04-17"

ARENAS = {
    "ANA": (33.8078, -117.8766), "BOS": (42.3662, -71.0621),
    "BUF": (42.8750, -78.8764), "CGY": (51.0374, -114.0519),
    "CAR": (35.8032, -78.7219), "CHI": (41.8807, -87.6742),
    "COL": (39.7487, -105.0077), "CBJ": (39.9694, -83.0060),
    "DAL": (32.7905, -96.8104), "DET": (42.3250, -83.0522),
    "EDM": (53.5470, -113.4976), "FLA": (26.1585, -80.3255),
    "LAK": (34.0430, -118.2673), "MIN": (44.9447, -93.1013),
    "MTL": (45.4961, -73.5693), "NSH": (36.1593, -86.7785),
    "NJD": (40.7336, -74.1711), "NYI": (40.7229, -73.5904),
    "NYR": (40.7505, -73.9934), "OTT": (45.2969, -75.9271),
    "PHI": (39.9012, -75.1720), "PIT": (40.4395, -79.9893),
    "SJS": (37.3328, -121.9012), "SEA": (47.6221, -122.3540),
    "STL": (38.6268, -90.2027), "TBL": (27.9427, -82.4518),
    "TOR": (43.6435, -79.3791), "UTA": (40.7683, -111.9011),
    "VGK": (36.1029, -115.1784), "VAN": (49.2778, -123.1088),
    "WSH": (38.8981, -77.0209), "WPG": (49.8927, -97.1436),
}


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "detroitsportsreporter/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def miles(a: str, b: str) -> float:
    """Great-circle distance between two arenas."""
    (la1, lo1), (la2, lo2) = ARENAS[a], ARENAS[b]
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 3958.8 * math.asin(math.sqrt(h))


def collect() -> dict:
    """Raw schedules and standings for all 32 teams. Cached."""
    if CACHE.exists() and (time.time() - CACHE.stat().st_mtime) / 3600 < CACHE_HOURS:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    standings = get(f"https://api-web.nhle.com/v1/standings/{PRIOR_STANDINGS}")["standings"]
    prior = {}
    for t in standings:
        ab = t["teamAbbrev"]["default"]
        prior[ab] = {
            "name": t["teamName"]["default"],
            "points": t["points"],
            "gf": t["goalFor"],
            "ga": t["goalAgainst"],
            "wins": t["wins"], "losses": t["losses"], "ot": t["otLosses"],
            # z/y/x/p all clinched a berth; e was eliminated.
            "playoffs": t.get("clinchIndicator", "e") != "e",
            "conf": t["conferenceName"],
            "div": t["divisionAbbrev"],
            "wildcard": t.get("wildcardSequence"),
        }
    scheds = {}
    for ab in sorted(prior):
        url = f"https://api-web.nhle.com/v1/club-schedule-season/{ab}/{SEASON}"
        games = [g for g in get(url)["games"] if g["gameType"] == 2]
        scheds[ab] = [{
            "date": g["gameDate"],
            "home": g["homeTeam"]["abbrev"],
            "away": g["awayTeam"]["abbrev"],
            "neutral": g.get("neutralSite", False),
            "startUTC": g["startTimeUTC"],
        } for g in games]
        print(f"  {ab} {len(games)} games", file=sys.stderr)
        time.sleep(0.2)
    out = {"prior": prior, "schedules": scheds}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def analyse(team: str, data: dict) -> dict:
    prior, games = data["prior"], data["schedules"][team]
    opps, venues, dates = [], [], []
    for g in games:
        home = g["home"] == team
        opps.append(g["away"] if home else g["home"])
        venues.append(team if home and not g["neutral"] else g["home"])
        dates.append(date.fromisoformat(g["date"]))

    opp_points = [prior[o]["points"] for o in opps]
    vs_playoff = sum(prior[o]["playoffs"] for o in opps)
    home_games = sum(1 for g in games if g["home"] == team and not g["neutral"])

    # Rest. Gaps are calendar days between consecutive games.
    gaps = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]
    b2b = sum(1 for g in gaps if g == 1)
    b2b_travel = sum(1 for i, g in enumerate(gaps, start=1)
                     if g == 1 and venues[i] != venues[i - 1])

    # Travel. Start and finish at home; a game at our own arena adds nothing.
    legs = [venues[0]] + venues[1:]
    total = miles(team, legs[0])
    for i in range(1, len(legs)):
        total += miles(legs[i - 1], legs[i])
    total += miles(legs[-1], team)

    # Rested-opponent games: they had 2+ days off, we are on a back-to-back.
    opp_dates = {o: sorted(date.fromisoformat(g["date"]) for g in data["schedules"][o])
                 for o in set(opps)}
    tired = 0
    for i in range(1, len(dates)):
        if gaps[i - 1] != 1:
            continue
        o, d = opps[i], dates[i]
        prev = [x for x in opp_dates[o] if x < d]
        if prev and (d - prev[-1]).days >= 3:
            tired += 1

    trips, run, cur = [], 0, None
    for g in games:
        at_home = g["home"] == team and not g["neutral"]
        if cur is None or at_home == cur:
            run += 1
        else:
            trips.append((cur, run))
            run = 1
        cur = at_home
    trips.append((cur, run))

    return {
        "games": len(games),
        "home": home_games,
        "away": len(games) - home_games,
        "opp_points": sum(opp_points) / len(opp_points),
        "vs_playoff": vs_playoff,
        "b2b": b2b,
        "b2b_travel": b2b_travel,
        "b2b_vs_rested": tired,
        "miles": total,
        "one_day_rest": sum(1 for g in gaps if g == 2),
        "three_plus": sum(1 for g in gaps if g >= 4),
        "longest_road": max([n for h, n in trips if not h], default=0),
        "longest_home": max([n for h, n in trips if h], default=0),
        "opens": games[0]["date"],
        "ends": games[-1]["date"],
    }


def points_vs_differential(prior: dict) -> dict:
    """Least-squares fit of 2025-26 points on goal differential, and the residuals.

    The same question the Tigers pieces keep asking: was the record earned, or is
    it running ahead of the underlying play? A team well above the line won more
    than its goals say it should have.
    """
    xs = [v["gf"] - v["ga"] for v in prior.values()]
    ys = [v["points"] for v in prior.values()]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = my - slope * mx
    resid = {k: v["points"] - (intercept + slope * (v["gf"] - v["ga"]))
             for k, v in prior.items()}
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum(r ** 2 for r in resid.values())
    return {"slope": slope, "intercept": intercept, "residual": resid,
            "r2": 1 - ss_res / ss_tot, "rmse": (ss_res / n) ** 0.5}


def chart(rows: list[tuple[str, float]], det: float) -> str:
    """All 32 teams as dots on one axis.

    Deliberately not a bar chart. Bars would need a baseline near 90 to be
    readable, and a truncated baseline would make a 3.5 point spread look like a
    landslide, which is the opposite of what the numbers say. Dots on a shared
    axis show the bunching honestly, and the whole argument is the bunching.
    """
    rows = sorted(rows, key=lambda r: -r[1])
    rank = [n for n, _ in rows].index("DET") + 1
    lg = sum(v for _, v in rows) / len(rows)
    lo, hi = 90.0, 94.0

    W, H = 640, 176
    x0, x1, axis = 40, 600, 118

    def x(p: float) -> float:
        return x0 + (p - lo) / (hi - lo) * (x1 - x0)

    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="nhl-sos-t" '
           f'style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,'
           f'-apple-system,\'Segoe UI\',Roboto,sans-serif">',
           '<title id="nhl-sos-t">Every NHL team\'s 2026-27 schedule strength, '
           'plotted as average opponent points from last season. All 32 teams fall '
           'between 90.4 and 93.9, with Detroit at 93.2.</title>',
           '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
           'Every team\'s 2026-27 schedule, on one axis</text>',
           '<text x="0" y="34" fill="var(--muted)" font-size="11">'
           'Average points each team\'s opponents earned last season. 32 dots. '
           'The whole league fits in 3.5 points.</text>',
           f'<line x1="{x0}" y1="{axis}" x2="{x1}" y2="{axis}" stroke="var(--rule)" '
           f'stroke-width="1"/>']
    for tick in (90, 91, 92, 93, 94):
        out.append(f'<line x1="{x(tick):.1f}" y1="{axis}" x2="{x(tick):.1f}" y2="{axis + 5}" '
                   f'stroke="var(--rule)" stroke-width="1"/>')
        out.append(f'<text x="{x(tick):.1f}" y="{axis + 19}" text-anchor="middle" '
                   f'fill="var(--muted)" font-size="11" '
                   f'font-variant-numeric="tabular-nums">{tick}</text>')
    out.append(f'<line x1="{x(lg):.1f}" y1="60" x2="{x(lg):.1f}" y2="{axis}" '
               f'stroke="var(--rule)" stroke-width="2" stroke-dasharray="3 3"/>')
    out.append(f'<text x="{x(lg):.1f}" y="55" text-anchor="middle" fill="var(--muted)" '
               f'font-size="11">league average {lg:.2f}</text>')

    # Stack dots that would otherwise overlap, so 32 teams stay countable.
    placed: list[tuple[float, int]] = []
    for name, val in rows:
        px = x(val)
        row = 0
        while any(abs(px - qx) < 9 and row == qr for qx, qr in placed):
            row += 1
        placed.append((px, row))
        cy = axis - 10 - row * 11
        if name == "DET":
            # Label sits clear of the stack, with a leader down to the dot, so it
            # cannot land on top of a neighbouring team's marker.
            out.append(f'<circle cx="{px:.1f}" cy="{cy}" r="6" fill="var(--chart-neg)">'
                       f'<title>Detroit: {val:.2f}, rank {rank} of 32</title></circle>')
            out.append(f'<line x1="{px:.1f}" y1="72" x2="{px:.1f}" y2="{cy - 7}" '
                       f'stroke="var(--chart-neg)" stroke-width="1"/>')
            out.append(f'<text x="{px:.1f}" y="69" text-anchor="middle" '
                       f'fill="var(--fg)" font-size="11" font-weight="700">DET</text>')
        else:
            out.append(f'<circle cx="{px:.1f}" cy="{cy}" r="4" fill="var(--muted)" '
                       f'opacity="0.55"><title>{name}: {val:.2f}</title></circle>')
    out.append(f'<text x="0" y="{H - 6}" fill="var(--muted)" font-size="11">'
               f'Detroit {det:.2f}, rank {rank} of 32. Hardest '
               f'{rows[0][0]} {rows[0][1]:.2f}, easiest {rows[-1][0]} '
               f'{rows[-1][1]:.2f}.</text>')
    out.append("</svg>")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    data = collect()
    all_teams = {ab: analyse(ab, data) for ab in data["schedules"]}
    det = all_teams["DET"]

    if "--json" in argv:
        print(json.dumps({"teams": all_teams, "prior": data["prior"]}, indent=1))
        return 0

    def rank(key: str, high_is_hard: bool = True) -> int:
        order = sorted(all_teams.items(), key=lambda kv: -kv[1][key] if high_is_hard
                       else kv[1][key])
        return [k for k, _ in order].index("DET") + 1

    p = data["prior"]["DET"]
    print(f"Detroit 2025-26: {p['wins']}-{p['losses']}-{p['ot']}, {p['points']} points, "
          f"{p['gf']} for {p['ga']} against, diff {p['gf'] - p['ga']:+d}")
    # The bar is the second wild card, not the weakest division qualifier.
    cut = min(v["points"] for v in data["prior"].values()
              if v["playoffs"] and v["conf"] == "Eastern" and v["wildcard"] in (1, 2))
    holder = [k for k, v in data["prior"].items()
              if v["conf"] == "Eastern" and v["wildcard"] == 2 and v["playoffs"]]
    print(f"Last Eastern wild card: {holder[0]} at {cut} points; "
          f"Detroit missed by {cut - p['points']}")

    # Where the hard schedule comes from: who is in the division.
    div = [k for k, v in data["prior"].items()
           if v["div"] == p["div"] and k != "DET"]
    print(f"Atlantic rivals: {len(div)}, of which {sum(data['prior'][d]['playoffs'] for d in div)} "
          f"made the 2026 playoffs ({', '.join(sorted(d for d in div if data['prior'][d]['playoffs']))})")
    div_games = sum(1 for g in data["schedules"]["DET"]
                    if (g["away"] if g["home"] == "DET" else g["home"]) in div)
    print(f"Games inside the division: {div_games} of 84")
    order = sorted(all_teams.items(), key=lambda kv: -kv[1]["vs_playoff"])
    print("Most games vs 2026 playoff teams: " +
          ", ".join(f"{k} {v['vs_playoff']}" for k, v in order[:5]))
    print()
    print(f"2026-27: {det['games']} games, {det['opens']} to {det['ends']}, "
          f"{det['home']} home / {det['away']} away")
    print(f"Average opponent points last season: {det['opp_points']:.2f} "
          f"(rank {rank('opp_points')} of 32 hardest)")
    print(f"Games vs 2026 playoff teams: {det['vs_playoff']} "
          f"(rank {rank('vs_playoff')} of 32)")
    print(f"Back-to-backs: {det['b2b']} (rank {rank('b2b')} of 32 most), "
          f"{det['b2b_travel']} of them with a venue change")
    print(f"Back-to-backs against an opponent with 2+ days rest: {det['b2b_vs_rested']} "
          f"(rank {rank('b2b_vs_rested')} of 32)")
    print(f"Travel: {det['miles']:,.0f} great-circle miles "
          f"(rank {rank('miles')} of 32 most)")
    print(f"Longest road trip {det['longest_road']}, longest homestand {det['longest_home']}")
    print()
    lg = {k: sum(v[k] for v in all_teams.values()) / 32
          for k in ("opp_points", "vs_playoff", "b2b", "b2b_vs_rested", "miles")}
    print("League averages: " + ", ".join(
        f"{k} {lg[k]:,.2f}" for k in ("opp_points", "vs_playoff", "b2b",
                                      "b2b_vs_rested", "miles")))

    fit = points_vs_differential(data["prior"])
    order = sorted(fit["residual"].items(), key=lambda kv: -kv[1])
    place = [k for k, _ in order].index("DET") + 1
    print(f"\nPoints on goal differential, 2025-26: {fit['slope']:.3f} points per goal, "
          f"intercept {fit['intercept']:.1f}, r2 {fit['r2']:.3f}, "
          f"typical miss {fit['rmse']:.1f} points")
    print(f"Detroit residual {fit['residual']['DET']:+.1f} points, "
          f"rank {place} of 32 (1 = most points above what the goals predict)")
    print("Most above: " + ", ".join(f"{k} {v:+.1f}" for k, v in order[:3]))
    print("Most below: " + ", ".join(f"{k} {v:+.1f}" for k, v in order[-3:]))

    svg = ROOT / "scripts" / "last_nhl_sos_chart.svg"
    svg.write_text(chart([(k, v["opp_points"]) for k, v in all_teams.items()],
                         det["opp_points"]), encoding="utf-8")
    print(f"\nwrote {svg.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
