"""How unusual is it to score 1.83 runs a game against one opponent?

Detroit is 0-6 against Cleveland in 2026 and has scored 11 runs doing it,
against a season average of 4.58. This script asks whether that is a real
property of the matchup or the ordinary noise of a six-game sample, by
building the same statistic for every team-opponent pair in baseball.

For each (team, opponent) pair with at least MIN_GAMES completed games, it
computes the team's runs per game in that matchup minus the team's runs per
game for the season. Detroit-vs-Cleveland is then a single point in a
distribution of a few hundred, and the question "is minus 2.75 remarkable?"
becomes a percentile rather than a feeling.

Data: MLB Stats API schedule endpoint, regular season only, filtered on
abstractGameState == "Final" (never the detailed string, which sits on
"Game Over" and "Completed Early" for real finished games).

Usage:
    python scripts/opponent_splits.py
    python scripts/opponent_splits.py --min-games 6 --season 2026
"""

import argparse
import json
import os
import urllib.request
from collections import defaultdict

CACHE = os.path.join(os.path.dirname(__file__), "opponent_splits_cache.json")
API = "https://statsapi.mlb.com/api/v1"


def fetch_season(season, refresh=False):
    """Every completed regular-season game, pinned to a cache file.

    Pinned for the same reason close_games_snapshot.json is: games go Final
    all evening, and a chart built at 9:50 disagreeing with a table built at
    9:58 is a bug that has already happened here once.
    """
    if os.path.exists(CACHE) and not refresh:
        with open(CACHE) as f:
            blob = json.load(f)
        if blob.get("season") == season:
            return blob["games"]

    url = (
        f"{API}/schedule?sportId=1&gameType=R"
        f"&startDate={season}-03-01&endDate={season}-11-01"
    )
    data = json.load(urllib.request.urlopen(url))

    games = []
    for date in data["dates"]:
        for g in date["games"]:
            if g["status"]["abstractGameState"] != "Final":
                continue
            away, home = g["teams"]["away"], g["teams"]["home"]
            if away.get("score") is None or home.get("score") is None:
                continue
            games.append(
                {
                    "pk": g["gamePk"],
                    "date": date["date"],
                    "away": away["team"]["id"],
                    "away_name": away["team"]["name"],
                    "away_score": away["score"],
                    "home": home["team"]["id"],
                    "home_name": home["team"]["name"],
                    "home_score": home["score"],
                }
            )

    with open(CACHE, "w") as f:
        json.dump({"season": season, "games": games}, f)
    return games


def build(games, min_games):
    """Returns (season_rpg, pair_rows) keyed by team id."""
    names = {}
    season_runs = defaultdict(int)
    season_games = defaultdict(int)
    pair_runs = defaultdict(int)
    pair_games = defaultdict(int)
    pair_wins = defaultdict(int)

    for g in games:
        a, h = g["away"], g["home"]
        names[a], names[h] = g["away_name"], g["home_name"]
        for team, opp, rs, ra in (
            (a, h, g["away_score"], g["home_score"]),
            (h, a, g["home_score"], g["away_score"]),
        ):
            season_runs[team] += rs
            season_games[team] += 1
            pair_runs[(team, opp)] += rs
            pair_games[(team, opp)] += 1
            if rs > ra:
                pair_wins[(team, opp)] += 1

    season_rpg = {t: season_runs[t] / season_games[t] for t in season_games}

    rows = []
    for (team, opp), n in pair_games.items():
        if n < min_games:
            continue
        rpg = pair_runs[(team, opp)] / n
        rows.append(
            {
                "team": names[team],
                "opp": names[opp],
                "games": n,
                "runs": pair_runs[(team, opp)],
                "rpg": rpg,
                "season_rpg": season_rpg[team],
                "delta": rpg - season_rpg[team],
                "wins": pair_wins[(team, opp)],
            }
        )
    rows.sort(key=lambda r: r["delta"])
    return season_rpg, rows


def permutation_test(games, min_games, trials, seed=20260809):
    """If opponent identity meant nothing, how extreme would the worst pair be?

    Somebody has to be the worst matchup in baseball. The question is not
    whether minus 2.75 is a big number, it is whether minus 2.75 is bigger
    than the worst number 294 coin flips produce.

    So: hold every team's actual game-by-game runs scored fixed, shuffle
    which of that team's games belong to which opponent (preserving how many
    games each pair has), recompute all the deltas, and record the single
    most negative one. Repeat. That distribution is what pure chance looks
    like at this sample size.
    """
    import random

    rng = random.Random(seed)

    # team -> list of runs scored, and team -> list of pair sizes
    scored = defaultdict(list)
    pair_sizes = defaultdict(list)
    counts = defaultdict(int)
    for g in games:
        scored[g["away"]].append(g["away_score"])
        scored[g["home"]].append(g["home_score"])
        counts[(g["away"], g["home"])] += 1
        counts[(g["home"], g["away"])] += 1
    for (team, _opp), n in counts.items():
        pair_sizes[team].append(n)

    minima = []
    for _ in range(trials):
        worst = 0.0
        for team, runs in scored.items():
            shuffled = runs[:]
            rng.shuffle(shuffled)
            season_rpg = sum(runs) / len(runs)
            i = 0
            for n in pair_sizes[team]:
                if n >= min_games:
                    delta = sum(shuffled[i:i + n]) / n - season_rpg
                    worst = min(worst, delta)
                i += n
        minima.append(worst)
    minima.sort()
    return minima


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=2000)
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--min-games", type=int, default=6)
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    games = fetch_season(args.season, refresh=args.refresh)
    season_rpg, rows = build(games, args.min_games)
    print(f"{len(games)} completed games, {len(rows)} team-opponent pairs "
          f"with >= {args.min_games} games\n")

    print("Ten worst offensive matchups in baseball (runs/game vs season avg):")
    for r in rows[:10]:
        print(f"  {r['team']:22s} vs {r['opp']:22s} {r['games']:2d}g  "
              f"{r['rpg']:.2f} vs {r['season_rpg']:.2f}  {r['delta']:+.2f}  "
              f"({r['wins']}-{r['games'] - r['wins']})")

    det = [r for r in rows if r["team"] == "Detroit Tigers"]
    print("\nDetroit's matchups:")
    for r in sorted(det, key=lambda r: r["delta"]):
        rank = rows.index(r) + 1
        print(f"  vs {r['opp']:22s} {r['games']:2d}g  {r['rpg']:.2f}  "
              f"{r['delta']:+.2f}  rank {rank}/{len(rows)}  "
              f"({r['wins']}-{r['games'] - r['wins']})")

    # How many pairs are winless, and how many teams got swept this badly?
    winless = [r for r in rows if r["wins"] == 0]
    # A sweep is rare; seven of them is not. Expected count if every pair were
    # decided by the teams' season win rates and nothing else.
    wpct = {}
    wins_by_team = defaultdict(int)
    gp_by_team = defaultdict(int)
    for g in games:
        gp_by_team[g["away"]] += 1
        gp_by_team[g["home"]] += 1
        winner = g["away"] if g["away_score"] > g["home_score"] else g["home"]
        wins_by_team[winner] += 1
    name_to_id = {}
    for g in games:
        name_to_id[g["away_name"]] = g["away"]
        name_to_id[g["home_name"]] = g["home"]
    for t in gp_by_team:
        wpct[t] = wins_by_team[t] / gp_by_team[t]

    expected_sweeps = 0.0
    for r in rows:
        t, o = name_to_id[r["team"]], name_to_id[r["opp"]]
        # log5: probability team t beats opponent o
        pt, po = wpct[t], wpct[o]
        p = (pt - pt * po) / (pt + po - 2 * pt * po)
        expected_sweeps += (1 - p) ** r["games"]

    print(f"\nWinless pairs at >= {args.min_games} games: {len(winless)} "
          f"(expected by team strength alone: {expected_sweeps:.1f})")
    for r in sorted(winless, key=lambda x: -x["games"]):
        print(f"  {r['team']:22s} 0-{r['games']} vs {r['opp']:22s} "
              f"{r['delta']:+.2f} runs/game")

    deltas = sorted(r["delta"] for r in rows)
    n = len(deltas)
    mean = sum(deltas) / n
    sd = (sum((d - mean) ** 2 for d in deltas) / n) ** 0.5
    print(f"\nDistribution of {n} pair deltas: mean {mean:+.3f}, sd {sd:.3f}")
    for p in (1, 5, 10, 25, 50, 75, 90, 95, 99):
        print(f"  p{p:<2d} {deltas[int(p / 100 * n)]:+.2f}")

    observed = deltas[0]
    minima = permutation_test(games, args.min_games, args.trials)
    beat = sum(1 for m in minima if m <= observed)
    print(f"\nPermutation test, {args.trials} shuffles of who played whom:")
    print(f"  worst pair delta, observed:  {observed:+.2f}")
    print(f"  worst pair delta, simulated: median {minima[len(minima) // 2]:+.2f}, "
          f"p5 {minima[int(.05 * len(minima))]:+.2f}, "
          f"p95 {minima[int(.95 * len(minima))]:+.2f}")
    print(f"  shuffles producing a worst pair at least this extreme: "
          f"{beat}/{len(minima)} ({beat / len(minima):.1%})")


if __name__ == "__main__":
    main()
