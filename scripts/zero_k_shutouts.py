"""How rare is a shutout with zero strikeouts?

Scans every team's pitching game log, season by season, and finds games where a
staff allowed 0 runs, recorded 0 strikeouts, and got at least 24 outs.

Written for the 824238 grade: Detroit beat Cleveland 3-0 on 2026-08-13 and the
staff struck out nobody in 9 innings.

The counts come from the league's own game logs rather than a search summary,
one row per team-game, cached on disk so a re-run costs nothing.

Usage:
    python scripts/zero_k_shutouts.py [--from 2000] [--to 2026] [--refresh]
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "zero_k_shutouts_cache.json")
API = "https://statsapi.mlb.com/api/v1"


def fetch(url, tries=3):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == tries - 1:
                raise RuntimeError("failed: %s (%s)" % (url, exc))
            time.sleep(2 * (attempt + 1))


def teams_for(season):
    d = fetch("%s/teams?sportId=1&season=%d" % (API, season))
    return [(t["id"], t["name"]) for t in d.get("teams", [])]


def game_log(team_id, season):
    url = "%s/teams/%d/stats?stats=gameLog&group=pitching&season=%d&sportId=1" % (
        API,
        team_id,
        season,
    )
    d = fetch(url)
    stats = d.get("stats") or []
    if not stats:
        return []
    out = []
    for s in stats[0].get("splits", []):
        st = s["stat"]
        out.append(
            {
                "date": s.get("date"),
                "gamePk": s.get("game", {}).get("gamePk"),
                "opponent": s.get("opponent", {}).get("id"),
                "isHome": s.get("isHome"),
                "isWin": s.get("isWin"),
                "runs": st.get("runs"),
                "strikeOuts": st.get("strikeOuts"),
                "outs": st.get("outs"),
                "hits": st.get("hits"),
                "walks": st.get("baseOnBalls"),
                "battersFaced": st.get("battersFaced"),
                "ip": st.get("inningsPitched"),
            }
        )
    return out


def load_cache():
    if os.path.exists(CACHE):
        with open(CACHE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(c):
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(c, f)


def collect(first, last, refresh=False):
    cache = {} if refresh else load_cache()
    team_names = {}
    for season in range(first, last + 1):
        try:
            teams = teams_for(season)
        except RuntimeError as exc:
            print("  season %d: team list failed (%s), skipped" % (season, exc),
                  file=sys.stderr)
            continue
        for tid, name in teams:
            team_names[str(tid)] = name
            key = "%d-%d" % (season, tid)
            if key in cache:
                continue
            try:
                cache[key] = game_log(tid, season)
            except RuntimeError as exc:
                print("  %s failed (%s)" % (key, exc), file=sys.stderr)
                continue
        save_cache(cache)
        print("  %d done (%d teams)" % (season, len(teams)), file=sys.stderr)
    return cache, team_names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="first", type=int, default=2000)
    ap.add_argument("--to", dest="last", type=int, default=2026)
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    cache, names = collect(args.first, args.last, args.refresh)

    seen = set()
    hits = []
    team_games = 0
    shutouts = 0
    for key, rows in cache.items():
        season = int(key.split("-")[0])
        if not (args.first <= season <= args.last):
            continue
        tid = key.split("-")[1]
        for r in rows:
            pk = r.get("gamePk")
            ident = (tid, pk)
            if ident in seen:
                continue
            seen.add(ident)
            team_games += 1
            if r.get("runs") == 0 and (r.get("outs") or 0) >= 24:
                shutouts += 1
                if r.get("strikeOuts") == 0:
                    row = dict(r)
                    row["season"] = season
                    row["team"] = names.get(tid, tid)
                    hits.append(row)

    hits.sort(key=lambda r: r["date"] or "")
    print("Seasons %d-%d" % (args.first, args.last))
    print("Team-games scanned: %d" % team_games)
    print("Shutouts (0 runs allowed, 24+ outs): %d" % shutouts)
    print("Of those, with 0 strikeouts: %d" % len(hits))
    print()
    for r in hits:
        print(
            "  %s  %-22s %s  %s IP, %s H, %s BB, %s BF  (gamePk %s)"
            % (
                r["date"],
                r["team"],
                "home" if r["isHome"] else "away",
                r["ip"],
                r["hits"],
                r["walks"],
                r["battersFaced"],
                r["gamePk"],
            )
        )


if __name__ == "__main__":
    main()
