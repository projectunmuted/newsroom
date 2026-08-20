"""Opening-stretch strength of schedule for the 2026-27 NBA season.

Answers one question properly: a fan thread says Detroit's first 4 games are
Boston, Miami, Philadelphia and the Knicks. Is that actually the hardest
opening in the league, or does somebody have to be first?

Method: prior-season (2025-26) winning percentage as the opponent-strength
proxy, because it is the only real number that exists before a game is played.
Every team's first N games are scored the same way, so Detroit gets ranked
against 29 others rather than described in isolation.

Free data, no key: ESPN's public JSON.
"""
import json, sys, urllib.request, statistics

UA = {"User-Agent": "Mozilla/5.0"}
STANDINGS = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings?season=2026"
SCHED = ("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/"
         "{abbr}/schedule?season={season}&seasontype=2")


def fetch(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))


def prior_records():
    """{abbr: (w, l, pct)} from the completed 2025-26 regular season."""
    d = fetch(STANDINGS)
    out = {}
    for conf in d.get("children", []):
        for e in conf["standings"]["entries"]:
            abbr = e["team"]["abbreviation"]
            st = {s["name"]: s for s in e["stats"]}
            w = int(st["wins"]["value"])
            l = int(st["losses"]["value"])
            out[abbr] = (w, l, w / (w + l))
    return out


def schedule(abbr, season=2027):
    """Ordered list of (date, opponent_abbr, is_home), deduped by event id."""
    d = fetch(SCHED.format(abbr=abbr.lower(), season=season))
    rows, seen = [], set()
    for ev in d.get("events", []):
        cid = ev["id"]
        if cid in seen:
            continue
        seen.add(cid)
        comp = ev["competitions"][0]["competitors"]
        me = next(c for c in comp if c["team"]["abbreviation"].upper() == abbr.upper())
        them = next(c for c in comp if c is not me)
        rows.append((ev["date"], them["team"]["abbreviation"], me["homeAway"] == "home",
                     me.get("winner"), bool(ev["competitions"][0].get("neutralSite"))))
    rows.sort(key=lambda r: r[0])
    return rows


def home_win_pct():
    """League-wide home winning percentage across the completed 2025-26 season."""
    home_w = home_g = 0
    for t in TEAMS:
        for _, _, is_home, won, neutral in schedule(t, season=2026):
            if not is_home or won is None or neutral:
                continue
            home_g += 1
            home_w += 1 if won else 0
    return home_w, home_g, home_w / home_g


def log5(p_a, p_b, home_odds=1.0):
    """Probability A beats B, with A's odds multiplied by home_odds."""
    p_a = min(max(p_a, 1e-6), 1 - 1e-6)
    p_b = min(max(p_b, 1e-6), 1 - 1e-6)
    base = (p_a - p_a * p_b) / (p_a + p_b - 2 * p_a * p_b)
    o = base / (1 - base) * home_odds
    return o / (1 + o)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    prior = prior_records()
    global TEAMS
    TEAMS = sorted(prior)
    print(f"2025-26 final records loaded for {len(TEAMS)} teams")

    hw, hg, hpct = home_win_pct()
    home_odds = hpct / (1 - hpct)
    print(f"2025-26 home teams went {hw}-{hg - hw} in {hg} non-neutral games "
          f"({hpct:.4f}); home odds multiplier {home_odds:.3f}")

    table = []
    for t in TEAMS:
        sched = schedule(t)
        first = sched[:n]
        if len(first) < n or any(o not in prior for _, o, _, _, _ in first):
            print(f"  !! {t}: incomplete first {n}", file=sys.stderr)
            continue
        if any(neu for _, _, _, _, neu in first):
            print(f"  !! {t}: neutral-site game in first {n}", file=sys.stderr)
            print(f"  !! {t}: incomplete first {n}", file=sys.stderr)
            continue
        pcts = [prior[o][2] for _, o, _, _, _ in first]
        road = sum(1 for _, _, h, _, _ in first if not h)
        exp = sum(log5(prior[t][2], prior[o][2], home_odds if h else 1 / home_odds)
                  for _, o, h, _, _ in first)
        table.append({
            "team": t, "opp_pct": sum(pcts) / n, "road": road, "exp_wins": exp,
            "opps": [(o, prior[o][0], prior[o][1], h) for _, o, h, _, _ in first],
            "dates": [d[:10] for d, _, _, _, _ in first],
        })

    def report(key, label, reverse=True):
        table.sort(key=lambda r: -r[key] if reverse else r[key])
        print(f"\n=== {label}, opening {n} games, all {len(table)} teams ===")
        print(f"{'#':>3}  {'Tm':<4} {'OppPct':>7} {'Road':>5} {'xW':>6}  Opponents")
        for i, r in enumerate(table, 1):
            opps = ", ".join(f"{o}{'' if h else '@'}({w}-{l})" for o, w, l, h in r["opps"])
            star = "  <<<" if r["team"] == "DET" else ""
            print(f"{i:>3}  {r['team']:<4} {r['opp_pct']:>7.4f} {r['road']:>5} "
                  f"{r['exp_wins']:>6.3f}  {opps}{star}")
        det = next(r for r in table if r["team"] == "DET")
        vals = [r[key] for r in table]
        z = (det[key] - statistics.mean(vals)) / statistics.pstdev(vals)
        print(f"  league mean {statistics.mean(vals):.4f} sd {statistics.pstdev(vals):.4f}; "
              f"DET rank {table.index(det) + 1} of {len(table)}, {det[key]:.4f}, z {z:+.2f}")

    report("opp_pct", "By mean opponent 2025-26 win pct")
    report("exp_wins", "By expected wins (log5, home-court adjusted), hardest first", reverse=False)

    det = next(r for r in table if r["team"] == "DET")
    print(f"\nDET: {det['road']} road in first {n}, dates {det['dates']}, "
          f"prior record {prior['DET'][0]}-{prior['DET'][1]}")
    roads = sorted((r["road"] for r in table), reverse=True)
    print(f"road counts across the league: {roads}")


TEAMS = []


if __name__ == "__main__":
    main()
