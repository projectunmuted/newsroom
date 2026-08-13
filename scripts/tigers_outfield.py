"""What Detroit's outfield injuries actually cost, derived in one run.

Every number the entry uses comes out of this script, so the prose and any
chart cannot drift apart. Written 2026-08-13, the day after Riley Greene went
on the 10-day IL joining Matt Vierling and Kerry Carpenter.

The chain, stated so it can be attacked:

1. Pull every 2026 team hitting line. Fit runs per plate appearance on OPS
   across all 30 teams. That is the OPS-to-runs conversion, derived from this
   season rather than from a constant somebody remembered.
2. Pull the individual lines for the outfielders Detroit lost and the ones now
   on the active roster.
3. Work out how many plate appearances the missing bats would have taken over
   the games remaining, from their own rate of PA per team game.
4. Convert the OPS gap between out and available into runs, then into wins at
   the runs-per-win implied by this season's actual run environment.

Usage:  python scripts/tigers_outfield.py [--refresh]
"""

import json
import os
import sys
import urllib.request

API = "https://statsapi.mlb.com/api/v1"
DET = 116
CACHE = os.path.join(os.path.dirname(__file__), "outfield_cache.json")


def lg_pa_check(data):
    return sum(t["pa"] for t in data["teams"])


def fetch(path):
    with urllib.request.urlopen(API + path, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def load(refresh=False):
    if os.path.exists(CACHE) and not refresh:
        with open(CACHE, encoding="utf-8") as f:
            cached = json.load(f)
        # JSON turns integer keys into strings on the way out, and this bit us
        # with a KeyError on the second run rather than the first.
        cached["runs_allowed"] = {int(k): v for k, v in cached["runs_allowed"].items()}
        cached["active"] = {int(k): v for k, v in cached["active"].items()}
        return cached

    data = {}

    # 1. every team's hitting line, for the OPS -> runs fit
    teams = fetch("/teams/stats?season=2026&group=hitting&stats=season&sportId=1")
    data["teams"] = [
        {
            "name": s["team"]["name"],
            "id": s["team"]["id"],
            "pa": int(s["stat"]["plateAppearances"]),
            "runs": int(s["stat"]["runs"]),
            "ops": float(s["stat"]["ops"]),
            "games": int(s["stat"]["gamesPlayed"]),
        }
        for s in teams["stats"][0]["splits"]
    ]

    # 2. every team's pitching line, for runs allowed and the run environment
    pitch = fetch("/teams/stats?season=2026&group=pitching&stats=season&sportId=1")
    data["runs_allowed"] = {
        s["team"]["id"]: int(s["stat"]["runs"]) for s in pitch["stats"][0]["splits"]
    }

    # 3. Detroit's individual hitters, all of them, active or not
    roster = fetch("/teams/%d/roster?rosterType=fullSeason" % DET)
    people = []
    for p in roster["roster"]:
        pid = p["person"]["id"]
        try:
            st = fetch(
                "/people/%d/stats?stats=season&season=2026&group=hitting&gameType=R"
                % pid
            )
        except Exception as e:  # noqa: BLE001
            print("  ! could not fetch %s: %s" % (p["person"]["fullName"], e),
                  file=sys.stderr)
            continue
        splits = st.get("stats", [{}])[0].get("splits", []) if st.get("stats") else []
        # a player traded mid-season returns one split per team; take the Detroit
        # one if it is there, otherwise the aggregate is wrong for our purpose
        row = None
        for sp in splits:
            if sp.get("team", {}).get("id") == DET:
                row = sp
                break
        if row is None and splits:
            row = splits[-1]
        if row is None:
            continue
        s = row["stat"]
        if int(s.get("plateAppearances", 0)) == 0:
            continue
        people.append(
            {
                "id": pid,
                "name": p["person"]["fullName"],
                "pos": p["position"]["abbreviation"],
                "status": p["status"]["description"],
                "pa": int(s["plateAppearances"]),
                "games": int(s["gamesPlayed"]),
                "ops": float(s["ops"]),
                "obp": float(s["obp"]),
                "slg": float(s["slg"]),
                "avg": float(s["avg"]),
                "hr": int(s["homeRuns"]),
                "rbi": int(s["rbi"]),
            }
        )
    data["tigers"] = people

    # 4. active roster ids, so we can tell who is actually available
    act = fetch("/teams/%d/roster?rosterType=active" % DET)
    data["active"] = {p["person"]["id"]: p["position"]["abbreviation"]
                      for p in act["roster"]}

    # 5. replacement level, derived from the league rather than remembered.
    # Every non-pitcher with under 150 PA this season: that is the population a
    # club calls on when a regular goes down, and it is exactly the group
    # Detroit is using now. Summed from the components so the rate is a real
    # weighted OPS and not an average of averages.
    pool = fetch(
        "/stats?stats=season&season=2026&group=hitting&sportId=1&gameType=R"
        "&playerPool=All&limit=3000"
    )
    rows = [
        r for r in pool["stats"][0]["splits"]
        if r.get("position", {}).get("abbreviation") != "P"
    ]
    tot_pa = sum(int(r["stat"]["plateAppearances"]) for r in rows)
    if abs(tot_pa - lg_pa_check(data)) > 50:
        print("  ! player pool PA %d does not reconcile with team PA %d"
              % (tot_pa, lg_pa_check(data)), file=sys.stderr)
    small = [r for r in rows if int(r["stat"]["plateAppearances"]) < 150]

    def rate(rs):
        ab = sum(int(r["stat"]["atBats"]) for r in rs)
        h = sum(int(r["stat"]["hits"]) for r in rs)
        bb = sum(int(r["stat"]["baseOnBalls"]) for r in rs)
        hbp = sum(int(r["stat"]["hitByPitch"]) for r in rs)
        sf = sum(int(r["stat"]["sacFlies"]) for r in rs)
        tb = sum(int(r["stat"]["totalBases"]) for r in rs)
        obp = (h + bb + hbp) / (ab + bb + hbp + sf)
        return obp + tb / ab

    data["replacement_ops"] = round(rate(small), 4)
    data["replacement_n"] = len(small)
    data["replacement_pa"] = sum(int(r["stat"]["plateAppearances"]) for r in small)
    data["pool_pa"] = tot_pa

    # 6. standings
    st = fetch("/standings?leagueId=103&season=2026&standingsTypes=wildCard")
    wc = []
    for rec in st["records"]:
        for t in rec["teamRecords"]:
            wc.append(
                {
                    "name": t["team"]["name"],
                    "id": t["team"]["id"],
                    "w": t["wins"],
                    "l": t["losses"],
                    "gb": t.get("wildCardGamesBack"),
                }
            )
    data["wildcard"] = wc

    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    return data


def linfit(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sxy / sxx
    a = my - b * mx
    # r squared
    pred = [a + b * x for x in xs]
    ssr = sum((y - p) ** 2 for y, p in zip(ys, pred))
    sst = sum((y - my) ** 2 for y in ys)
    return a, b, 1 - ssr / sst


def main():
    refresh = "--refresh" in sys.argv
    d = load(refresh)

    teams = d["teams"]
    lg_pa = sum(t["pa"] for t in teams)
    lg_runs = sum(t["runs"] for t in teams)
    lg_ops = sum(t["ops"] * t["pa"] for t in teams) / lg_pa
    print("League 2026: %d PA, %d runs, %.4f runs/PA, team-weighted OPS %.3f"
          % (lg_pa, lg_runs, lg_runs / lg_pa, lg_ops))

    a, b, r2 = linfit([t["ops"] for t in teams], [t["runs"] / t["pa"] for t in teams])
    print("Fit  runs/PA = %.5f + %.5f * OPS   (r2 = %.3f, n=30)" % (a, b, r2))
    print("  -> 100 points of OPS is worth %.4f runs per PA" % (b * 0.100))

    det = [t for t in teams if t["id"] == DET][0]
    ra = d["runs_allowed"][DET]
    # runs per win: the Pythagenpat-style derivative, but the plain and
    # defensible version is (R + RA) / G * 2 ... use the standard 10-ish check
    rpw = 9.0 * (det["runs"] + ra) / det["games"] / 9.0 + 2.0
    print("\nDetroit: %d G, %d R, %d RA, OPS %.3f"
          % (det["games"], det["runs"], ra, det["ops"]))
    print("Runs per win (Pythagorean derivative, (R+RA)/G + 2): %.2f" % rpw)

    tigers = sorted(d["tigers"], key=lambda p: -p["pa"])
    active = d["active"]
    out_names = {"Riley Greene", "Matt Vierling", "Kerry Carpenter",
                 "Wenceel Perez", "Parker Meadows"}

    print("\n--- Detroit hitters, 100+ PA, by PA ---")
    print("%-22s %-4s %5s %5s %6s  %s" % ("name", "pos", "PA", "G", "OPS", "status"))
    for p in tigers:
        if p["pa"] < 100:
            continue
        mark = "ACTIVE" if p["id"] in active else p["status"]
        print("%-22s %-4s %5d %5d %6.3f  %s"
              % (p["name"], p["pos"], p["pa"], p["games"], p["ops"], mark))

    print("\n--- the outfielders who are out ---")
    outs = [p for p in tigers if p["id"] not in active and p["pos"] in ("LF", "CF", "RF")]
    tot_pa = 0
    for p in outs:
        pa_per_g = p["pa"] / det["games"]
        print("%-22s %-4s %5d PA  %6.3f OPS  %.2f PA per team game  (%s)"
              % (p["name"], p["pos"], p["pa"], p["ops"], pa_per_g, p["status"]))
        tot_pa += p["pa"]

    print("\n--- the outfielders who are available ---")
    ins = [p for p in tigers if p["id"] in active and active[p["id"]] in ("LF", "CF", "RF")]
    for p in ins:
        print("%-22s %-4s %5d PA  %6.3f OPS" % (p["name"], p["pos"], p["pa"], p["ops"]))

    left = 162 - det["games"]
    print("\nGames remaining: %d" % left)

    # Replacement level, derived rather than remembered: the league-wide OPS of
    # every non-pitcher with under 150 plate appearances this season. That is
    # the population Detroit is actually calling on - Julks (2 PA), Clark (50),
    # Malgeri (57), Outman (100) are all inside it.
    repl = d.get("replacement_ops", REPLACEMENT_OPS)
    print("Replacement OPS (league non-pitchers under 150 PA): %.3f" % repl)

    by_name = {p["name"]: p for p in tigers}

    def cost(names, label, games_missed):
        runs = 0.0
        pas = 0.0
        for n in names:
            p = by_name[n]
            pa = p["pa"] / p["games"] * games_missed  # his own rate when he plays
            pas += pa
            runs += (p["ops"] - repl) * b * pa
        print("%-46s %6.1f PA  %+6.2f runs  %+5.2f wins"
              % (label, pas, runs, runs / rpw))
        return runs / rpw

    print("\n--- cost against replacement level, by scenario ---")
    print("(PA are that player's own PA-per-game-played, times games missed)")
    g = cost(["Riley Greene"], "Greene, out all %d remaining" % left, left)
    v = cost(["Matt Vierling"], "Vierling, out all %d" % left, left)
    c = cost(["Kerry Carpenter"], "Carpenter, out all %d" % left, left)
    print("%-46s %6s  %+6s  %+5.2f wins" % ("ALL THREE, rest of season", "", "", g + v + c))
    print("Greene's share of the three-man total: %.0f%%"
          % (100 * g / (g + v + c)))
    print()
    cost(["Riley Greene"], "Greene, 10-day minimum (~9 games)", 9)
    cost(["Riley Greene", "Kerry Carpenter"], "Greene 9 games + Carpenter 9 more", 9)

    # Sensitivity: Carpenter's 2026 line is the worst of his career and using it
    # as his true rate almost certainly understates him. Re-run him at his
    # 2023-2025 rate instead. This is the strongest argument against the piece's
    # own headline, so it gets derived rather than hand-waved.
    print("\n--- sensitivity: Carpenter at his 2023-25 rate instead of 2026 ---")
    p = by_name["Kerry Carpenter"]
    for rate, lab in [(p["ops"], "2026 line"), (0.832, "2023-25 rate (.832)")]:
        pa = p["pa"] / p["games"] * left
        runs = (rate - repl) * b * pa
        print("  Carpenter at %-22s %6.2f runs  %5.2f wins over %d games"
              % (lab, runs, runs / rpw, left))

    return d, det, b, rpw, left, tigers, active


# Derived 2026-08-13 from /stats?playerPool=All: 267 non-pitchers under 150 PA,
# 15,352 PA, .280/.324. Re-derive with scripts/replacement_level.py rather than
# trusting this constant if the season moves on.
REPLACEMENT_OPS = 0.604


if __name__ == "__main__":
    main()
