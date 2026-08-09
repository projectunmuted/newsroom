#!/usr/bin/env python3
"""Is a bad close-game record a property of the team, or is it noise?

A reader (u/suicide-squeeze on r/motorcitykitties, 2026-08-08) argued that the
Pythagorean-regression story is conceptually wrong: a team that keeps losing
close games may simply be a team that is bad at close games, not a team with
luck owed to it. That objection is testable, and this is the test.

    python scripts/close_games.py            # margin <= 3 (default)
    python scripts/close_games.py --margin 1 # one-run games only

Method, and why:

* **Split-half reliability.** Deal each team's close games alternately into two
  piles, compute the win rate in each pile, and correlate across all 30 teams.
  If close-game performance were a repeatable team property, a team's odd games
  would predict its even games. Two piles from the same season share the same
  roster, the same manager and the same bullpen, so this is the friendliest
  possible test of the skill hypothesis: no aging, no trades in between, no
  drift. If it fails here it fails everywhere.
* **The same test on all games**, as a control. Team quality is unquestionably
  real, so overall win rate has to survive split-half. If it does and close
  games do not, the difference is the finding rather than an artifact of small
  samples.
* **Chronological halves**, first half of a team's close games predicting the
  second half. This is the forward-looking version of the claim, the one that
  matters to anyone reading a standings page in August.
* **A random baseline.** Simulate each team playing its actual number of close
  games as coin flips and run the identical split-half. Small samples produce a
  nonzero correlation by chance; this says how much.

Correlation is Pearson r, computed here rather than imported, since the site
runs on the standard library only.
"""

from __future__ import annotations

import argparse
import json
import random
import urllib.request
from collections import defaultdict
from pathlib import Path

SEASON_START, SEASON_END = "2026-03-01", "2026-08-08"
DETROIT = "Detroit Tigers"
AL_CENTRAL = {
    "Detroit Tigers", "Cleveland Guardians", "Minnesota Twins",
    "Kansas City Royals", "Chicago White Sox",
}


def load_seasons(years: list[int]) -> dict[int, list[dict]]:
    """Completed regular seasons, keyed by year.

    Thirty teams is not enough to separate an r of +0.10 from an r of +0.23,
    so the reliability test runs over many team-seasons instead of one. Each
    season is pooled as its own set of teams; nothing is averaged across a
    trade deadline or an offseason.
    """
    out = {}
    for y in years:
        out[y] = load_games(f"{y}-03-01", f"{y}-11-05")
    return out


def snapshot_path(name: str = "close_games_snapshot.json") -> Path:
    return Path(__file__).resolve().parent / name


def load_snapshot(refresh: bool = False) -> list[dict]:
    """The 2026 game list, pinned to a file once taken.

    Games go Final all evening. A chart generated at 9:50pm and a prose table
    generated at 9:58pm will quietly disagree, which is the exact failure the
    generate-from-data rule exists to prevent. So the fetch happens once, the
    result is written next to the script, and every figure in a published piece
    is drawn from that one snapshot. Pass --refresh to take a new one.
    """
    p = snapshot_path()
    if p.exists() and not refresh:
        return json.loads(p.read_text(encoding="utf-8"))["games"]
    games = load_games()
    p.write_text(json.dumps({"pulled": SEASON_END, "through": SEASON_END,
                             "games": games}), encoding="utf-8")
    return games


def load_games(start: str = SEASON_START, end: str = SEASON_END) -> list[dict]:
    """Every completed regular-season game, in order.

    Filters on `abstractGameState`, not `detailedState`. A rain-shortened game
    comes back as "Completed Early" and is a real, counted result; an earlier
    version of this project filtered on the detailed string and silently lost
    one Tigers win that way, which is how a recomputed 55-60 disagreed with the
    standings' 56-60.
    """
    url = ("https://statsapi.mlb.com/api/v1/schedule?sportId=1"
           f"&startDate={start}&endDate={end}&gameType=R")
    with urllib.request.urlopen(url, timeout=90) as r:
        data = json.load(r)

    games = []
    for day in data["dates"]:
        for g in day["games"]:
            if g["status"]["abstractGameState"] != "Final":
                continue
            a, h = g["teams"]["away"], g["teams"]["home"]
            if a.get("score") is None or h.get("score") is None:
                continue
            if a["score"] == h["score"]:          # ties are not decided games
                continue
            games.append({
                "date": g["officialDate"], "pk": g["gamePk"],
                "away": a["team"]["name"], "home": h["team"]["name"],
                "away_score": a["score"], "home_score": h["score"],
            })
    games.sort(key=lambda g: (g["date"], g["pk"]))
    return games


def team_games(games: list[dict]) -> dict[str, list[dict]]:
    """team -> chronological [{margin, won, opponent}]."""
    out: dict[str, list[dict]] = defaultdict(list)
    for g in games:
        margin = abs(g["home_score"] - g["away_score"])
        home_won = g["home_score"] > g["away_score"]
        out[g["home"]].append({"margin": margin, "won": home_won,
                               "opp": g["away"], "date": g["date"]})
        out[g["away"]].append({"margin": margin, "won": not home_won,
                               "opp": g["home"], "date": g["date"]})
    return out


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 3:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return float("nan")
    return num / (dx * dy)


def rate(rows: list[dict]) -> float:
    return sum(r["won"] for r in rows) / len(rows)


def split_half(per_team: dict[str, list[dict]], min_each: int = 8) -> tuple:
    """Alternating split. Returns (r, n_teams, pairs)."""
    xs, ys, pairs = [], [], []
    for team, rows in sorted(per_team.items()):
        odd, even = rows[0::2], rows[1::2]
        if len(odd) < min_each or len(even) < min_each:
            continue
        xs.append(rate(odd)); ys.append(rate(even))
        pairs.append((team, rate(odd), rate(even)))
    return pearson(xs, ys), len(xs), pairs


def chrono_half(per_team: dict[str, list[dict]], min_each: int = 8) -> tuple:
    xs, ys, pairs = [], [], []
    for team, rows in sorted(per_team.items()):
        half = len(rows) // 2
        first, second = rows[:half], rows[half:]
        if len(first) < min_each or len(second) < min_each:
            continue
        xs.append(rate(first)); ys.append(rate(second))
        pairs.append((team, rate(first), rate(second)))
    return pearson(xs, ys), len(xs), pairs


def coin_flip_baseline(counts: list[int], trials: int = 2000,
                       seed: int = 20260808) -> tuple[float, float, float]:
    """Split-half r for teams whose games are literally coin flips.

    Returns (mean, 5th percentile, 95th percentile) of r over `trials`.
    Deterministic seed so a published number can be reproduced exactly. The
    counts are passed in so the baseline is generated at the *same* sample
    sizes as whatever is being compared to it; a split-half correlation shrinks
    as the piles get smaller, and comparing a 70-game split against a 116-game
    split would credit sample size as if it were signal.
    """
    rng = random.Random(seed)
    rs = []
    for _ in range(trials):
        xs, ys = [], []
        for n in counts:
            flips = [rng.random() < 0.5 for _ in range(n)]
            odd, even = flips[0::2], flips[1::2]
            if len(odd) < 8 or len(even) < 8:
                continue
            xs.append(sum(odd) / len(odd)); ys.append(sum(even) / len(even))
        r = pearson(xs, ys)
        if r == r:                                 # skip NaN
            rs.append(r)
    rs.sort()
    return (sum(rs) / len(rs), rs[int(0.05 * len(rs))], rs[int(0.95 * len(rs))])


def matched_subsample(per_team_all: dict[str, list[dict]],
                      target: dict[str, int], trials: int = 400,
                      seed: int = 20260808) -> float:
    """Split-half r on *all* games, thinned to the close-game sample sizes.

    The honest control. Close games self-predict at some r; all games self-
    predict at a higher one. Part of that gap is just that every team played
    more games than close games. This throws games away at random until the
    counts match, so what survives the comparison is signal rather than n.
    """
    rng = random.Random(seed)
    rs = []
    for _ in range(trials):
        xs, ys = [], []
        for team, rows in sorted(per_team_all.items()):
            k = target.get(team, 0)
            if k < 16 or k > len(rows):
                continue
            thinned = rng.sample(rows, k)
            odd, even = thinned[0::2], thinned[1::2]
            if len(odd) < 8 or len(even) < 8:
                continue
            xs.append(rate(odd)); ys.append(rate(even))
        r = pearson(xs, ys)
        if r == r:
            rs.append(r)
    return sum(rs) / len(rs)


def binom_tail_at_most(k: int, n: int, p: float = 0.5) -> float:
    """P(X <= k) for X ~ Binomial(n, p). Exact, no dependencies."""
    total = 0.0
    c = 1.0                                        # C(n, 0)
    for i in range(0, k + 1):
        total += c * (p ** i) * ((1 - p) ** (n - i))
        c = c * (n - i) / (i + 1)
    return total


def pooled_reliability(years: list[int], max_margin: int,
                       seed: int = 20260808) -> None:
    """The same split-half test, pooled over many team-seasons.

    Each (season, team) contributes one point, so four seasons give roughly
    120 instead of 30. A team-season is never averaged with another; the
    pooling happens at the correlation, which is the level where n was the
    problem.
    """
    rng = random.Random(seed)
    close_x, close_y = [], []
    all_x, all_y = [], []
    matched_x, matched_y = [], []
    n_seasons = 0

    for year, games in load_seasons(years).items():
        if not games:
            continue
        n_seasons += 1
        per_team = team_games(games)
        for team, rows in sorted(per_team.items()):
            close = [g for g in rows if g["margin"] <= max_margin]
            if len(close) >= 16:
                close_x.append(rate(close[0::2])); close_y.append(rate(close[1::2]))
            if len(rows) >= 16:
                all_x.append(rate(rows[0::2])); all_y.append(rate(rows[1::2]))
            # All games thinned to the close-game count: the fair control.
            if 16 <= len(close) <= len(rows):
                thin = rng.sample(rows, len(close))
                matched_x.append(rate(thin[0::2])); matched_y.append(rate(thin[1::2]))

    label = ("one-run games" if max_margin == 1
             else f"games decided by {max_margin} or fewer")
    print(f"\nPooled over {n_seasons} seasons ({min(years)}-{max(years)}), "
          f"{len(close_x)} team-seasons")
    print("-" * 62)
    print(f'{"all games":<28} r = {pearson(all_x, all_y):+.3f}   (n = {len(all_x)})')
    print(f'{label:<28} r = {pearson(close_x, close_y):+.3f}   (n = {len(close_x)})')
    r_close = pearson(close_x, close_y)
    r_matched = pearson(matched_x, matched_y)
    print(f'{"all games, thinned to close n":<28} '
          f'r = {r_matched:+.3f}   (n = {len(matched_x)})')

    # Spearman-Brown: a split-half r understates the reliability of the whole
    # sample, because each half is only half as long. This steps it back up.
    sb = lambda r: 2 * r / (1 + r)
    rel_close, rel_all = sb(r_close), sb(r_matched)
    print(f'\nSpearman-Brown reliability of a full season')
    print(f'  {label:<26} {rel_close:.3f}')
    print(f'  {"a same-sized random slice":<26} {rel_all:.3f}')
    print(f'  So a close-game record carries roughly '
          f'{rel_close/rel_all*100:.0f}% of the repeatable signal that the same '
          f'number of\n  ordinary games would carry. Not zero, and not close to '
          f'all of it.')
    return rel_close


def project_detroit(rel_close: float, max_margin: int,
                    remaining_games: int) -> None:
    """What the reliability figure actually implies for the rest of the year.

    Regressing an observed rate toward the mean by its reliability is the
    whole point of measuring reliability. A number that never turns into an
    expectation was decoration.
    """
    games = load_snapshot()
    per_team = team_games(games)
    det = per_team[DETROIT]
    close = [g for g in det if g["margin"] <= max_margin]
    observed = rate(close)
    close_share = len(close) / len(det)
    true_est = 0.500 + rel_close * (observed - 0.500)
    n_ahead = remaining_games * close_share

    print(f"\nWhat that implies for Detroit's last {remaining_games} games")
    print("-" * 62)
    print(f'  observed close-game rate        {observed:.3f} '
          f'({sum(g["won"] for g in close)}-{len(close)-sum(g["won"] for g in close)})')
    print(f'  regressed talent estimate       {true_est:.3f}')
    print(f'  close games expected ahead      {n_ahead:.0f} '
          f'({close_share*100:.0f}% of games have been close)')
    print(f'  at the observed rate            '
          f'{n_ahead*observed:.1f}-{n_ahead*(1-observed):.1f}')
    print(f'  at the regressed rate           '
          f'{n_ahead*true_est:.1f}-{n_ahead*(1-true_est):.1f}')
    print(f'  difference                      '
          f'{n_ahead*(true_est-observed):+.1f} wins')


def run(max_margin: int) -> None:
    games = load_snapshot()
    per_team_all = team_games(games)

    per_team_close = {t: [r for r in rows if r["margin"] <= max_margin]
                      for t, rows in per_team_all.items()}
    per_team_blowout = {t: [r for r in rows if r["margin"] > max_margin]
                        for t, rows in per_team_all.items()}

    label = ("one-run games" if max_margin == 1
             else f"games decided by {max_margin} runs or fewer")
    total_close = sum(len(v) for v in per_team_close.values()) // 2
    print(f"{len(games)} decided regular-season games through {SEASON_END}; "
          f"{total_close} were {label}\n")

    # --- Detroit, the reason any of this is being asked ---
    det_all, det_close = per_team_all[DETROIT], per_team_close[DETROIT]
    det_one = [r for r in det_all if r["margin"] == 1]
    det_div = [r for r in det_all if r["opp"] in AL_CENTRAL]
    def wl(rows): return f'{sum(r["won"] for r in rows)}-{len(rows)-sum(r["won"] for r in rows)}'
    print("Detroit")
    print(f'  overall            {wl(det_all):>8}  ({rate(det_all):.3f})')
    print(f'  {label:<18} {wl(det_close):>8}  ({rate(det_close):.3f})')
    print(f'  one-run games      {wl(det_one):>8}  ({rate(det_one):.3f})')
    print(f'  blowouts (>{max_margin})       {wl(per_team_blowout[DETROIT]):>8}  '
          f'({rate(per_team_blowout[DETROIT]):.3f})')
    print(f'  vs AL Central      {wl(det_div):>8}  ({rate(det_div):.3f})')

    # --- The test ---
    print(f"\nSplit-half reliability (odd games vs even games, same season)")
    print("-" * 62)
    for name, data in (("all games", per_team_all),
                       (label, per_team_close),
                       (f"blowouts (>{max_margin} runs)", per_team_blowout)):
        r, n, _ = split_half(data)
        print(f'{name:<28} r = {r:+.3f}   (n = {n} teams)')

    counts = [len(v) for v in per_team_close.values()]
    mean_r, p5, p95 = coin_flip_baseline(counts)
    print(f'{"coin flips, same n as close":<28} r = {mean_r:+.3f}   '
          f'(90% of sims between {p5:+.3f} and {p95:+.3f})')

    all_counts = [len(v) for v in per_team_all.values()]
    a_mean, a_p5, a_p95 = coin_flip_baseline(all_counts)
    print(f'{"coin flips, same n as all":<28} r = {a_mean:+.3f}   '
          f'(90% of sims between {a_p5:+.3f} and {a_p95:+.3f})')

    matched = matched_subsample(per_team_all,
                                {t: len(v) for t, v in per_team_close.items()})
    print(f'{"all games, thinned to close n":<28} r = {matched:+.3f}   '
          f'(the fair comparison, averaged over 400 draws)')

    print(f"\nFirst half of the season predicting the second")
    print("-" * 62)
    for name, data in (("all games", per_team_all), (label, per_team_close)):
        r, n, _ = chrono_half(data)
        print(f'{name:<28} r = {r:+.3f}   (n = {n} teams)')

    # --- Does close-game record track team quality at all? ---
    teams = sorted(t for t in per_team_all if len(per_team_close[t]) >= 20)
    r_quality = pearson([rate(per_team_all[t]) for t in teams],
                        [rate(per_team_close[t]) for t in teams])
    r_blow = pearson([rate(per_team_blowout[t]) for t in teams],
                     [rate(per_team_close[t]) for t in teams])
    print(f"\nAcross the 30 teams")
    print("-" * 62)
    print(f'overall win rate vs close-game win rate    r = {r_quality:+.3f}')
    print(f'blowout win rate vs close-game win rate    r = {r_blow:+.3f}')

    n_close = len(det_close)
    k_close = sum(r["won"] for r in det_close)
    tail = binom_tail_at_most(k_close, n_close, 0.5)
    print(f'\nIf close games were coin flips, a team playing {n_close} of them '
          f'goes {k_close}-{n_close-k_close}\nor worse {tail*100:.1f}% of the '
          f'time. Thirty teams get thirty tries at that.')

    print(f"\nWorst close-game records, {label}")
    print("-" * 62)
    ranked = sorted(teams, key=lambda t: rate(per_team_close[t]))
    for t in ranked[:5]:
        print(f'  {t:<24}{wl(per_team_close[t]):>8}  ({rate(per_team_close[t]):.3f})'
              f'   overall {wl(per_team_all[t])}')


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--margin", type=int, default=3,
                    help="a game is 'close' when decided by this many runs or fewer")
    ap.add_argument("--seasons", type=int, nargs="*", default=None,
                    help="also run the pooled test over these seasons, e.g. "
                         "--seasons 2022 2023 2024 2025")
    ap.add_argument("--remaining", type=int, default=45,
                    help="Detroit's games left, for the projection")
    args = ap.parse_args()
    run(args.margin)
    if args.seasons:
        rel = pooled_reliability(args.seasons, args.margin)
        project_detroit(rel, args.margin, args.remaining)
