#!/usr/bin/env python3
"""Should Detroit run on Cleveland?

Written 2026-08-12 to answer the top item in REQUESTS.md, asked by two separate
commenters on r/motorcitykitties: Cleveland reportedly cannot throw anybody out,
Detroit reportedly refuses to run, and the series is being decided by one run at
a time.

Counting stolen bases proves nothing on its own, because a team that never
reaches first base cannot steal. So this pulls three things and keeps them
separate:

  1. Team running: SB, CS, success rate, and attempts per time reached first,
     which is the closest free proxy for "do they even try".
  2. Team defence: SB allowed and runners thrown out, taken from the **pitching**
     group. Not the catching group, which is a trap: it sums one row per catcher
     and each row carries the whole team's line, so Cleveland's four catchers
     turn 86 stolen bases allowed into 344 and 120 games into 18,008 batters
     faced. The multiplier is uniform, so the *rate* survives and the *counts*
     are fiction. The pitching group reconciles exactly with the hitting group
     across all 30 teams (2,458 steals, 740 caught, both ways), so it is the
     source of record here.
  3. The pitcher, because the runner goes on the pitcher far more than on the
     catcher, and tonight's Cleveland starter is the variable.

    python scripts/running_game.py            # tables plus the chart
    python scripts/running_game.py --json     # raw numbers

Writes scripts/last_running_chart.svg, embedded through the ```svg fence.
Cached for an hour in logs/running-cache.json so a re-run is free.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "logs" / "running-cache.json"
CACHE_MINUTES = 60
SEASON = 2026
API = "https://statsapi.mlb.com/api/v1"


def get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def team_group(group: str) -> dict:
    """Season totals for every team in one stat group, keyed by team name."""
    d = get(f"{API}/teams/stats?season={SEASON}&stats=season&group={group}&sportId=1")
    out = {}
    for split in d["stats"][0]["splits"]:
        out[split["team"]["name"]] = split["stat"]
    return out


def num(stat: dict, key: str) -> int:
    v = stat.get(key, 0)
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def reached_first(stat: dict) -> int:
    """Times a batter stood on first base: singles + walks + hit by pitch.

    An approximation, and the entry says so. It misses reaching on an error and
    on a fielder's choice, and it counts a walk that was immediately erased. It
    is the same approximation for all 30 teams, which is what the comparison
    needs.
    """
    hits = num(stat, "hits")
    singles = hits - num(stat, "doubles") - num(stat, "triples") - num(stat, "homeRuns")
    return singles + num(stat, "baseOnBalls") + num(stat, "hitByPitch")


def pitcher_running_game(pid: int) -> dict:
    """SB and CS allowed with this pitcher on the mound, plus handedness.

    A traded pitcher returns one split per team **plus** a combined row with no
    team on it, and they are not in a documented order. Taking the last split
    gave Foster Griffin's Washington line, 129.1 innings, and silently dropped
    the start he has made since the deadline. The combined row is the one with
    no `team` key; the per-team rows are kept so a piece can say where the
    innings were thrown.
    """
    person = get(f"{API}/people/{pid}")["people"][0]
    d = get(f"{API}/people/{pid}/stats?stats=season&group=pitching&season={SEASON}")
    total, by_team = {}, {}
    for s in d.get("stats", []):
        for split in s.get("splits", []):
            if "team" in split:
                by_team[split["team"]["name"]] = split["stat"]
            else:
                total = split["stat"]
    if not total:
        # A pitcher who has not changed teams gets one team row and no combined
        # row at all. Only safe to fall back when there is exactly one.
        if len(by_team) == 1:
            total = next(iter(by_team.values()))
        else:
            raise RuntimeError(f"no combined season row for {pid} "
                               f"and {len(by_team)} team rows")
    return {
        "name": person["fullName"],
        "hand": person.get("pitchHand", {}).get("code", "?"),
        "sb": num(total, "stolenBases"),
        "cs": num(total, "caughtStealing"),
        "ip": total.get("inningsPitched", "0.0"),
        "era": total.get("era"),
        "starts": num(total, "gamesStarted"),
        "by_team": {k: {"ip": v.get("inningsPitched"), "era": v.get("era"),
                        "starts": num(v, "gamesStarted"),
                        "sb": num(v, "stolenBases"), "cs": num(v, "caughtStealing")}
                    for k, v in by_team.items()},
    }


def collect() -> dict:
    if CACHE.exists() and (time.time() - CACHE.stat().st_mtime) / 60 < CACHE_MINUTES:
        return json.loads(CACHE.read_text(encoding="utf-8"))

    hitting = team_group("hitting")
    pitching = team_group("pitching")

    # Guard the trap described in the docstring: if these two ever stop
    # reconciling, something upstream changed and the numbers are not safe.
    lg_h = (sum(num(v, "stolenBases") for v in hitting.values()),
            sum(num(v, "caughtStealing") for v in hitting.values()))
    lg_p = (sum(num(v, "stolenBases") for v in pitching.values()),
            sum(num(v, "caughtStealing") for v in pitching.values()))
    if lg_h != lg_p:
        raise SystemExit(f"steals taken {lg_h} != steals allowed {lg_p}; "
                         f"do not publish off this run")

    teams = {}
    for name, h in hitting.items():
        p = pitching.get(name, {})
        teams[name] = {
            "sb": num(h, "stolenBases"),
            "cs": num(h, "caughtStealing"),
            "reached_first": reached_first(h),
            "sb_allowed": num(p, "stolenBases"),
            "cs_by": num(p, "caughtStealing"),
        }

    # Detroit's own runners, so "the roster is slow" can be tested rather than
    # repeated. One request; the roster endpoint carries season hitting stats.
    det = get(f"{API}/teams/116/roster?rosterType=active&hydrate=person(stats("
              f"group=[hitting],type=[season],season={SEASON}))")
    runners = []
    for entry in det["roster"]:
        p = entry["person"]
        stat = {}
        for s in p.get("stats", []):
            for split in s.get("splits", []):
                stat = split["stat"]
        if not stat:
            continue
        sb, cs = num(stat, "stolenBases"), num(stat, "caughtStealing")
        if sb + cs == 0:
            continue
        runners.append({"name": p["fullName"], "sb": sb, "cs": cs,
                        "reached_first": reached_first(stat)})
    runners.sort(key=lambda r: -r["sb"])

    starters = {}
    # IDs read off the schedule endpoint's probablePitcher for 824241, never
    # guessed: a wrong id here would silently describe a different pitcher.
    for label, pid in (("griffin", 656492), ("valdez", 664285)):
        try:
            starters[label] = pitcher_running_game(pid)
        except Exception as exc:  # noqa: BLE001 - reported, never silently dropped
            starters[label] = {"error": str(exc)}

    out = {"teams": teams, "detroit_runners": runners, "starters": starters}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(out, indent=1), encoding="utf-8")
    return out


def cs_rate(v: dict) -> float:
    att = v["sb_allowed"] + v["cs_by"]
    return v["cs_by"] / att if att else 0.0


def attempt_rate(v: dict) -> float:
    return (v["sb"] + v["cs"]) / v["reached_first"] if v["reached_first"] else 0.0


def chart(teams: dict) -> str:
    """Attempt rate against the rate opponents get thrown out.

    A scatter, because the request is a two-variable question: teams that run
    a lot, and defences that cannot stop it, are different axes and a bar chart
    would have to pick one.
    """
    rows = [(n, attempt_rate(v), cs_rate(v)) for n, v in teams.items()]
    xs = [r[1] for r in rows]
    ys = [r[2] for r in rows]
    xlo, xhi = min(xs) * 0.9, max(xs) * 1.05
    ylo, yhi = min(ys) * 0.9, max(ys) * 1.05
    W, H = 640, 400
    l, r, t, b = 52, 14, 56, 40

    def X(v):
        return l + (v - xlo) / (xhi - xlo) * (W - l - r)

    def Y(v):
        return t + (yhi - v) / (yhi - ylo) * (H - t - b)

    avg_x = sum(xs) / len(xs)
    avg_y = sum(ys) / len(ys)
    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="run-t" '
           f'style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,'
           f'-apple-system,\'Segoe UI\',Roboto,sans-serif">',
           '<title id="run-t">Every team\'s stolen base attempt rate against the rate '
           'at which their catchers throw runners out</title>',
           '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
           'Who runs, and who can stop it</text>',
           '<text x="0" y="34" fill="var(--muted)" font-size="11">'
           'Each dot is a team. Right means they attempt more steals. Up means their '
           'catchers throw more runners out.</text>']
    out.append(f'<line x1="{X(avg_x):.1f}" y1="{t}" x2="{X(avg_x):.1f}" y2="{H - b}" '
               f'stroke="var(--rule)" stroke-width="1"/>')
    out.append(f'<line x1="{l}" y1="{Y(avg_y):.1f}" x2="{W - r}" y2="{Y(avg_y):.1f}" '
               f'stroke="var(--rule)" stroke-width="1"/>')
    for name, ar, cr in rows:
        tag = {"Detroit Tigers": "DET", "Cleveland Guardians": "CLE"}.get(name)
        colour = {"DET": "var(--chart-pos)", "CLE": "var(--chart-neg)"}.get(tag, "var(--rule)")
        rad = 6 if tag else 3.5
        out.append(f'<circle cx="{X(ar):.1f}" cy="{Y(cr):.1f}" r="{rad}" fill="{colour}">'
                   f'<title>{name}: attempts on {ar * 100:.1f}% of times on first, '
                   f'throws out {cr * 100:.1f}%</title></circle>')
        if tag:
            out.append(f'<text x="{X(ar) + 9:.1f}" y="{Y(cr) + 4:.1f}" fill="var(--fg)" '
                       f'font-size="11" font-weight="600">{tag}</text>')
    out.append(f'<text x="{W / 2:.0f}" y="{H - 10}" text-anchor="middle" fill="var(--muted)" '
               f'font-size="11">Steal attempts per time reached first</text>')
    out.append(f'<text x="14" y="{(t + H - b) / 2:.0f}" fill="var(--muted)" font-size="11" '
               f'transform="rotate(-90 14 {(t + H - b) / 2:.0f})" text-anchor="middle">'
               f'Runners thrown out</text>')
    for v in (xlo, avg_x, xhi):
        out.append(f'<text x="{X(v):.1f}" y="{H - b + 16}" text-anchor="middle" '
                   f'fill="var(--muted)" font-size="10" font-variant-numeric="tabular-nums">'
                   f'{v * 100:.0f}%</text>')
    for v in (ylo, avg_y, yhi):
        out.append(f'<text x="{l - 6}" y="{Y(v) + 4:.1f}" text-anchor="end" '
                   f'fill="var(--muted)" font-size="10" font-variant-numeric="tabular-nums">'
                   f'{v * 100:.0f}%</text>')
    out.append("</svg>")
    return "\n".join(out)


def main(argv):
    data = collect()
    if "--json" in argv:
        print(json.dumps(data, indent=1))
        return 0
    teams = data["teams"]

    by_cs = sorted(teams.items(), key=lambda kv: cs_rate(kv[1]))
    print("Worst at throwing runners out:")
    for i, (n, v) in enumerate(by_cs[:6], 1):
        print(f"  {i:2}. {n:24} {v['cs_by']:3} of {v['sb_allowed'] + v['cs_by']:3} "
              f"= {cs_rate(v) * 100:.1f}%")
    print("Best:")
    for i, (n, v) in enumerate(by_cs[-3:], len(by_cs) - 2):
        print(f"  {i:2}. {n:24} {v['cs_by']:3} of {v['sb_allowed'] + v['cs_by']:3} "
              f"= {cs_rate(v) * 100:.1f}%")

    lg_sb = sum(v["sb_allowed"] for v in teams.values())
    lg_cs = sum(v["cs_by"] for v in teams.values())
    print(f"\nLeague caught stealing rate: {lg_cs} of {lg_sb + lg_cs} = "
          f"{lg_cs / (lg_sb + lg_cs) * 100:.1f}%")

    by_att = sorted(teams.items(), key=lambda kv: attempt_rate(kv[1]))
    print("\nLeast willing to run (attempts per time reached first):")
    for i, (n, v) in enumerate(by_att[:5], 1):
        print(f"  {i:2}. {n:24} {v['sb'] + v['cs']:4} attempts / {v['reached_first']:4} "
              f"= {attempt_rate(v) * 100:.1f}%   ({v['sb']}-{v['cs']})")
    print("Most willing:")
    for i, (n, v) in enumerate(by_att[-3:], len(by_att) - 2):
        print(f"  {i:2}. {n:24} {v['sb'] + v['cs']:4} attempts / {v['reached_first']:4} "
              f"= {attempt_rate(v) * 100:.1f}%   ({v['sb']}-{v['cs']})")

    for name in ("Detroit Tigers", "Cleveland Guardians"):
        v = teams[name]
        att = v["sb"] + v["cs"]
        succ = v["sb"] / att * 100 if att else 0
        print(f"\n{name}: {v['sb']}-{v['cs']}, {succ:.1f}% success, "
              f"attempt rate {attempt_rate(v) * 100:.2f}% "
              f"(rank {[n for n, _ in by_att].index(name) + 1} of 30), "
              f"reached first {v['reached_first']}")
        print(f"  catchers: {v['cs_by']} of {v['sb_allowed'] + v['cs_by']} = "
              f"{cs_rate(v) * 100:.1f}% "
              f"(rank {[n for n, _ in by_cs].index(name) + 1} of 30, 1 = worst)")

    print("\nDetroit runners:")
    for r in data["detroit_runners"][:10]:
        att = r["sb"] + r["cs"]
        print(f"  {r['name']:22} {r['sb']:3}-{r['cs']:2}  "
              f"{r['sb'] / att * 100:5.1f}%  on first {r['reached_first']:3}  "
              f"attempt rate {att / r['reached_first'] * 100 if r['reached_first'] else 0:.1f}%")

    print("\nTonight's starters:")
    for label, s in data["starters"].items():
        if "error" in s:
            print(f"  {label}: FAILED {s['error']}")
            continue
        att = s["sb"] + s["cs"]
        print(f"  {s['name']:20} {s['hand']}HP  {s['ip']} IP  {s['starts']} GS  "
              f"{s['era']} ERA  {s['sb']} SB / {s['cs']} CS allowed"
              + (f"  ({s['cs'] / att * 100:.0f}% caught)" if att else "  (nobody caught)"))
        for team, v in s["by_team"].items():
            print(f"      {team:24} {v['ip']:>6} IP  {v['starts']:2} GS  {v['era']:>5} ERA  "
                  f"{v['sb']} SB / {v['cs']} CS")

    svg = ROOT / "scripts" / "last_running_chart.svg"
    svg.write_text(chart(teams), encoding="utf-8")
    print(f"\nwrote {svg.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
