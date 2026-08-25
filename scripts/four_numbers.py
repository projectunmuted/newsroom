"""Candidate numbers for the Monday column, one team at a time, pulled live.

`PLAN.md` M2 is a named recurring column at a fixed time, because the strongest
free return mechanism at small scale is a column on a known day. The subject
settled on 2026-08-25 is **one number for each of the four Detroit teams**,
whatever the most interesting one is that week. That shape was chosen over the
original candidate because the original was a weekly recap of the prediction
record, and there is a standing rule against writing about the record.

This script does not write the column. It does the part a cycle would otherwise
do by hand at 10am and get wrong: pull every candidate number for all four
clubs from a primary source in one run, print the arithmetic next to each one,
and say which ones decay overnight.

    python scripts/four_numbers.py
    python scripts/four_numbers.py --json
    python scripts/four_numbers.py --team wings

Nothing is hardcoded and there is no DATA block, per the standing rule in
`WOODWARD-TODO.md`: a frozen block is how a draft ended up carrying an ERA that
had moved. Re-running this is the diff.

Sources, all free and keyless:
  Tigers                     statsapi.mlb.com
  Lions / Pistons / Wings    site.api.espn.com public JSON

Exit codes, deliberately the same contract as `injury_check.py`:
  0  every fetch landed, the candidate list is complete
  2  at least one fetch failed, so a team is missing and the list is partial
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request

SEASON = 2026
EXP = 1.83  # Baseball Reference's MLB Pythagorean exponent

MLB_STANDINGS = ("https://statsapi.mlb.com/api/v1/standings"
                 "?leagueId=103,104&season={season}&standingsTypes=regularSeason")
MLB_TEAM_STATS = ("https://statsapi.mlb.com/api/v1/teams/{tid}/stats"
                  "?stats=season&group=pitching&season={season}&gameType=R")
MLB_SCHEDULE = ("https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId={tid}"
                "&startDate={start}&endDate={end}")
ESPN_TEAM = ("https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}"
             "/teams/det")
ESPN_SCHEDULE = ("https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}"
                 "/teams/det/schedule?season={season}&seasontype={stype}")

TIGERS_ID = 116

# season/seasontype per sport, because the three leagues label a season by
# different years. NFL preseason is seasontype 1 and the regular season is 2;
# the NBA labels 2025-26 as 2026 and the NHL labels it 2026 too, so the most
# recently completed season is what these fetch while the clubs are dark.
ESPN_TEAMS = [
    ("lions", "football", "nfl", 2026, 1),
    ("pistons", "basketball", "nba", 2026, 2),
    ("wings", "hockey", "nhl", 2026, 2),
]

failures: list[str] = []


def get(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def try_get(url: str, what: str):
    try:
        return get(url)
    except (urllib.error.URLError, OSError, ValueError) as e:
        failures.append(what + ": " + str(e))
        return None


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def days_until(iso):
    if not iso:
        return None
    try:
        d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return None
    return round((d - now()).total_seconds() / 86400, 1)


def cand(label: str, value, how: str, decays: str) -> dict:
    """One candidate number.

    `decays` is the shelf-life note the standing rule asks for: a column
    published Monday morning carrying a number that moved Sunday night is the
    same failure the drafts folder has already had twice.
    """
    return {"label": label, "value": value, "how": how, "decays": decays}


# ---------------------------------------------------------------- Tigers

def tigers():
    st = try_get(MLB_STANDINGS.format(season=SEASON), "MLB standings")
    if st is None:
        return None
    me = None
    league = []
    for record in st["records"]:
        for t in record["teamRecords"]:
            rs, ra = t.get("runsScored"), t.get("runsAllowed")
            if not rs or not ra:
                continue
            w, l = t["wins"], t["losses"]
            exp = (rs ** EXP) / ((rs ** EXP) + (ra ** EXP)) * (w + l)
            row = {"id": t["team"]["id"], "name": t["team"]["name"],
                   "w": w, "l": l, "rs": rs, "ra": ra,
                   "gap": round(w - exp, 1)}
            league.append(row)
            if t["team"]["id"] == TIGERS_ID:
                me = dict(row)
                me["raw"] = t
    if me is None:
        failures.append("MLB standings: Detroit not in the payload")
        return None

    t = me.pop("raw")
    splits = {s["type"]: str(s["wins"]) + "-" + str(s["losses"])
              for s in t["records"]["splitRecords"]}
    league.sort(key=lambda r: r["gap"])

    out = {"team": "Tigers", "record": str(me["w"]) + "-" + str(me["l"]),
           "candidates": []}
    c = out["candidates"]
    c.append(cand("Run differential", me["rs"] - me["ra"],
                  str(me["rs"]) + " scored, " + str(me["ra"]) + " allowed",
                  "every night there is a game"))
    rank = [r["id"] for r in league].index(TIGERS_ID) + 1
    c.append(cand("Wins above Pythagorean expectation", me["gap"],
                  "exponent " + str(EXP) + "; " + str(rank) + " of "
                  + str(len(league)) + " from the bottom",
                  "every night there is a game"))
    c.append(cand("Last 10", splits.get("lastTen"),
                  "streak " + t["streak"]["streakCode"],
                  "every night, and it is the fastest-moving number here"))
    c.append(cand("Home / road",
                  str(splits.get("home")) + " / " + str(splits.get("away")),
                  "split records from the standings payload",
                  "every night there is a game"))

    ps = try_get(MLB_TEAM_STATS.format(tid=TIGERS_ID, season=SEASON),
                 "MLB Tigers pitching")
    if ps:
        s = ps["stats"][0]["splits"][0]["stat"]
        saves, opps = s.get("saves"), s.get("saveOpportunities")
        if saves is not None and opps:
            c.append(cand("Bullpen save conversion",
                          str(saves) + " of " + str(opps),
                          str(s.get("blownSaves")) + " blown, team ERA "
                          + str(s.get("era")),
                          "only on a save chance, so slower than the rest"))

    today = now().date()
    sch = try_get(MLB_SCHEDULE.format(tid=TIGERS_ID, start=today,
                                      end=today + dt.timedelta(days=10)),
                  "MLB Tigers schedule")
    if sch:
        for d in sch["dates"]:
            for g in d["games"]:
                if g["status"]["detailedState"] in ("Scheduled", "Pre-Game"):
                    out["next_game"] = {"name": "gamePk " + str(g["gamePk"]),
                                        "when": g["gameDate"],
                                        "days": days_until(g["gameDate"])}
                    break
            if "next_game" in out:
                break
    return out


# ---------------------------------------------------------- the other three

def espn_schedule(sport: str, league: str, season: int, stype: int):
    """The completed record and the true next game, off the schedule endpoint.

    The team endpoint's `nextEvent` goes stale: on 2026-08-25 it still pointed
    at a Lions game that had finished 3 days earlier. Anything with a negative
    days-until is not a next game, so this walks the schedule instead.
    """
    d = try_get(ESPN_SCHEDULE.format(sport=sport, league=league, season=season,
                                     stype=stype), "ESPN " + league + " schedule")
    if d is None:
        return None
    w = l = 0
    nxt = None
    for e in d.get("events", []):
        comp = (e.get("competitions") or [{}])[0]
        state = comp.get("status", {}).get("type", {}).get("name")
        if state == "STATUS_FINAL":
            for cm in comp.get("competitors", []):
                if cm.get("team", {}).get("abbreviation") == "DET":
                    if cm.get("winner"):
                        w += 1
                    else:
                        l += 1
        elif nxt is None and (days_until(e.get("date")) or -1) >= 0:
            nxt = {"name": e.get("name"), "when": e.get("date"),
                   "days": days_until(e.get("date"))}
    return {"completed": str(w) + "-" + str(l), "games": w + l, "next": nxt,
            "season": season, "seasontype": stype}


def espn(name: str, sport: str, league: str, season: int, stype: int):
    d = try_get(ESPN_TEAM.format(sport=sport, league=league), "ESPN " + league)
    if d is None:
        return None
    t = d["team"]
    out = {"team": t["displayName"], "candidates": []}
    c = out["candidates"]

    sched = espn_schedule(sport, league, season, stype)
    if sched:
        c.append(cand("Completed record, season " + str(season)
                      + " type " + str(stype), sched["completed"],
                      str(sched["games"]) + " games counted off the schedule "
                      "endpoint, not the record field",
                      "only when they play, so it is frozen out of season"))
        if sched["next"]:
            out["next_game"] = sched["next"]

    for item in t.get("record", {}).get("items", []):
        c.append(cand("Record (" + str(item.get("type")) + ")",
                      item.get("summary"), "ESPN " + league + " team endpoint",
                      "every game, and it reads 0-0 between seasons"))
        for s in item.get("stats", []):
            if s.get("name") in ("pointsFor", "pointsAgainst", "differential"):
                c.append(cand(s["name"], s.get("value"),
                              "ESPN " + league + " record stats", "every game"))

    if t.get("standingSummary"):
        c.append(cand("Standing", t["standingSummary"], "ESPN " + league,
                      "carries last season's finish while out of season, "
                      "so it holds until opening night"))

    ne = t.get("nextEvent") or []
    if ne and days_until(ne[0].get("date")) is not None \
            and days_until(ne[0].get("date")) < 0:
        c.append(cand("WARNING: ESPN nextEvent is stale",
                      ne[0].get("name"),
                      "the team endpoint still points at "
                      + str(ne[0].get("date")) + ", which is in the past; the "
                      "schedule endpoint above is the one to trust",
                      "n/a"))

    ng = out.get("next_game")
    if ng and ng.get("days") is not None:
        c.append(cand("Days until the next game", int(ng["days"]),
                      "next: " + str(ng.get("name")) + " at "
                      + str(ng.get("when")),
                      "predictably, by 1 a day"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Monday column candidate numbers.")
    ap.add_argument("--json", action="store_true", help="machine-readable")
    ap.add_argument("--team", choices=["tigers", "lions", "pistons", "wings"],
                    help="just one of them")
    args = ap.parse_args()

    wanted = args.team
    result = []
    if wanted in (None, "tigers"):
        r = tigers()
        if r:
            result.append(r)
    for name, sport, league, season, stype in ESPN_TEAMS:
        if wanted in (None, name):
            r = espn(name, sport, league, season, stype)
            if r:
                result.append(r)

    if args.json:
        print(json.dumps({"read_at": now().isoformat(timespec="seconds"),
                          "teams": result, "failures": failures}, indent=1))
    else:
        print("Four Numbers candidates, read "
              + now().isoformat(timespec="seconds") + "\n")
        for team in result:
            print("=== " + team["team"])
            ng = team.get("next_game")
            if ng:
                print("  next game: " + str(ng.get("name")) + "  "
                      + str(ng.get("when")) + "  (" + str(ng.get("days"))
                      + " days)")
            for c in team["candidates"]:
                print("  " + c["label"].ljust(38) + str(c["value"]).ljust(16)
                      + "[" + c["how"] + "]")
                print("  " + "".ljust(38) + "decays: " + c["decays"])
            print()
        if failures:
            print("FAILURES:")
            for f in failures:
                print("  " + f)

    if failures:
        print("\nEXIT 2: at least one fetch failed. The candidate list above is "
              "partial; re-run before writing the column.", file=sys.stderr)
        return 2
    print("EXIT 0: every fetch landed. The candidate list above is complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
