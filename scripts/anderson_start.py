"""Every number behind the 2026-08-10 entry on Drew Anderson's start against
Cleveland, derived in one execution so the prose and the chart cannot disagree.

Sources, all primary:
  - MLB Stats API game logs (Anderson 623454, Bibee 676440)
  - MLB Stats API boxscores for every Detroit game, for batters faced per start
  - MLB Stats API standings and team season pitching

Anything the API cannot answer (his years in Japan and Korea) is not computed
here; it is cited in the entry from the reporting, and is flagged as such.

Usage:
    python scripts/anderson_start.py            # use the cache if present
    python scripts/anderson_start.py --refresh  # re-fetch everything
"""

import json
import os
import statistics
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "anderson_snapshot.json")

DET = 116
CLE = 114
ANDERSON = 623454
BIBEE = 676440
SEASON = 2026


def get(url):
    with urllib.request.urlopen(url) as fh:
        return json.load(fh)


def game_log(pid):
    d = get(
        "https://statsapi.mlb.com/api/v1/people/%d/stats"
        "?stats=gameLog&group=pitching&season=%d" % (pid, SEASON)
    )
    out = []
    for s in d["stats"]:
        for sp in s["splits"]:
            st = sp["stat"]
            out.append(
                {
                    "date": sp["date"],
                    "gamePk": sp.get("game", {}).get("gamePk"),
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


def det_games():
    d = get(
        # gameType=R matters: without it the schedule returns spring training
        # too, which quietly added 22 exhibition games to the starter sample.
        "https://statsapi.mlb.com/api/v1/schedule?sportId=1&gameType=R&teamId=%d"
        "&startDate=%d-03-01&endDate=%d-08-09" % (DET, SEASON, SEASON)
    )
    out = []
    for dt in d["dates"]:
        for g in dt["games"]:
            if g["status"]["abstractGameState"] != "Final":
                continue
            a, h = g["teams"]["away"], g["teams"]["home"]
            # A postponed game returns Final on its original date with null
            # scores. Requiring a score is the only safe filter; this project
            # has already been bitten by trusting the status string alone.
            if a.get("score") is None or h.get("score") is None:
                continue
            out.append(
                {
                    "date": dt["date"],
                    "gamePk": g["gamePk"],
                    "away": a["team"]["name"],
                    "away_id": a["team"]["id"],
                    "away_score": a["score"],
                    "home": h["team"]["name"],
                    "home_id": h["team"]["id"],
                    "home_score": h["score"],
                }
            )
    return out


def det_starter_lines(games):
    """Batters faced and outs recorded by Detroit's starting pitcher, per game."""
    lines = []
    for i, g in enumerate(games):
        box = get(
            "https://statsapi.mlb.com/api/v1/game/%d/boxscore" % g["gamePk"]
        )
        side = "home" if g["home_id"] == DET else "away"
        team = box["teams"][side]
        order = team.get("pitchers") or []
        if not order:
            continue
        pid = order[0]
        p = team["players"]["ID%d" % pid]
        st = p["stats"]["pitching"]
        lines.append(
            {
                "date": g["date"],
                "gamePk": g["gamePk"],
                "pitcher": p["person"]["fullName"],
                "id": pid,
                "bf": st.get("battersFaced"),
                "outs": st.get("outs"),
                "er": st.get("earnedRuns"),
            }
        )
        sys.stderr.write("\r  boxscores %d/%d" % (i + 1, len(games)))
    sys.stderr.write("\n")
    return lines


def standings():
    d = get(
        "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104"
        "&season=%d&standingsTypes=regularSeason&hydrate=team" % SEASON
    )
    out = {}
    for rec in d["records"]:
        for t in rec["teamRecords"]:
            out[t["team"]["name"]] = {
                "w": t["wins"],
                "l": t["losses"],
                "rs": t.get("runsScored"),
                "ra": t.get("runsAllowed"),
                "diff": t.get("runDifferential"),
                "gb": t.get("gamesBack"),
                "wcgb": t.get("wildCardGamesBack"),
                "g": t["wins"] + t["losses"],
                # splitRecords carries home/away/lastTen. The entry quotes
                # those, so they belong in this snapshot rather than in a
                # separate lookup the sourcing note would then be lying about.
                "splits": {
                    r["type"]: "%d-%d" % (r["wins"], r["losses"])
                    for r in t.get("records", {}).get("splitRecords", [])
                },
            }
    return out


def team_pitching(team_id):
    d = get(
        "https://statsapi.mlb.com/api/v1/teams/%d/stats"
        "?season=%d&stats=season&group=pitching" % (team_id, SEASON)
    )
    return d["stats"][0]["splits"][0]["stat"]


def league_pitching():
    d = get(
        "https://statsapi.mlb.com/api/v1/teams/stats?season=%d&stats=season"
        "&group=pitching&sportId=1" % SEASON
    )
    return [
        {
            "team": sp["team"]["name"],
            "saves": int(sp["stat"]["saves"]),
            "blown": int(sp["stat"]["blownSaves"]),
            "era": sp["stat"]["era"],
        }
        for sp in d["stats"][0]["splits"]
    ]


def load(refresh=False):
    if os.path.exists(CACHE) and not refresh:
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)
    games = det_games()
    snap = {
        "anderson": game_log(ANDERSON),
        "bibee": game_log(BIBEE),
        "det_games": games,
        "det_starters": det_starter_lines(games),
        "standings": standings(),
        "det_pitching": team_pitching(DET),
        "cle_pitching": team_pitching(CLE),
        "league_pitching": league_pitching(),
    }
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=1)
    return snap


def ip(outs):
    return "%d.%d" % (outs // 3, outs % 3)


def main():
    snap = load(refresh="--refresh" in sys.argv)
    a = snap["anderson"]
    st = snap["standings"]

    print("== Drew Anderson, 2026 ==")
    outs = sum(x["outs"] for x in a)
    er = sum(x["er"] for x in a)
    bf = sum(x["bf"] for x in a)
    k = sum(x["k"] for x in a)
    bb = sum(x["bb"] for x in a)
    starts = [x for x in a if x["start"]]
    print(
        "  %d appearances, %d starts, %s IP, %.2f ERA, %d K, %d BB, %d BF"
        % (len(a), len(starts), ip(outs), er * 27.0 / outs, k, bb, bf)
    )
    print(
        "  K rate %.1f%%, BB rate %.1f%%, K/9 %.2f"
        % (100.0 * k / bf, 100.0 * bb / bf, 27.0 * k / outs)
    )
    print("  longest outing: %d batters faced, %s IP"
          % (max(x["bf"] for x in a), ip(max(x["outs"] for x in a))))
    print("  the three starts:")
    for s in starts:
        print(
            "    %s vs %-22s %s IP, %d ER, %d K, %d BF, %d pitches"
            % (s["date"], s["opp"], ip(s["outs"]), s["er"], s["k"], s["bf"],
               s["pitches"])
        )
    vs_cle = [x for x in a if x["opp"] == "Cleveland Guardians"]
    print("  vs Cleveland: %d outings, %s IP, %d ER, %d K"
          % (len(vs_cle), ip(sum(x["outs"] for x in vs_cle)),
             sum(x["er"] for x in vs_cle), sum(x["k"] for x in vs_cle)))

    print()
    print("== Tanner Bibee vs Detroit, 2026 ==")
    b = [x for x in snap["bibee"] if x["opp"] == "Detroit Tigers"]
    for x in b:
        print("    %s  %s IP, %d ER, %d H, %d BB, %d K"
              % (x["date"], ip(x["outs"]), x["er"], x["h"], x["bb"], x["k"]))
    bouts = sum(x["outs"] for x in b)
    print("  total %s IP, %d ER, ERA %.2f"
          % (ip(bouts), sum(x["er"] for x in b),
             sum(x["er"] for x in b) * 27.0 / bouts))
    allb = snap["bibee"]
    abouts = sum(x["outs"] for x in allb)
    print("  season: %d starts, %s IP, %.2f ERA, %d HR allowed (%.2f per 9)"
          % (len(allb), ip(abouts), sum(x["er"] for x in allb) * 27.0 / abouts,
             sum(x["hr"] for x in allb),
             27.0 * sum(x["hr"] for x in allb) / abouts))

    print()
    print("== Detroit starters, 2026 ==")
    lines = [x for x in snap["det_starters"] if x["bf"]]
    bfs = sorted(x["bf"] for x in lines)
    print("  %d starts, median %d batters faced, mean %.1f"
          % (len(bfs), statistics.median(bfs), statistics.mean(bfs)))
    print("  starts of 18 batters faced or fewer: %d of %d (%.0f%%)"
          % (sum(1 for x in bfs if x <= 18), len(bfs),
             100.0 * sum(1 for x in bfs if x <= 18) / len(bfs)))
    print("  starter outs per game: median %.1f (%.2f innings)"
          % (statistics.median([x["outs"] for x in lines]),
             statistics.median([x["outs"] for x in lines]) / 3.0))
    print("  the chart's bins, as a table (the accessible view):")
    lo = 2 * (min(bfs) // 2)
    for b in range(lo, max(bfs) + 1, 2):
        c = sum(1 for v in bfs if b <= v <= b + 1)
        if c:
            print("    | %d to %d | %d |" % (b, b + 1, c))

    print()
    print("== Head to head and standings ==")
    h2h = [g for g in snap["det_games"]
           if CLE in (g["away_id"], g["home_id"])]
    dw = dl = drs = dra = 0
    for g in h2h:
        det_home = g["home_id"] == DET
        ds = g["home_score"] if det_home else g["away_score"]
        cs = g["away_score"] if det_home else g["home_score"]
        drs += ds
        dra += cs
        if ds > cs:
            dw += 1
        else:
            dl += 1
    print("  Detroit %d-%d vs Cleveland, %d runs scored, %d allowed" % (dw, dl, drs, dra))
    print("  Detroit scored %.2f/g in the matchup, Cleveland scored %.2f/g"
          % (float(drs) / len(h2h), float(dra) / len(h2h)))
    for name in ("Detroit Tigers", "Cleveland Guardians"):
        s = st[name]
        print("  %-20s %d-%d, %+d run diff, %.2f runs scored/g, %.2f allowed/g"
              % (name, s["w"], s["l"], s["diff"], float(s["rs"]) / s["g"],
                 float(s["ra"]) / s["g"]))
        print("      home %s, away %s, last ten %s, %s back of a wild card"
              % (s["splits"].get("home"), s["splits"].get("away"),
                 s["splits"].get("lastTen"), s["wcgb"]))
    # where those offenses rank
    rs = sorted(((float(v["rs"]) / v["g"], n) for n, v in st.items()),
                reverse=True)
    for i, (rate, n) in enumerate(rs, 1):
        if n in ("Detroit Tigers", "Cleveland Guardians"):
            print("  %-20s ranks %d of %d in runs per game (%.2f)"
                  % (n, i, len(rs), rate))

    print()
    print("== Detroit bullpen ==")
    p = snap["det_pitching"]
    print("  %s saves, %s blown, %.0f%% conversion, %s team ERA"
          % (p["saves"], p["blownSaves"],
             100.0 * int(p["saves"]) / (int(p["saves"]) + int(p["blownSaves"])),
             p["era"]))
    print("  Cleveland team ERA %s" % snap["cle_pitching"]["era"])
    conv = sorted(
        (float(t["saves"]) / (t["saves"] + t["blown"]), t["team"])
        for t in snap["league_pitching"]
    )
    for i, (rate, name) in enumerate(conv, 1):
        if i <= 2 or name == "Detroit Tigers":
            print("  save conversion rank %d of %d: %-22s %.1f%%"
                  % (i, len(conv), name, 100.0 * rate))

    print()
    print("== Openers in the short-start tail ==")
    short = sorted((x for x in snap["det_starters"] if x["bf"]),
                   key=lambda r: r["bf"])
    print("  starts of 5 batters faced or fewer: %d"
          % sum(1 for x in short if x["bf"] <= 5))
    for x in short[:6]:
        print("    %s %-18s %d BF, %d outs"
              % (x["date"], x["pitcher"], x["bf"], x["outs"]))


if __name__ == "__main__":
    main()
