#!/usr/bin/env python3
"""Everything a Tigers series preview needs, from one run, for any opponent.

`det_cle_series.py` did this for Cleveland with the opponent id hardcoded, and
when the White Sox series arrived on 2026-08-14 there was no script for it, so
no preview got written even though `CALENDAR.md` had the slot. This is that
script with the opponent as an argument, so the next series is a command rather
than a project.

The rule it inherits and keeps: **every number in the prose comes out of one
execution of this file.** Nothing read off a box score by eye, nothing
re-derived in a second pass. Two passes disagreed once and that is why.

    python scripts/series_preview.py --opp CWS
    python scripts/series_preview.py --opp CLE --json

Prints the season series, both teams' recent form, the standings gap, and the
probable pitchers for the upcoming games with each starter's season line.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from collections import defaultdict
from datetime import date, timedelta

API = "https://statsapi.mlb.com/api/v1"
DET = 116

# Team ids are stable in the MLB API. Only the ones Detroit plays enough to
# preview are here; --oppid takes anything else.
OPPS = {
    "CLE": (114, "Guardians"), "CWS": (145, "White Sox"),
    "MIN": (142, "Twins"), "KC": (118, "Royals"),
    "NYY": (147, "Yankees"), "BOS": (111, "Red Sox"),
    "TOR": (141, "Blue Jays"), "BAL": (110, "Orioles"),
    "TB": (139, "Rays"), "HOU": (117, "Astros"),
    "SEA": (136, "Mariners"), "TEX": (140, "Rangers"),
    "LAA": (108, "Angels"), "ATH": (133, "Athletics"),
    "PIT": (134, "Pirates"), "LAD": (119, "Dodgers"),
}


def get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "dsr-preview"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def season_series(opp_id: int) -> tuple[list[dict], list[dict]]:
    """Games played and games still to come between the two clubs."""
    sched = get(f"{API}/schedule?sportId=1&teamId={DET}&opponentId={opp_id}"
                f"&startDate=2026-03-01&endDate=2026-11-01&gameType=R"
                f"&hydrate=probablePitcher,linescore")
    played, upcoming, seen = [], [], set()
    for d in sched.get("dates", []):
        for g in d["games"]:
            # A postponed game keeps "Final" on its original date with no score
            # and reappears on the makeup date. Status alone would count it as
            # a game that was never played.
            scored = (g["teams"]["away"].get("score") is not None
                      and g["teams"]["home"].get("score") is not None)
            home_is_det = g["teams"]["home"]["team"]["id"] == DET
            row = {
                "pk": g["gamePk"], "date": d["date"], "home": home_is_det,
                "det_r": g["teams"]["home" if home_is_det else "away"].get("score"),
                "opp_r": g["teams"]["away" if home_is_det else "home"].get("score"),
                "det_sp": (g["teams"]["home" if home_is_det else "away"]
                           .get("probablePitcher", {}) or {}).get("fullName"),
                "opp_sp": (g["teams"]["away" if home_is_det else "home"]
                           .get("probablePitcher", {}) or {}).get("fullName"),
                "det_spid": (g["teams"]["home" if home_is_det else "away"]
                             .get("probablePitcher", {}) or {}).get("id"),
                "opp_spid": (g["teams"]["away" if home_is_det else "home"]
                             .get("probablePitcher", {}) or {}).get("id"),
                "time": g.get("gameDate"),
            }
            if g["status"]["abstractGameState"] == "Final" and scored:
                played.append(row)
            elif g["status"]["abstractGameState"] != "Final":
                if row["pk"] not in seen:
                    seen.add(row["pk"])
                    upcoming.append(row)
    return played, upcoming


def record(team_id: int, days: int | None = None) -> tuple[int, int]:
    """Wins and losses, whole season or the last `days` days."""
    start = "2026-03-01"
    if days:
        start = (date.today() - timedelta(days=days)).isoformat()
    sched = get(f"{API}/schedule?sportId=1&teamId={team_id}&startDate={start}"
                f"&endDate={date.today().isoformat()}&gameType=R")
    w = l = 0
    for d in sched.get("dates", []):
        for g in d["games"]:
            if g["status"]["abstractGameState"] != "Final":
                continue
            home_is = g["teams"]["home"]["team"]["id"] == team_id
            us = g["teams"]["home" if home_is else "away"]
            them = g["teams"]["away" if home_is else "home"]
            if us.get("score") is None or them.get("score") is None:
                continue
            if us["score"] > them["score"]:
                w += 1
            else:
                l += 1
    return w, l


def pitcher_line(pid: int | None) -> dict:
    if not pid:
        return {}
    d = get(f"{API}/people/{pid}?hydrate=stats(group=pitching,type=season,"
            f"season=2026)")
    people = d.get("people") or [{}]
    splits = ((people[0].get("stats") or [{}])[0].get("splits") or [{}])
    s = splits[0].get("stat", {}) if splits else {}
    return {
        "name": people[0].get("fullName"),
        "era": s.get("era"), "whip": s.get("whip"), "ip": s.get("inningsPitched"),
        "g": s.get("gamesPlayed"), "gs": s.get("gamesStarted"),
        "so": s.get("strikeOuts"), "bb": s.get("baseOnBalls"),
        "w": s.get("wins"), "l": s.get("losses"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--opp", default="CWS", help="team code, e.g. CWS")
    ap.add_argument("--oppid", type=int, help="raw MLB team id, overrides --opp")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.oppid:
        opp_id, opp_name = a.oppid, f"team {a.oppid}"
    else:
        if a.opp.upper() not in OPPS:
            raise SystemExit(f"unknown --opp {a.opp}; add it to OPPS or use --oppid")
        opp_id, opp_name = OPPS[a.opp.upper()]

    played, upcoming = season_series(opp_id)
    det_w, det_l = record(DET)
    opp_w, opp_l = record(opp_id)
    det10 = record(DET, 14)
    opp10 = record(opp_id, 14)

    det_runs = sum(g["det_r"] for g in played)
    opp_runs = sum(g["opp_r"] for g in played)
    det_wins = sum(1 for g in played if g["det_r"] > g["opp_r"])

    out = {
        "opponent": opp_name,
        "season_records": {"det": [det_w, det_l], "opp": [opp_w, opp_l]},
        "last_14_days": {"det": list(det10), "opp": list(opp10)},
        "head_to_head": {
            "played": len(played), "det_wins": det_wins,
            "opp_wins": len(played) - det_wins,
            "det_runs": det_runs, "opp_runs": opp_runs,
            "det_rpg": round(det_runs / len(played), 2) if played else None,
            "opp_rpg": round(opp_runs / len(played), 2) if played else None,
            "games": [{"date": g["date"], "det": g["det_r"], "opp": g["opp_r"],
                       "home": g["home"]} for g in played],
        },
        "upcoming": [],
    }
    for g in upcoming[:4]:
        out["upcoming"].append({
            "date": g["date"], "pk": g["pk"], "home": g["home"],
            "first_pitch_utc": g["time"],
            "det_sp": pitcher_line(g["det_spid"]) or {"name": g["det_sp"]},
            "opp_sp": pitcher_line(g["opp_spid"]) or {"name": g["opp_sp"]},
        })

    if a.json:
        print(json.dumps(out, indent=1))
        return

    print(f"Tigers vs {opp_name}\n")
    print(f"  Detroit  {det_w}-{det_l}   last 14 days {det10[0]}-{det10[1]}")
    print(f"  {opp_name:<9}{opp_w}-{opp_l}   last 14 days {opp10[0]}-{opp10[1]}\n")
    print(f"  Season series: Detroit {det_wins}-{len(played) - det_wins}, "
          f"runs {det_runs}-{opp_runs} "
          f"({out['head_to_head']['det_rpg']} to {out['head_to_head']['opp_rpg']} "
          f"per game)")
    for g in played:
        where = "home" if g["home"] else "away"
        print(f"    {g['date']}  {g['det_r']}-{g['opp_r']}  {where}")
    print("\n  Upcoming:")
    for g in out["upcoming"]:
        d, o = g["det_sp"], g["opp_sp"]
        print(f"    {g['date']}  {o.get('name')} (ERA {o.get('era')}, "
              f"WHIP {o.get('whip')}, {o.get('gs')} GS) vs "
              f"{d.get('name')} (ERA {d.get('era')}, WHIP {d.get('whip')}, "
              f"{d.get('gs')} GS)")


if __name__ == "__main__":
    main()
