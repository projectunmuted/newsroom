#!/usr/bin/env python3
"""Compare 2 bullpens on the things that actually decide a series.

Written 2026-08-14 for Tigers and White Sox, but the teams are arguments. The
series preview ended on the line that a bad Sunday "might lead to a lot of
bullpen innings", which is a claim nobody had checked.

The measures here, and why each one is in:

- **Relief ERA and WHIP.** The baseline. Necessary, not sufficient: a bullpen
  can post a good ERA in games nobody was leading.
- **Inherited runners scored.** The one that separates relievers who put out
  fires from relievers who inherit clean innings. A staff whose starters go 5
  hands over more traffic, and this is the only stat that prices it.
- **Blown saves against save opportunities.** Converting is the job.
- **Holds.** Credits the setup innings a save total ignores entirely.
- **Share of team innings.** A bullpen throwing 45% of a staff's innings is a
  different animal from one throwing 35%, regardless of its ERA, because the
  question in a 3-game series is whether it is already tired.

A pitcher counts as a reliever here if more than half his appearances came in
relief, and his *whole* line is then attributed to the bullpen. That is the
honest simple rule; an opener or a swingman muddies it, and the script prints
anyone whose split is close so the ambiguity is visible rather than hidden.

    python scripts/bullpen_compare.py --teams DET CWS
    python scripts/bullpen_compare.py --teams DET CWS --json
"""

from __future__ import annotations

import argparse
import json
import urllib.request

API = "https://statsapi.mlb.com/api/v1"
TEAMS = {
    "DET": (116, "Tigers"), "CWS": (145, "White Sox"), "CLE": (114, "Guardians"),
    "MIN": (142, "Twins"), "KC": (118, "Royals"), "NYY": (147, "Yankees"),
    "BOS": (111, "Red Sox"), "TOR": (141, "Blue Jays"), "BAL": (110, "Orioles"),
    "TB": (139, "Rays"), "HOU": (117, "Astros"), "SEA": (136, "Mariners"),
    "TEX": (140, "Rangers"), "LAA": (108, "Angels"), "ATH": (133, "Athletics"),
}


def get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "dsr-bullpen"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def outs(ip: str) -> int:
    """'5.2' is 5 innings and 2 outs, not 5.2 innings."""
    whole, _, frac = str(ip).partition(".")
    return int(whole or 0) * 3 + int(frac or 0)


def fmt_ip(n: int) -> str:
    return f"{n // 3}.{n % 3}"


def staff(team_id: int) -> tuple[list[dict], list[dict]]:
    d = get(f"{API}/teams/{team_id}/roster?rosterType=fullSeason&season=2026"
            f"&hydrate=person(stats(type=season,group=pitching,season=2026))")
    pen, rot = [], []
    for r in d["roster"]:
        st = r["person"].get("stats") or []
        if not st:
            continue
        sp = st[0].get("splits") or []
        if not sp:
            continue
        s = sp[0]["stat"]
        g = s.get("gamesPitched") or s.get("gamesPlayed") or 0
        gs = s.get("gamesStarted") or 0
        if not g:
            continue
        row = {
            "name": r["person"]["fullName"], "g": g, "gs": gs,
            "outs": outs(s.get("inningsPitched", "0.0")),
            "er": s.get("earnedRuns", 0), "h": s.get("hits", 0),
            "bb": s.get("baseOnBalls", 0), "so": s.get("strikeOuts", 0),
            "hr": s.get("homeRuns", 0),
            "ir": s.get("inheritedRunners", 0),
            "irs": s.get("inheritedRunnersScored", 0),
            "sv": s.get("saves", 0), "svo": s.get("saveOpportunities", 0),
            "bs": s.get("blownSaves", 0), "hld": s.get("holds", 0),
            "era": s.get("era"), "whip": s.get("whip"),
        }
        # More than half his outings in relief makes him a reliever. Anyone
        # inside 20 points of the line gets flagged rather than quietly bucketed.
        row["relief_share"] = (g - gs) / g
        (pen if row["relief_share"] > 0.5 else rot).append(row)
    return pen, rot


def totals(rows: list[dict]) -> dict:
    t = {k: sum(r[k] for r in rows)
         for k in ("g", "outs", "er", "h", "bb", "so", "hr", "ir", "irs",
                   "sv", "svo", "bs", "hld")}
    ip = t["outs"] / 3
    t["ip"] = fmt_ip(t["outs"])
    t["era"] = round(t["er"] * 9 / ip, 2) if ip else None
    t["whip"] = round((t["h"] + t["bb"]) / ip, 2) if ip else None
    t["k9"] = round(t["so"] * 9 / ip, 1) if ip else None
    t["bb9"] = round(t["bb"] * 9 / ip, 1) if ip else None
    t["hr9"] = round(t["hr"] * 9 / ip, 2) if ip else None
    t["irs_pct"] = round(t["irs"] * 100 / t["ir"], 1) if t["ir"] else None
    t["sv_pct"] = round(t["sv"] * 100 / t["svo"], 1) if t["svo"] else None
    return t


def league_saves() -> list[tuple[float, str, int, int, int]]:
    """Every team's save conversion, worst first.

    Taken from the team endpoint rather than summed off rosters, because that
    is the authoritative line and the 2 disagree by a save or so: a starter can
    record a save, and a full-season roster carries players who have since left.
    Rate stats above come from the roster, since only that can separate the
    bullpen from the rotation. Both sources are named wherever a number is used.
    """
    d = get(f"{API}/teams/stats?season=2026&group=pitching&stats=season"
            f"&sportId=1&gameType=R")
    rows = []
    for s in d["stats"][0]["splits"]:
        st = s["stat"]
        sv, svo = st.get("saves", 0), st.get("saveOpportunities", 0)
        if svo:
            rows.append((sv * 100 / svo, s["team"]["name"], sv, svo,
                         st.get("blownSaves", 0)))
    rows.sort()
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--teams", nargs=2, default=["DET", "CWS"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--league", action="store_true",
                    help="rank both teams' save conversion against all 30")
    a = ap.parse_args()

    out = {}
    for code in a.teams:
        tid, name = TEAMS[code.upper()]
        pen, rot = staff(tid)
        pt, rt = totals(pen), totals(rot)
        share = round(pt["outs"] * 100 / (pt["outs"] + rt["outs"]), 1)
        out[code.upper()] = {
            "name": name, "bullpen": pt, "rotation": rt,
            "bullpen_share_of_innings": share,
            "arms": sorted(pen, key=lambda r: -r["outs"]),
            "borderline": [r["name"] for r in pen + rot
                           if 0.3 < r["relief_share"] < 0.7],
        }

    if a.json:
        print(json.dumps(out, indent=1))
        return

    for code, d in out.items():
        p = d["bullpen"]
        print(f"\n{d['name']} bullpen")
        print(f"  {p['ip']} IP over {p['g']} appearances, "
              f"{d['bullpen_share_of_innings']}% of all staff innings")
        print(f"  ERA {p['era']}   WHIP {p['whip']}   "
              f"K/9 {p['k9']}   BB/9 {p['bb9']}   HR/9 {p['hr9']}")
        print(f"  Inherited runners {p['ir']}, scored {p['irs']} "
              f"({p['irs_pct']}%)")
        print(f"  Saves {p['sv']}/{p['svo']} ({p['sv_pct']}%), "
              f"blown {p['bs']}, holds {p['hld']}")
        if d["borderline"]:
            print(f"  Swingmen, counted by the >50% rule: "
                  f"{', '.join(d['borderline'])}")
        print("  Busiest arms:")
        for r in d["arms"][:5]:
            print(f"    {r['name']:<22} {fmt_ip(r['outs']):>6} IP  "
                  f"{r['g']:>2} G  ERA {r['era']:>5}  WHIP {r['whip']:>5}  "
                  f"IR {r['ir']:>2}/{r['irs']:<2}")

    if len(out) == 2:
        (c1, d1), (c2, d2) = out.items()
        print(f"\nHead to head, {d1['name']} first:")
        for lab, key in (("relief ERA", "era"), ("WHIP", "whip"),
                         ("K/9", "k9"), ("BB/9", "bb9"),
                         ("inherited scored %", "irs_pct"),
                         ("save conversion %", "sv_pct")):
            print(f"  {lab:<20} {d1['bullpen'][key]:>6}   {d2['bullpen'][key]:>6}")
        print(f"  {'share of innings':<20} "
              f"{d1['bullpen_share_of_innings']:>6}   "
              f"{d2['bullpen_share_of_innings']:>6}")

    if a.league:
        rows = league_saves()
        mean = sum(r[0] for r in rows) / len(rows)
        names = {d["name"] for d in out.values()}
        print(f"\nSave conversion, all 30 teams. League mean {mean:.1f}%")
        for i, (pct, nm, sv, svo, bs) in enumerate(rows, 1):
            mine = any(n in nm for n in names)
            if mine or i <= 3 or i > len(rows) - 3:
                mark = " <-" if mine else ""
                print(f"  {i:>2}. {nm:<24} {sv:>2}/{svo:<3} {pct:5.1f}%  "
                      f"blown {bs}{mark}")


if __name__ == "__main__":
    main()
