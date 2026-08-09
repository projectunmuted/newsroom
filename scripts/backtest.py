#!/usr/bin/env python3
"""Backtest simple game predictors against the 2026 MLB season.

The record is this site's whole product, so the honest question to answer
before asking anyone to care is: does the method beat a coin flip, and does it
beat the trivial baseline of always taking the home team?

    python scripts/backtest.py

Walks the season in order, reconstructing each team's record and run totals as
they stood *before* each game, so nothing leaks from the future. Then scores
several predictors on the same set of games.

Also tests the specific thesis published in Pick No. 1: that a team far below
its Pythagorean expectation is "due." That one is checked over a forward
window rather than a single game, because that is the claim actually made.
"""

from __future__ import annotations

import json
import urllib.request
from collections import defaultdict

EXP = 1.83
MIN_GAMES = 25          # ignore April noise; both teams need a real sample
FORWARD_WINDOW = 20     # games ahead, for the "due" test


def load_games() -> list[dict]:
    url = ("https://statsapi.mlb.com/api/v1/schedule?sportId=1"
           "&startDate=2026-03-01&endDate=2026-08-07&gameType=R")
    with urllib.request.urlopen(url, timeout=60) as r:
        data = json.load(r)
    games = []
    for day in data["dates"]:
        for g in day["games"]:
            # `abstractGameState`, not `detailedState`: a rain-shortened game
            # comes back as "Completed Early" and is a real, counted result.
            # Matching the literal string "Final" silently dropped one Tigers
            # win (Apr 4 vs St. Louis) from every game-by-game figure here.
            if g["status"]["abstractGameState"] != "Final":
                continue
            a, h = g["teams"]["away"], g["teams"]["home"]
            if a.get("score") is None or h.get("score") is None:
                continue
            games.append({
                "date": g["officialDate"],
                "pk": g["gamePk"],
                "away": a["team"]["name"], "home": h["team"]["name"],
                "away_score": a["score"], "home_score": h["score"],
                "home_won": h["score"] > a["score"],
            })
    games.sort(key=lambda g: (g["date"], g["pk"]))
    return games


def pyth(rs: float, ra: float) -> float:
    if rs <= 0 or ra <= 0:
        return 0.5
    return (rs ** EXP) / ((rs ** EXP) + (ra ** EXP))


def state_snapshot():
    return {"w": 0, "l": 0, "rs": 0, "ra": 0}


def run() -> None:
    games = load_games()
    st = defaultdict(state_snapshot)

    # Predictor -> [correct, total]. Each predictor returns True for "home wins",
    # False for "away wins", or None to abstain when it has no opinion.
    preds = {
        "Always home": lambda h, a: True,
        "Better record": lambda h, a: None if wpct(h) == wpct(a) else wpct(h) > wpct(a),
        "Better run diff": lambda h, a: None if diff(h) == diff(a) else diff(h) > diff(a),
        "Better Pythagorean": lambda h, a: None if pz(h) == pz(a) else pz(h) > pz(a),
        "Most 'due' team": lambda h, a: None if luck(h) == luck(a) else luck(h) < luck(a),
    }
    score = {k: [0, 0] for k in preds}

    wpct = lambda s: s["w"] / max(1, s["w"] + s["l"])
    diff = lambda s: (s["rs"] - s["ra"]) / max(1, s["w"] + s["l"])
    pz = lambda s: pyth(s["rs"], s["ra"])
    luck = lambda s: wpct(s) - pz(s)      # negative means underperforming

    # Forward-window test for the "due" thesis.
    due_rows = []          # (luck_at_time, team, games_played)
    team_future = defaultdict(list)   # team -> chronological list of (won?)

    for g in games:
        h, a = st[g["home"]], st[g["away"]]
        hg, ag = h["w"] + h["l"], a["w"] + a["l"]

        if hg >= MIN_GAMES and ag >= MIN_GAMES:
            for name, fn in preds.items():
                call = fn(h, a)
                if call is None:
                    continue
                score[name][1] += 1
                if call == g["home_won"]:
                    score[name][0] += 1

            # Snapshot each team's luck for the forward test.
            for side, s in (("home", h), ("away", a)):
                due_rows.append((luck(s), g[side], len(team_future[g[side]])))

        # Advance state AFTER predicting.
        for side, s in (("home", h), ("away", a)):
            won = g["home_won"] if side == "home" else not g["home_won"]
            s["w" if won else "l"] += 1
            team_future[g[side]].append(won)
        h["rs"] += g["home_score"]; h["ra"] += g["away_score"]
        a["rs"] += g["away_score"]; a["ra"] += g["home_score"]

    print(f"Backtest on {len(games)} completed 2026 games "
          f"(scored once both teams had {MIN_GAMES}+ games)\n")
    print(f'{"predictor":<22}{"correct":>9}{"games":>8}{"accuracy":>10}')
    print("-" * 49)
    for name, (c, t) in sorted(score.items(), key=lambda kv: -(kv[1][0] / max(1, kv[1][1]))):
        if t:
            print(f'{name:<22}{c:>9}{t:>8}{c/t*100:>9.1f}%')

    # --- The published thesis: are unlucky teams "due"? ---
    print(f"\nThe 'due' thesis, tested over the next {FORWARD_WINDOW} games")
    print("-" * 49)
    buckets = {"very unlucky (< -.060)": [], "unlucky (-.060 to -.020)": [],
               "neutral (-.020 to .020)": [], "lucky (> .020)": []}
    for luck_val, team, idx in due_rows:
        fut = team_future[team][idx:idx + FORWARD_WINDOW]
        if len(fut) < FORWARD_WINDOW:
            continue
        rate = sum(fut) / len(fut)
        if luck_val < -0.060:
            buckets["very unlucky (< -.060)"].append(rate)
        elif luck_val < -0.020:
            buckets["unlucky (-.060 to -.020)"].append(rate)
        elif luck_val <= 0.020:
            buckets["neutral (-.020 to .020)"].append(rate)
        else:
            buckets["lucky (> .020)"].append(rate)

    for label, rates in buckets.items():
        if rates:
            print(f'{label:<28}{sum(rates)/len(rates)*100:>6.1f}% over next {FORWARD_WINDOW}'
                  f'   (n={len(rates)})')


if __name__ == "__main__":
    run()
