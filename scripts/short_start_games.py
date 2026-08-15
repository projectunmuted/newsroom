"""Every number behind the Sunday 2026-08-16 pick on `824236`, Sean Burke against
Drew Anderson, derived in one execution so the prose cannot disagree with itself.

The question it exists to answer: Detroit is starting a reliever who has never
been past the 4th inning, against a starter who has thrown 6 or more innings in
9 of his last 11. What does a Detroit game look like when the starter does not
get through the order twice, and how often does that team win it?

Sources, all primary MLB Stats API:
  - every Detroit regular-season boxscore, for batters faced by the starter and
    the game's result
  - game logs for Anderson (623454) and Burke (680732)
  - league standings, for records and run differential

Usage:
    python scripts/short_start_games.py             # use cache if present
    python scripts/short_start_games.py --refresh   # re-fetch everything
"""

import json
import os
import statistics
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "short_start_snapshot.json")

DET = 116
CHW = 145
ANDERSON = 623454
BURKE = 680732
SEASON = 2026

# The threshold is not a round number picked to flatter. 18 batters faced is the
# most Drew Anderson has ever faced in a major league game, so "18 or fewer" is
# literally "a start no longer than his longest".
SHORT = 18


def get(url):
    with urllib.request.urlopen(url) as fh:
        return json.load(fh)


def game_log(pid):
    d = get(
        "https://statsapi.mlb.com/api/v1/people/%d/stats"
        "?stats=gameLog&group=pitching&season=%d&gameType=R" % (pid, SEASON)
    )
    out = []
    for s in d["stats"]:
        for sp in s["splits"]:
            st = sp["stat"]
            out.append(
                {
                    "date": sp["date"],
                    "opp": sp.get("opponent", {}).get("name"),
                    "start": bool(st.get("gamesStarted")),
                    "ip": st.get("inningsPitched"),
                    "outs": st.get("outs"),
                    "er": st.get("earnedRuns"),
                    "h": st.get("hits"),
                    "bb": st.get("baseOnBalls"),
                    "k": st.get("strikeOuts"),
                    "hr": st.get("homeRuns"),
                    "bf": st.get("battersFaced"),
                    "pitches": st.get("numberOfPitches"),
                }
            )
    return out


def season_line(pid):
    d = get(
        "https://statsapi.mlb.com/api/v1/people/%d/stats"
        "?stats=season&group=pitching&season=%d&gameType=R" % (pid, SEASON)
    )
    for s in d["stats"]:
        for sp in s["splits"]:
            return sp["stat"]
    return {}


def detroit_starts():
    """Every finished Detroit regular-season game: starter, batters faced, result.

    A game with a null score is not counted. That trap is already paid for: a
    postponed game returns Final on its original date with no runs in it.
    """
    sched = get(
        "https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=%d"
        "&startDate=%d-03-01&endDate=%d-11-30&gameType=R" % (DET, SEASON, SEASON)
    )
    games = []
    for day in sched["dates"]:
        for g in day["games"]:
            if g["status"].get("abstractGameState") != "Final":
                continue
            home = g["teams"]["home"]
            away = g["teams"]["away"]
            if home.get("score") is None or away.get("score") is None:
                continue
            det_home = home["team"]["id"] == DET
            games.append(
                {
                    "gamePk": g["gamePk"],
                    "date": g["officialDate"],
                    "home": det_home,
                    "det_runs": (home if det_home else away)["score"],
                    "opp_runs": (away if det_home else home)["score"],
                    "opp": (away if det_home else home)["team"]["name"],
                }
            )

    out = []
    for i, g in enumerate(games):
        sys.stderr.write("\r  boxscores %d/%d" % (i + 1, len(games)))
        box = get(
            "https://statsapi.mlb.com/api/v1/game/%d/boxscore" % g["gamePk"]
        )
        side = "home" if g["home"] else "away"
        team = box["teams"][side]
        order = team.get("pitchers") or []
        if not order:
            continue
        starter = order[0]
        st = team["players"]["ID%d" % starter]["stats"]["pitching"]
        rec = dict(g)
        rec["starter"] = team["players"]["ID%d" % starter]["person"]["fullName"]
        rec["bf"] = st.get("battersFaced")
        rec["outs"] = st.get("outs")
        rec["relievers"] = len(order) - 1
        out.append(rec)
    sys.stderr.write("\n")
    return out


def standings():
    rows = {}
    # Keys are strings so a fresh run and a cache round-trip agree; JSON has no
    # integer keys and a silent mismatch between the two paths is exactly the
    # class of bug this project keeps paying for.
    for lg in (103, 104):
        d = get(
            "https://statsapi.mlb.com/api/v1/standings?leagueId=%d&season=%d"
            "&standingsTypes=regularSeason" % (lg, SEASON)
        )
        for rec in d["records"]:
            for t in rec["teamRecords"]:
                rows[str(t["team"]["id"])] = {
                    "name": t["team"]["name"],
                    "w": t["wins"],
                    "l": t["losses"],
                    "rs": t["runsScored"],
                    "ra": t["runsAllowed"],
                }
    return rows


def build(refresh):
    if not refresh and os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)
    snap = {
        "anderson": game_log(ANDERSON),
        "anderson_season": season_line(ANDERSON),
        "burke": game_log(BURKE),
        "burke_season": season_line(BURKE),
        "det_games": detroit_starts(),
        "standings": standings(),
    }
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=1)
    return snap


def pythag(rs, ra):
    return rs ** 2 / float(rs ** 2 + ra ** 2)


def main():
    snap = build("--refresh" in sys.argv)

    print("== Drew Anderson, 2026 ==")
    a = snap["anderson_season"]
    log = snap["anderson"]
    starts = [g for g in log if g["start"]]
    print(
        "  %s G, %s GS, %s IP, %s ERA, %s K, %s BB, %s WHIP, %s BF"
        % (
            a.get("gamesPlayed"),
            a.get("gamesStarted"),
            a.get("inningsPitched"),
            a.get("era"),
            a.get("strikeOuts"),
            a.get("baseOnBalls"),
            a.get("whip"),
            a.get("battersFaced"),
        )
    )
    print("  the starts, oldest first:")
    for g in starts:
        print(
            "    %s  %-22s %5s IP  %2d BF  %3s pitches  %d ER  %d K"
            % (
                g["date"],
                g["opp"][:22],
                g["ip"],
                g["bf"],
                g["pitches"],
                g["er"],
                g["k"],
            )
        )
    most = max(g["bf"] for g in log)
    print("  most batters faced in any appearance, ever this season: %d" % most)
    print("  most outs recorded in any appearance: %d" % max(g["outs"] for g in log))

    print()
    print("== Sean Burke, 2026 ==")
    b = snap["burke_season"]
    print(
        "  %s G, %s GS, %s IP, %s ERA, %s K, %s BB, %s WHIP, %s HR"
        % (
            b.get("gamesPlayed"),
            b.get("gamesStarted"),
            b.get("inningsPitched"),
            b.get("era"),
            b.get("strikeOuts"),
            b.get("baseOnBalls"),
            b.get("whip"),
            b.get("homeRuns"),
        )
    )
    blog = [g for g in snap["burke"] if g["start"]]
    last11 = blog[-11:]
    six_plus = sum(1 for g in last11 if g["outs"] >= 18)
    print("  last %d starts with 18+ outs: %d" % (len(last11), six_plus))
    vs_det = [g for g in snap["burke"] if g["opp"] and "Detroit" in g["opp"]]
    for g in vs_det:
        print(
            "  vs Detroit %s: %s IP, %d ER, %d K, %d BB, %d H"
            % (g["date"], g["ip"], g["er"], g["k"], g["bb"], g["h"])
        )

    print()
    print("== Detroit's season by how long the starter lasted ==")
    games = snap["det_games"]
    bfs = [g["bf"] for g in games if g["bf"] is not None]
    print("  %d finished games, starter batters faced: median %.1f, mean %.1f"
          % (len(games), statistics.median(bfs), statistics.mean(bfs)))

    short = [g for g in games if g["bf"] is not None and g["bf"] <= SHORT]
    rest = [g for g in games if g["bf"] is not None and g["bf"] > SHORT]

    def rec(rows):
        w = sum(1 for g in rows if g["det_runs"] > g["opp_runs"])
        return w, len(rows) - w

    sw, sl = rec(short)
    rw, rl = rec(rest)
    print(
        "  starter faced %d or fewer: %d-%d (%.3f), %d games"
        % (SHORT, sw, sl, sw / float(len(short)), len(short))
    )
    print(
        "  starter faced more than %d: %d-%d (%.3f), %d games"
        % (SHORT, rw, rl, rw / float(len(rest)), len(rest))
    )
    print(
        "  runs allowed per game, short starts %.2f, the rest %.2f"
        % (
            sum(g["opp_runs"] for g in short) / float(len(short)),
            sum(g["opp_runs"] for g in rest) / float(len(rest)),
        )
    )
    print(
        "  relievers used per game, short starts %.1f, the rest %.1f"
        % (
            sum(g["relievers"] for g in short) / float(len(short)),
            sum(g["relievers"] for g in rest) / float(len(rest)),
        )
    )
    print("  the short-start games, most recent last:")
    for g in short:
        print(
            "    %s  %-22s %-20s %2d BF  Detroit %d-%d  %s"
            % (
                g["date"],
                g["opp"][:22],
                g["starter"][:20],
                g["bf"],
                g["det_runs"],
                g["opp_runs"],
                "W" if g["det_runs"] > g["opp_runs"] else "L",
            )
        )

    print()
    print("== The two clubs ==")
    st = snap["standings"]
    for tid in (str(DET), str(CHW)):
        t = st[tid]
        gp = t["w"] + t["l"]
        exp = pythag(t["rs"], t["ra"]) * gp
        print(
            "  %-22s %d-%d, %+d run differential, expected %.1f wins, %+.1f"
            % (
                t["name"],
                t["w"],
                t["l"],
                t["rs"] - t["ra"],
                exp,
                t["w"] - exp,
            )
        )

    gaps = []
    for tid, t in st.items():
        gp = t["w"] + t["l"]
        gaps.append((t["w"] - pythag(t["rs"], t["ra"]) * gp, t["name"]))
    gaps.sort()
    print("  the 3 largest shortfalls in baseball:")
    for g, n in gaps[:3]:
        print("    %-22s %+.1f" % (n, g))


if __name__ == "__main__":
    main()
