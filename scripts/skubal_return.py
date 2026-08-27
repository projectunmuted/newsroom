#!/usr/bin/env python3
"""Numbers for the Dodgers-at-Comerica series, 2026-08-28 to 08-30.

Tarik Skubal was traded to Los Angeles at the 2026 deadline and starts Friday
against the club he pitched for through July 29. Everything here is pulled
live from statsapi.mlb.com on every run and every intermediate value is
printed, so re-running the script IS the diff (WOODWARD-TODO, 2026-08-24).

Exit 2 if any pull came back short; a partial read is not a number.
"""
import json
import sys
import urllib.request

DET, LAD = 116, 119
SKUBAL = 669373
DEADLINE = "2026-07-31"
TODAY = "2026-08-27"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dsr-skubal"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def ip_to_outs(ip):
    """'94.1' is 94 innings and 1 out, not 94.1 innings. This is the trap."""
    whole, _, frac = str(ip).partition(".")
    return int(whole) * 3 + int(frac or 0)


def era(er, outs):
    return round(er * 27.0 / outs, 2) if outs else None


def team_split(team_id, label):
    """Record and runs either side of the deadline. Regular season only.

    'Completed Early' is a real, shortened game and counts; 'Postponed' carries
    abstractGameState Final and does not. Filtering on abstractGameState alone
    inflates the schedule by both.
    """
    url = (f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={team_id}"
           f"&startDate=2026-03-01&endDate={TODAY}&gameType=R")
    data = get(url)
    buckets = {"pre": [0, 0, 0, 0], "post": [0, 0, 0, 0]}
    for date in data["dates"]:
        for g in date["games"]:
            state = g["status"]["detailedState"]
            if state not in ("Final", "Completed Early"):
                continue
            home = g["teams"]["home"]["team"]["id"] == team_id
            us = g["teams"]["home" if home else "away"]
            them = g["teams"]["away" if home else "home"]
            if "score" not in us or "score" not in them:
                continue
            b = buckets["pre" if date["date"] <= DEADLINE else "post"]
            b[0] += us["score"] > them["score"]
            b[1] += us["score"] < them["score"]
            b[2] += us["score"]
            b[3] += them["score"]
    print(f"{label}, regular season only")
    for key, name in (("pre", f"through {DEADLINE}"), ("post", "since 08-01")):
        w, l, rs, ra = buckets[key]
        gp = w + l
        print(f"  {name:<18} {w}-{l}  ({gp} G)  RS {rs}  RA {ra}  diff {rs - ra:+d}"
              f"  win% {w / gp:.3f}" if gp else f"  {name}: no games")
    tot = [buckets["pre"][i] + buckets["post"][i] for i in range(4)]
    w, l, rs, ra = tot
    exp = rs ** 1.83 / (rs ** 1.83 + ra ** 1.83)
    print(f"  {'season':<18} {w}-{l}  ({w + l} G)  RS {rs}  RA {ra}  diff {rs - ra:+d}")
    print(f"  pythagorean  win% {exp:.3f}  expected {exp * (w + l):.1f} wins"
          f"  actual {w}  gap {w - exp * (w + l):+.1f}")
    return tot


def skubal():
    data = get(f"https://statsapi.mlb.com/api/v1/people/{SKUBAL}/stats"
               f"?stats=gameLog&group=pitching&season=2026")
    logs = data["stats"][0]["splits"]
    if len(logs) < 15:
        print(f"  only {len(logs)} starts returned, partial read", file=sys.stderr)
        return None
    agg = {}
    for g in logs:
        club = g["team"]["name"]
        s = g["stat"]
        a = agg.setdefault(club, {"gs": 0, "outs": 0, "er": 0, "k": 0, "bb": 0,
                                  "h": 0, "first": g["date"], "last": g["date"]})
        a["gs"] += 1
        a["outs"] += ip_to_outs(s["inningsPitched"])
        a["er"] += int(s["earnedRuns"])
        a["k"] += int(s["strikeOuts"])
        a["bb"] += int(s["baseOnBalls"])
        a["h"] += int(s["hits"])
        a["last"] = g["date"]
    print("\nTarik Skubal 2026, by club")
    for club, a in agg.items():
        ip = f"{a['outs'] // 3}.{a['outs'] % 3}"
        whip = round((a["bb"] + a["h"]) * 3.0 / a["outs"], 2)
        k9 = round(a["k"] * 27.0 / a["outs"], 1)
        print(f"  {club:<20} {a['gs']} GS  {ip} IP  {a['er']} ER  ERA {era(a['er'], a['outs'])}"
              f"  WHIP {whip}  K {a['k']} (K/9 {k9})  {a['first']} to {a['last']}")
    return agg


def probables():
    url = (f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={DET}"
           f"&startDate=2026-08-28&endDate=2026-08-30&hydrate=probablePitcher")
    data = get(url)
    print("\nThe series")
    rows = 0
    for date in data["dates"]:
        for g in data and date["games"]:
            a, h = g["teams"]["away"], g["teams"]["home"]
            print(f"  {date['date']}  gamePk {g['gamePk']}  "
                  f"{a['team']['name']} ({a.get('probablePitcher', {}).get('fullName', 'TBD')})"
                  f" at {h['team']['name']} ({h.get('probablePitcher', {}).get('fullName', 'TBD')})")
            rows += 1
    return rows


def main():
    det = team_split(DET, "Detroit")
    print()
    lad = team_split(LAD, "Los Angeles")
    sk = skubal()
    rows = probables()
    if not det or not lad or not sk or rows != 3:
        print("\nPartial read. Do not publish these numbers.", file=sys.stderr)
        return 2
    print("\nAll pulls complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
