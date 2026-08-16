#!/usr/bin/env python3
"""Every number behind the Tigers-Pirates series preview, derived in one run.

Detroit and Pittsburgh both sit on 60 wins in the middle of August and both sit
below what their run differentials say they should have. This asks how far
below, where each club ranks league-wide, and which of the usual mechanisms
(one-run games, bullpen conversion, blowouts) actually accounts for it.

    python scripts/underperformers.py            # prose numbers
    python scripts/underperformers.py --chart    # the inline SVG
    python scripts/underperformers.py --json

One execution derives the chart and the prose together so the two cannot drift
apart, which is a mistake this project has already paid for.

Pythagorean exponent is 1.83, the standard Baseball-Reference value. Every
counting stat comes from the league's own game-by-game feed rather than from a
season-total endpoint, because a season-total endpoint has multiplied counts on
this project before.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import date

API = "https://statsapi.mlb.com/api/v1"
SEASON = 2026
DET, PIT = 116, 134
EXP = 1.83


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "dsr-underperf"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pythag(rs: int, ra: int, games: int) -> float:
    return (rs ** EXP) / ((rs ** EXP) + (ra ** EXP)) * games


def standings() -> list[dict]:
    """All 30 clubs with their Pythagorean gap, worst first."""
    rows = []
    for lg in (103, 104):
        d = get(f"{API}/standings?leagueId={lg}&season={SEASON}"
                f"&standingsTypes=regularSeason&hydrate=team")
        for rec in d["records"]:
            for t in rec["teamRecords"]:
                w, l = t["wins"], t["losses"]
                rs, ra = t["runsScored"], t["runsAllowed"]
                exp = pythag(rs, ra, w + l)
                rows.append({
                    "id": t["team"]["id"], "name": t["team"]["name"],
                    "league": lg, "w": w, "l": l, "rs": rs, "ra": ra,
                    "exp": round(exp, 1), "gap": round(w - exp, 1),
                })
    rows.sort(key=lambda r: r["gap"])
    return rows


def margins(team_id: int) -> dict:
    """Record split by margin of victory, from the game-by-game schedule."""
    sched = get(f"{API}/schedule?sportId=1&teamId={team_id}"
                f"&startDate={SEASON}-03-01&endDate={date.today().isoformat()}"
                f"&gameType=R&hydrate=linescore")
    buckets = {"one": [0, 0], "two_three": [0, 0], "blowout": [0, 0]}
    games = 0
    for d in sched.get("dates", []):
        for g in d["games"]:
            if g["status"]["abstractGameState"] != "Final":
                continue
            home_is = g["teams"]["home"]["team"]["id"] == team_id
            us = g["teams"]["home" if home_is else "away"].get("score")
            them = g["teams"]["away" if home_is else "home"].get("score")
            # A postponed game keeps Final on its original date with null
            # scores and reappears on the makeup date.
            if us is None or them is None:
                continue
            games += 1
            diff = abs(us - them)
            key = ("one" if diff == 1 else
                   "two_three" if diff <= 3 else "blowout")
            buckets[key][0 if us > them else 1] += 1
    return {"games": games, **{k: tuple(v) for k, v in buckets.items()}}


def bullpen(team_id: int) -> dict:
    d = get(f"{API}/teams/{team_id}/stats?stats=season&group=pitching"
            f"&season={SEASON}&gameType=R&sportId=1")
    total = d["stats"][0]["splits"][0]["stat"]
    # The bullpen line is the team line minus what the starters did. The
    # league's own starter/reliever split is available as a separate call and
    # is used here rather than derived, so the two can be reconciled.
    sp = get(f"{API}/teams/{team_id}/stats?stats=statSplits&sitCodes=sp"
             f"&group=pitching&season={SEASON}&gameType=R&sportId=1")
    rp = get(f"{API}/teams/{team_id}/stats?stats=statSplits&sitCodes=rp"
             f"&group=pitching&season={SEASON}&gameType=R&sportId=1")
    out = {"team_era": total.get("era"),
           "saves": total.get("saves"),
           "save_opps": total.get("saveOpportunities"),
           "blown": total.get("blownSaves")}
    for label, blob in (("sp", sp), ("rp", rp)):
        try:
            s = blob["stats"][0]["splits"][0]["stat"]
            out[label] = {"era": s.get("era"), "ip": s.get("inningsPitched"),
                          "so9": s.get("strikeoutsPer9Inn")}
        except (KeyError, IndexError):
            out[label] = {}
    return out


def probables(team_id: int, opp_id: int) -> list[dict]:
    sched = get(f"{API}/schedule?sportId=1&teamId={team_id}&opponentId={opp_id}"
                f"&startDate={date.today().isoformat()}&endDate={SEASON}-11-01"
                f"&gameType=R&hydrate=probablePitcher")
    rows = []
    for d in sched.get("dates", []):
        for g in d["games"]:
            if g["status"]["abstractGameState"] == "Final":
                continue
            home_is = g["teams"]["home"]["team"]["id"] == team_id
            rows.append({
                "pk": g["gamePk"], "date": d["date"], "time": g.get("gameDate"),
                "home": home_is,
                "us": (g["teams"]["home" if home_is else "away"]
                       .get("probablePitcher") or {}).get("fullName"),
                "them": (g["teams"]["away" if home_is else "home"]
                         .get("probablePitcher") or {}).get("fullName"),
                "them_id": (g["teams"]["away" if home_is else "home"]
                            .get("probablePitcher") or {}).get("id"),
            })
    return rows


def pitcher(pid: int) -> dict:
    d = get(f"{API}/people/{pid}?hydrate=stats(group=pitching,type=season,"
            f"season={SEASON})")
    p = d["people"][0]
    s = ((p.get("stats") or [{}])[0].get("splits") or [{}])[0].get("stat", {})
    return {"name": p.get("fullName"), "era": s.get("era"),
            "whip": s.get("whip"), "ip": s.get("inningsPitched"),
            "gs": s.get("gamesStarted"), "so": s.get("strikeOuts"),
            "bb": s.get("baseOnBalls"), "so9": s.get("strikeoutsPer9Inn"),
            "hr": s.get("homeRuns"), "baa": s.get("avg")}


def last_meeting() -> dict:
    """The most recent regular-season game between the two clubs."""
    for year in range(SEASON, SEASON - 12, -1):
        sched = get(f"{API}/schedule?sportId=1&teamId={DET}&opponentId={PIT}"
                    f"&season={year}&gameType=R")
        games = [g for d in sched.get("dates", []) for g in d["games"]
                 if g["status"]["abstractGameState"] == "Final"
                 and g["teams"]["home"].get("score") is not None]
        if games:
            g = games[-1]
            return {"year": year, "count": len(games),
                    "last": g["officialDate"],
                    "score": f"{g['teams']['away']['team']['name']} "
                             f"{g['teams']['away']['score']}, "
                             f"{g['teams']['home']['team']['name']} "
                             f"{g['teams']['home']['score']}"}
    return {}


def home_road(team_id: int) -> dict:
    """Home and road records, counted off the same feed as `margins`.

    The `hydrate=record(type=[home,away])` form on /teams returns an empty
    splitRecords list for this season, so this counts the games instead. Same
    postponed-game guard as everywhere else.
    """
    sched = get(f"{API}/schedule?sportId=1&teamId={team_id}"
                f"&startDate={SEASON}-03-01&endDate={date.today().isoformat()}"
                f"&gameType=R")
    out = {"home": [0, 0], "away": [0, 0]}
    for d in sched.get("dates", []):
        for g in d["games"]:
            if g["status"]["abstractGameState"] != "Final":
                continue
            home_is = g["teams"]["home"]["team"]["id"] == team_id
            us = g["teams"]["home" if home_is else "away"].get("score")
            them = g["teams"]["away" if home_is else "home"].get("score")
            if us is None or them is None:
                continue
            out["home" if home_is else "away"][0 if us > them else 1] += 1
    return {k: tuple(v) for k, v in out.items()}


def league_margins(cache: str = "logs/margin-buckets.json") -> dict:
    """Every club's record split by margin. Cached, because it is 30 calls."""
    import os

    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            return json.load(f)
    teams = get(f"{API}/teams?sportId=1&season={SEASON}")["teams"]
    out = {}
    for t in teams:
        m = margins(t["id"])
        out[t["name"]] = {k: list(v) for k, v in m.items() if k != "games"}
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    return out


def simulate_bucket(lm: dict, observed: float, key: str = "two_three",
                    trials: int = 20000, seed: int = 20260816) -> float:
    """How often does *somebody* finish at or below `observed` in a bucket?

    Same minimum-of-30 logic as `simulate`. Each club plays out its actual
    number of games in that bucket as a fair coin, because a game decided by 2
    or 3 runs has no obvious reason to favour either side once you have already
    conditioned on it being close.
    """
    import random

    rnd = random.Random(seed)
    sizes = [sum(v[key]) for v in lm.values() if sum(v[key])]
    hits = 0
    for _ in range(trials):
        worst = 1.0
        for n in sizes:
            wins = sum(1 for _ in range(n) if rnd.random() < 0.5)
            worst = min(worst, wins / n)
        if worst <= observed + 1e-9:
            hits += 1
    return round(hits / trials, 4)


def simulate(rows: list[dict], trials: int = 20000, seed: int = 20260816) -> dict:
    """How extreme is a Pythagorean shortfall, once you allow for 30 teams?

    Every club plays out its actual number of games as a fair coin weighted by
    its own Pythagorean win probability, so each team is *by construction*
    exactly as good as its run differential says. The only thing left is luck.
    Then take the worst gap in that simulated league.

    The point of taking the minimum across 30 clubs rather than asking about
    one club in isolation is that "biggest in baseball" is a claim about the
    minimum. Asking whether one pre-selected team is unlucky answers a
    different and easier question.
    """
    import random

    rnd = random.Random(seed)
    det = next(r for r in rows if r["id"] == DET)
    pit = next(r for r in rows if r["id"] == PIT)
    params = [(r["w"] + r["l"],
               (r["rs"] ** EXP) / ((r["rs"] ** EXP) + (r["ra"] ** EXP)))
              for r in rows]
    worst_hits = 0
    pit_level_count = 0
    for _ in range(trials):
        worst = 99.0
        n_at_pit = 0
        for games, p in params:
            wins = sum(1 for _ in range(games) if rnd.random() < p)
            gap = wins - p * games
            worst = min(worst, gap)
            if gap <= pit["gap"]:
                n_at_pit += 1
        if worst <= det["gap"]:
            worst_hits += 1
        pit_level_count += n_at_pit
    return {
        "trials": trials, "seed": seed,
        "p_worst_at_least_detroit": round(worst_hits / trials, 4),
        "expected_teams_at_pittsburgh_level": round(pit_level_count / trials, 2),
    }


def chart(rows: list[dict]) -> str:
    """Ranked dot plot of every club's Pythagorean gap, both ends labelled."""
    w, h = 640, 400
    left, right, top = 128.0, 24.0, 46.0
    plot_w = w - left - right
    lo = min(r["gap"] for r in rows)
    hi = max(r["gap"] for r in rows)
    pad = 1.0
    lo, hi = lo - pad, hi + pad

    def x(v: float) -> float:
        return left + (v - lo) / (hi - lo) * plot_w

    row_h = (h - top - 34) / len(rows)
    parts = [
        f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" '
        f'aria-labelledby="pyt-title" style="max-width:{w}px;height:auto;'
        f"font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',"
        f'Roboto,sans-serif">',
        '<title id="pyt-title">Every major league club\'s actual wins minus the '
        'wins its run differential expects, August 16 2026. Detroit is the '
        'furthest below at minus 10.7 and Pittsburgh is third furthest at '
        'minus 4.8.</title>',
        f'<text x="0" y="16" fill="var(--fg)" font-size="13" '
        f'font-weight="600">Wins above and below what the run differential '
        f'expects</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">All 30 clubs. '
        f'Monday\'s two teams are the 1st and 3rd furthest below the line.</text>',
    ]
    zero = x(0)
    parts.append(f'<line x1="{zero:.1f}" y1="{top - 6:.1f}" x2="{zero:.1f}" '
                 f'y2="{h - 30:.1f}" stroke="var(--rule)" stroke-width="1.5" '
                 f'stroke-dasharray="5 4"/>')
    for i, r in enumerate(rows):
        cy = top + row_h * i + row_h / 2
        highlight = r["id"] in (DET, PIT)
        color = "var(--chart-neg)" if r["gap"] < 0 else "var(--chart-pos)"
        weight = "700" if highlight else "400"
        fill = "var(--fg)" if highlight else "var(--muted)"
        parts.append(
            f'<text x="{left - 8:.1f}" y="{cy + 3.5:.1f}" text-anchor="end" '
            f'fill="{fill}" font-size="10" font-weight="{weight}">'
            f'{r["name"]}</text>')
        parts.append(
            f'<line x1="{zero:.1f}" y1="{cy:.1f}" x2="{x(r["gap"]):.1f}" '
            f'y2="{cy:.1f}" stroke="{color}" stroke-width="1.5" '
            f'opacity="{0.9 if highlight else 0.45}"/>')
        parts.append(
            f'<circle cx="{x(r["gap"]):.1f}" cy="{cy:.1f}" '
            f'r="{4.2 if highlight else 3}" fill="{color}">'
            f'<title>{r["name"]}: {r["w"]}-{r["l"]}, expected '
            f'{r["exp"]}, {r["gap"]:+.1f}</title></circle>')
        if highlight:
            parts.append(
                f'<text x="{x(r["gap"]) - 8:.1f}" y="{cy + 3.5:.1f}" '
                f'text-anchor="end" fill="{color}" font-size="10.5" '
                f'font-weight="700" font-variant-numeric="tabular-nums">'
                f'{r["gap"]:+.1f}</text>')
    for v in (-10, -5, 0, 5):
        parts.append(f'<text x="{x(v):.1f}" y="{h - 12:.1f}" '
                     f'text-anchor="middle" fill="var(--muted)" '
                     f'font-size="10.5">{v:+d}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chart", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = standings()
    if a.chart:
        print(chart(rows))
        return

    det = next(r for r in rows if r["id"] == DET)
    pit = next(r for r in rows if r["id"] == PIT)
    nl = [r for r in rows if r["league"] == 104]
    al = [r for r in rows if r["league"] == 103]

    data = {
        "det": det, "pit": pit,
        "det_rank": rows.index(det) + 1, "pit_rank": rows.index(pit) + 1,
        "det_al_rank": al.index(det) + 1, "pit_nl_rank": nl.index(pit) + 1,
        "worst_three": rows[:3],
        "det_margins": margins(DET), "pit_margins": margins(PIT),
        "det_pen": bullpen(DET), "pit_pen": bullpen(PIT),
        "det_split": home_road(DET), "pit_split": home_road(PIT),
        "upcoming": probables(DET, PIT),
        "last_meeting": last_meeting(),
        "sim": simulate(rows),
    }
    lm = league_margins()
    pw, pl = data["pit_margins"]["two_three"]
    data["sim"]["pit_bucket_rate"] = round(pw / (pw + pl), 3)
    data["sim"]["p_someone_at_pit_bucket_rate"] = simulate_bucket(
        lm, pw / (pw + pl))
    data["sim"]["pit_bucket_rank"] = 1 + sorted(
        v["two_three"][0] / sum(v["two_three"]) for v in lm.values()
    ).index(pw / (pw + pl))
    for g in data["upcoming"]:
        if g.get("them_id"):
            g["them_line"] = pitcher(g["them_id"])

    if a.json:
        print(json.dumps(data, indent=1))
        return

    print("Pythagorean gap, worst 5 in baseball")
    for r in rows[:5]:
        print(f"  {r['gap']:+5.1f}  {r['name']:<24} {r['w']}-{r['l']} "
              f"RS {r['rs']} RA {r['ra']} expected {r['exp']}")
    print(f"\n  Detroit: {data['det_rank']} of 30 overall, "
          f"{data['det_al_rank']} of 15 in the AL")
    print(f"  Pittsburgh: {data['pit_rank']} of 30 overall, "
          f"{data['pit_nl_rank']} of 15 in the NL")
    print(f"  Combined shortfall: {det['gap'] + pit['gap']:+.1f} wins")

    for label, m in (("Detroit", data["det_margins"]),
                     ("Pittsburgh", data["pit_margins"])):
        one, tt, bl = m["one"], m["two_three"], m["blowout"]
        print(f"\n{label}: {m['games']} games")
        print(f"  1 run          {one[0]}-{one[1]}")
        print(f"  2 to 3 runs    {tt[0]}-{tt[1]}")
        print(f"  4 or more      {bl[0]}-{bl[1]}")

    for label, p in (("Detroit", data["det_pen"]), ("Pittsburgh", data["pit_pen"])):
        conv = (p["saves"] / p["save_opps"] * 100) if p.get("save_opps") else 0
        print(f"\n{label} pitching: team ERA {p['team_era']}, "
              f"starters {p['sp'].get('era')} in {p['sp'].get('ip')}, "
              f"relievers {p['rp'].get('era')} in {p['rp'].get('ip')}")
        print(f"  saves {p['saves']}/{p['save_opps']} ({conv:.1f}%), "
              f"blown {p['blown']}")

    print("\nUpcoming")
    for g in data["upcoming"]:
        line = g.get("them_line") or {}
        print(f"  {g['date']} pk {g['pk']}  DET {g['us'] or '?'} vs "
              f"{g['them'] or '?'}"
              + (f" (ERA {line.get('era')}, {line.get('gs')} GS, "
                 f"K/9 {line.get('so9')})" if line else ""))

    print(f"\nHome/road: Detroit {data['det_split']}, "
          f"Pittsburgh {data['pit_split']}")

    s = data["sim"]
    print(f"\nSimulation, {s['trials']} leagues, seed {s['seed']}")
    print(f"  P(worst gap in the league is at least Detroit's "
          f"{det['gap']}): {s['p_worst_at_least_detroit']}")
    print(f"  Expected teams at or below Pittsburgh's {pit['gap']}: "
          f"{s['expected_teams_at_pittsburgh_level']}")
    print(f"  Pittsburgh in 2-3 run games: {s['pit_bucket_rate']}, "
          f"rank {s['pit_bucket_rank']} of 30 (1 = worst)")
    print(f"  P(somebody finishes that low by chance): "
          f"{s['p_someone_at_pit_bucket_rate']}")

    print("\nLast meeting:", data["last_meeting"])


if __name__ == "__main__":
    main()
