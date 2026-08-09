"""Everything that happened in the six Detroit-Cleveland games, from one run.

The rule this script exists to enforce: every number that appears in the prose
of the entry comes out of a single execution of this file, against the MLB
Stats API, matched by gamePk. Nothing is copied from a box score by eye and
nothing is re-derived later in a second run, because the last time numbers were
gathered in two passes the two passes disagreed.

Usage:
    python scripts/det_cle_series.py
"""

import json
import urllib.request
from collections import defaultdict

API = "https://statsapi.mlb.com/api/v1"
DET, CLE = 116, 114


def get(url):
    return json.load(urllib.request.urlopen(url))


def outs(ip_string):
    """'5.2' means five innings and two outs, not five and two tenths."""
    whole, _, frac = str(ip_string).partition(".")
    return int(whole) * 3 + int(frac or 0)


def fmt_ip(n_outs):
    return f"{n_outs // 3}.{n_outs % 3}"


def main():
    sched = get(
        f"{API}/schedule?sportId=1&teamId={DET}&opponentId={CLE}"
        f"&startDate=2026-03-01&endDate=2026-11-01&gameType=R"
    )

    played, upcoming = [], []
    for date in sched["dates"]:
        for g in date["games"]:
            row = {"pk": g["gamePk"], "date": date["date"],
                   "state": g["status"]["abstractGameState"]}
            # A postponed game keeps abstractGameState "Final" on its original
            # date with no score, and reappears on the date it was made up.
            # Status alone would count June 14 as a seventh loss that was
            # never played.
            scored = (g["teams"]["away"].get("score") is not None
                      and g["teams"]["home"].get("score") is not None)
            if row["state"] == "Final" and scored:
                played.append(row)
            elif row["state"] != "Final":
                upcoming.append(row)

    # gamePk is unique but a postponed game can appear on two dates.
    seen = set()
    upcoming = [g for g in upcoming if not (g["pk"] in seen or seen.add(g["pk"]))]

    print(f"Completed: {len(played)}   Remaining: {len(upcoming)}")

    tot = defaultdict(int)
    per_game = []

    for g in played:
        box = get(f"{API}/game/{g['pk']}/boxscore")
        line = get(f"{API}/game/{g['pk']}/linescore")

        home_is_det = box["teams"]["home"]["team"]["id"] == DET
        det = box["teams"]["home" if home_is_det else "away"]
        cle = box["teams"]["away" if home_is_det else "home"]

        det_r = det["teamStats"]["batting"]["runs"]
        cle_r = cle["teamStats"]["batting"]["runs"]

        # Split each staff into the starter and everyone after him.
        staff = {}
        for side, tag in ((det, "det"), (cle, "cle")):
            ids = side["pitchers"]
            starter_outs = reliever_outs = starter_er = reliever_er = 0
            for i, pid in enumerate(ids):
                s = side["players"]["ID%d" % pid]["stats"]["pitching"]
                o, er = outs(s.get("inningsPitched", 0)), s.get("earnedRuns", 0)
                if i == 0:
                    starter_outs += o
                    starter_er += er
                else:
                    reliever_outs += o
                    reliever_er += er
            staff[tag] = (starter_outs, starter_er, reliever_outs, reliever_er)
            tot[f"{tag}_sp_outs"] += starter_outs
            tot[f"{tag}_sp_er"] += starter_er
            tot[f"{tag}_rp_outs"] += reliever_outs
            tot[f"{tag}_rp_er"] += reliever_er

        db = det["teamStats"]["batting"]
        tot["det_r"] += det_r
        tot["cle_r"] += cle_r
        tot["det_h"] += db["hits"]
        tot["det_k"] += db["strikeOuts"]
        tot["det_bb"] += db["baseOnBalls"]
        tot["det_ab"] += db["atBats"]
        tot["det_lob"] += db["leftOnBase"]

        cle_sp = cle["players"]["ID%d" % cle["pitchers"][0]]["person"]["fullName"]

        # Did Detroit ever hold a lead after the sixth?
        det_key, cle_key = ("home", "away") if home_is_det else ("away", "home")
        d = c = 0
        lead_after_6 = False
        for inn in line["innings"]:
            d += inn[det_key].get("runs") or 0
            c += inn[cle_key].get("runs") or 0
            if inn["num"] >= 6 and d > c:
                lead_after_6 = True
        if lead_after_6:
            tot["lead_after_6"] += 1

        per_game.append(
            {"pk": g["pk"], "date": g["date"], "det_r": det_r, "cle_r": cle_r,
             "margin": cle_r - det_r, "cle_sp": cle_sp,
             "det_h": db["hits"], "det_k": db["strikeOuts"],
             "innings": len(line["innings"]), "lead_after_6": lead_after_6}
        )

    print("\n| Date | Game | Result | Margin | DET H | DET K | Cleveland starter |")
    print("|---|---|---|---|---|---|---|")
    for r in per_game:
        extra = f" ({r['innings']})" if r["innings"] != 9 else ""
        print(f"| {r['date']} | `{r['pk']}` | CLE {r['cle_r']}, DET {r['det_r']}{extra} "
              f"| {r['margin']} | {r['det_h']} | {r['det_k']} | {r['cle_sp']} |")

    n = len(played)
    print(f"\nDetroit: {tot['det_r']} runs in {n} games "
          f"({tot['det_r'] / n:.2f}/g), {tot['det_h']} hits, "
          f"{tot['det_k']} K in {tot['det_ab']} AB "
          f"({tot['det_k'] / tot['det_ab']:.1%}), {tot['det_bb']} BB, "
          f"{tot['det_lob']} LOB")
    print(f"Cleveland: {tot['cle_r']} runs ({tot['cle_r'] / n:.2f}/g)")
    print(f"Games Detroit led at any point from the 6th on: {tot['lead_after_6']}/{n}")

    for tag, label in (("det", "Detroit"), ("cle", "Cleveland")):
        for role in ("sp", "rp"):
            o, er = tot[f"{tag}_{role}_outs"], tot[f"{tag}_{role}_er"]
            era = er * 27 / o if o else 0
            print(f"{label:10s} {'starters' if role == 'sp' else 'bullpen ':9s} "
                  f"{fmt_ip(o):>5s} IP  {er:2d} ER  {era:.2f} ERA")

    # Season baselines to compare against.
    for tid, label in ((DET, "Detroit"), (CLE, "Cleveland")):
        h = get(f"{API}/teams/{tid}/stats?stats=season&group=hitting"
                f"&season=2026&gameType=R")["stats"][0]["splits"][0]["stat"]
        print(f"{label} season: {h['runs'] / h['gamesPlayed']:.2f} R/G, "
              f"{h['avg']} AVG, {h['ops']} OPS, "
              f"{h['strikeOuts'] / h['atBats']:.1%} K rate")

    print("\nRemaining games:")
    for g in upcoming:
        gg = get(f"{API}/schedule?gamePk={g['pk']}&hydrate=probablePitcher")
        game = gg["dates"][0]["games"][0]
        away = game["teams"]["away"].get("probablePitcher", {}).get("fullName", "TBD")
        home = game["teams"]["home"].get("probablePitcher", {}).get("fullName", "TBD")
        print(f"  `{g['pk']}` {game['gameDate']}  {away} vs {home}")


if __name__ == "__main__":
    main()
