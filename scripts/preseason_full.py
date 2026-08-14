#!/usr/bin/env python3
"""The preseason backtest, rebuilt after two reader objections.

The published version (`preseason_signal.py`, entry 2026-08-08) ran 2015 to
2025 and said the window came from ESPN's coverage. Two things turned out to be
wrong, and this script exists to fix both in one derivation so the prose and the
chart cannot disagree.

1. **The window was not the data floor.** ESPN serves preseason schedules back
   to 2000. 2015 was a choice nobody made on purpose, and it excluded the 2008
   Lions, which is the single most famous confirming case of the piece's own
   claim and belongs to the subreddit the post went to.

2. **Three franchises were being counted as their opponents.** `fetch()` found
   "my" side of a game by comparing the requested abbreviation to the one in the
   box score. ESPN's schedule endpoint answers `/teams/lar/` for every season but
   returns the *historical* abbreviation inside the game, so a 2015 Rams game
   carries STL, no side matched "lar", and the code fell back to `sides[0]` --
   which is whichever team ESPN listed first, frequently the opponent. Same for
   LAC (SD through 2016) and LV (OAK through 2019).

   The fix is to match on ESPN's numeric team id, which is stable across all
   three relocations (Rams 14, Chargers 24, Raiders 13).

    python scripts/preseason_full.py            # full derivation to stdout
    python scripts/preseason_full.py --chart    # inline SVG to stdout
    python scripts/preseason_full.py --diff     # what the bug did to the
                                                # published 2015-2025 numbers

2020 is skipped: no preseason was played. Ties count as half a win on both
sides. The cache file is the receipt; delete it to refetch.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

FIRST_SEASON = 2000          # verified floor: 1999 and earlier return 0 events
LAST_SEASON = 2025
SEASONS = [s for s in range(FIRST_SEASON, LAST_SEASON + 1) if s != 2020]
PUBLISHED_SEASONS = [s for s in range(2015, 2026) if s != 2020]

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "preseason_cache_2000.json")
PHANTOM_LOG = os.path.join(HERE, "preseason_phantom_games.json")
OLD_CACHE = os.path.join(HERE, "preseason_cache.json")   # what was published

# Fixtures ESPN serves as 0-0 rather than null, collected during a live sweep
# so the count is evidence rather than an assertion. See fetch().
PHANTOMS: list[tuple] = []

API = ("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/"
       "{team}/schedule?season={season}&seasontype={st}")

TEAMS = [
    "ari", "atl", "bal", "buf", "car", "chi", "cin", "cle", "dal", "den",
    "det", "gb", "hou", "ind", "jax", "kc", "lac", "lar", "lv", "mia",
    "min", "ne", "no", "nyg", "nyj", "phi", "pit", "sea", "sf", "tb",
    "ten", "wsh",
]

PAD_L, PAD_R, TOP, BOTTOM = 52, 22, 58, 46


def _get(url: str) -> dict:
    """ESPN throws intermittent 502s under a long sweep; back off and retry."""
    for attempt in range(8):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt == 7:
                raise
            time.sleep(2.0 * (attempt + 1))
    raise RuntimeError("unreachable")


def fetch(team: str, season: int, st: int) -> tuple[float, float]:
    """Return (wins, games) for one team-season-phase. A tie is half a win.

    Identifies our side by ESPN's numeric team id rather than by abbreviation.
    The abbreviation in a box score is the one the franchise used *that year*,
    so STL/SD/OAK games never matched a request for lar/lac/lv. There is no
    positional fallback on purpose: guessing `sides[0]` is what produced wrong
    records silently, and a loud failure is worth more than a plausible number.
    """
    data = _get(API.format(team=team, season=season, st=st))
    my_id = str(data.get("team", {}).get("id", ""))
    if not my_id:
        raise RuntimeError(f"no team id for {team} {season}")

    wins = games = 0.0
    skipped_zero: list[str] = []
    for event in data.get("events", []):
        comp = event["competitions"][0]
        sides = comp.get("competitors", [])
        if len(sides) != 2:
            continue
        scores = [s.get("score", {}).get("value") for s in sides]
        if any(v is None for v in scores):
            continue                                   # unplayed or cancelled
        if scores[0] == 0 and scores[1] == 0:
            # Older seasons carry never-played fixtures as 0-0 rather than
            # null, and a 0-0 was scoring as a tie, i.e. half a win each way.
            # Detroit 2001 came back 2.5-13.5 against a real 2-14 because of a
            # phantom DET-STL game on 2001-10-09. No NFL game has finished 0-0
            # since 1943, so treating a 0-0 as unplayed costs nothing.
            skipped_zero.append(event.get("date", "")[:10])
            continue
        mine = next((s for s in sides
                     if str(s["team"].get("id")) == my_id), None)
        if mine is None:
            raise RuntimeError(
                f"{team} {season} st{st}: id {my_id} absent from a game it is "
                f"listed in ({[s['team']['abbreviation'] for s in sides]})")
        games += 1
        if scores[0] == scores[1]:
            wins += 0.5
        elif mine.get("winner"):
            wins += 1
    if skipped_zero:
        PHANTOMS.append((team, season, st, skipped_zero))
    return wins, games


def collect() -> list[dict]:
    """One row per team-season, cached to disk so a rerun costs nothing."""
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)

    partial = CACHE + ".partial"
    rows: list[dict] = []
    if os.path.exists(partial):
        with open(partial, encoding="utf-8") as fh:
            rows = json.load(fh)
    done = {(r["team"], r["season"]) for r in rows}

    for season in SEASONS:
        for team in TEAMS:
            if (team, season) in done:
                continue
            pre_w, pre_g = fetch(team, season, 1)
            reg_w, reg_g = fetch(team, season, 2)
            if pre_g < 2 or reg_g < 10:      # franchise did not exist, or gaps
                continue
            rows.append({
                "team": team, "season": season,
                "pre_w": pre_w, "pre_g": pre_g,
                "reg_w": reg_w, "reg_g": reg_g,
                "pre_pct": pre_w / pre_g, "reg_pct": reg_w / reg_g,
            })
        with open(partial, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=1)
        print(f"  {season}: {len(rows)} rows", file=sys.stderr)

    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
    with open(PHANTOM_LOG, "w", encoding="utf-8") as fh:
        json.dump([{"team": t, "season": s, "seasontype": st, "dates": d}
                   for t, s, st, d in PHANTOMS], fh, indent=1)
    os.remove(partial)
    return rows


def correlation(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    return num / (dx * dy)


BUCKETS = [
    ("Won every preseason game", lambda r: r["pre_pct"] == 1.0),
    ("Winning preseason", lambda r: 0.5 < r["pre_pct"] < 1.0),
    ("Even preseason", lambda r: r["pre_pct"] == 0.5),
    ("Losing preseason", lambda r: 0.0 < r["pre_pct"] < 0.5),
    ("Lost every preseason game", lambda r: r["pre_pct"] == 0.0),
]


def buckets(rows: list[dict]) -> list[dict]:
    out = []
    for label, test in BUCKETS:
        group = [r for r in rows if test(r)]
        if not group:
            continue
        reg = sum(r["reg_pct"] for r in group) / len(group)
        out.append({"label": label, "n": len(group), "reg_pct": reg,
                    "gap": reg - 0.5})
    return out


def bar_path(x0: float, x1: float, y: float, h: float, r: float = 4.0) -> str:
    if abs(x1 - x0) < r:
        return f"M{x0},{y}H{x1}V{y+h}H{x0}Z"
    if x1 > x0:
        return (f"M{x0},{y}H{x1-r}A{r},{r} 0 0 1 {x1},{y+r}"
                f"V{y+h-r}A{r},{r} 0 0 1 {x1-r},{y+h}H{x0}Z")
    return (f"M{x0},{y}H{x1+r}A{r},{r} 0 0 0 {x1},{y+r}"
            f"V{y+h-r}A{r},{r} 0 0 0 {x1+r},{y+h}H{x0}Z")


def build_chart(rows: list[dict], width: int = 640) -> str:
    """Same grouped-bar form as the published chart, on the full sample.

    A scatter is the wrong shape here: preseason win rate takes about seven
    distinct values, so the dots collapse into columns and hide the thing being
    shown. Bars against a .500 baseline say it plainly.
    """
    bars = buckets(rows)
    n_total = len(rows)
    bar_h, gap = 26, 14
    label_w = 196
    plot_w = width - label_w - 56
    span = 0.09                                   # +/- around .500, in win pct
    def to_x(v: float) -> float:
        return label_w + (v + span) / (2 * span) * plot_w
    zero = to_x(0.0)

    height = TOP + len(bars) * (bar_h + gap) - gap + BOTTOM
    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" '
        f'role="img" aria-labelledby="pre26-title" '
        f'style="max-width:{width}px;height:auto;font-family:ui-sans-serif,'
        f"system-ui,-apple-system,'Segoe UI',Roboto,sans-serif\">",
        f'<title id="pre26-title">Regular season winning percentage by '
        f'preseason record, all NFL teams, {FIRST_SEASON} to {LAST_SEASON}'
        f'</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">How each preseason group actually did</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">Regular season '
        f'winning percentage against .500. {n_total} team-seasons, '
        f'{FIRST_SEASON} to {LAST_SEASON}, 2020 excluded.</text>',
        '<text x="0" y="49" fill="var(--muted)" font-size="11">Every season '
        'ESPN carries preseason results for.</text>',
    ]
    out.append(f'<line x1="{zero:.1f}" y1="{TOP-6}" x2="{zero:.1f}" '
               f'y2="{height-BOTTOM+6:.1f}" stroke="var(--rule)" '
               f'stroke-width="2"/>')

    for i, b in enumerate(bars):
        y = TOP + i * (bar_h + gap)
        x_end = to_x(b["gap"])
        pos = b["gap"] >= 0
        x_start = zero + (2 if pos else -2)
        color = "var(--chart-pos)" if pos else "var(--chart-neg)"
        out.append(
            f'<text x="{label_w-12}" y="{y+bar_h/2+4:.1f}" text-anchor="end" '
            f'fill="var(--fg)" font-size="12.5">{b["label"]}</text>'
        )
        out.append(
            f'<path d="{bar_path(x_start, x_end, y, bar_h)}" fill="{color}">'
            f'<title>{b["label"]}: {b["n"]} team-seasons, regular season '
            f'{b["reg_pct"]:.3f}</title></path>'
        )
        anchor, dx = ("start", 8) if pos else ("end", -8)
        out.append(
            f'<text x="{x_end+dx:.1f}" y="{y+bar_h/2+4:.1f}" '
            f'text-anchor="{anchor}" fill="var(--muted)" font-size="12" '
            f'font-variant-numeric="tabular-nums">'
            f'{b["reg_pct"]:.3f} (n={b["n"]})</text>'
        )

    out.append(f'<text x="0" y="{height-10}" fill="var(--muted)" '
               f'font-size="11">Bars right of the line beat .500, left of it '
               f'missed. Nothing here is far from the line.</text>')
    out.append("</svg>")
    return "\n".join(out)


def report(rows: list[dict], label: str) -> None:
    xs = [r["pre_pct"] for r in rows]
    ys = [r["reg_pct"] for r in rows]
    r_val = correlation(xs, ys)
    print(f"--- {label}: {len(rows)} team-seasons")
    print(f"    correlation {r_val:+.3f}   variance explained "
          f"{r_val ** 2 * 100:.1f}%")
    for b in buckets(rows):
        print(f"    {b['label']:<28} n={b['n']:<4} "
              f"regular season {b['reg_pct']:.3f} ({b['gap']:+.3f})")
    print()


def diff_against_published(rows: list[dict]) -> None:
    """Quantify what the abbreviation bug did to the numbers already in print.

    The old cache is the receipt for the published entry, so this is a direct
    comparison rather than a reconstruction from memory.
    """
    if not os.path.exists(OLD_CACHE):
        print("old cache absent; nothing to diff", file=sys.stderr)
        return
    with open(OLD_CACHE, encoding="utf-8") as fh:
        old = {(r["team"], r["season"]): r for r in json.load(fh)}
    new = {(r["team"], r["season"]): r for r in rows
           if r["season"] in PUBLISHED_SEASONS}

    changed = []
    for key, n in sorted(new.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        o = old.get(key)
        if o is None:
            continue
        if (o["pre_w"], o["reg_w"]) != (n["pre_w"], n["reg_w"]):
            changed.append((key, o, n))

    print(f"--- the relocation bug, on the published 2015-2025 window")
    print(f"    team-seasons in both: {len(new & old.keys())}")
    print(f"    rows whose record changed: {len(changed)}")
    for (team, season), o, n in changed:
        print(f"    {team.upper()} {season}: preseason "
              f"{o['pre_w']:g}-{o['pre_g']-o['pre_w']:g} -> "
              f"{n['pre_w']:g}-{n['pre_g']-n['pre_w']:g}   regular "
              f"{o['reg_w']:g}-{o['reg_g']-o['reg_w']:g} -> "
              f"{n['reg_w']:g}-{n['reg_g']-n['reg_w']:g}")
    print()
    print("    published buckets vs corrected, same window:")
    old_rows = [old[k] for k in new if k in old]
    ob = {b["label"]: b for b in buckets(old_rows)}
    nb = {b["label"]: b for b in buckets(list(new.values()))}
    for label, _ in BUCKETS:
        o, n = ob.get(label), nb.get(label)
        if not o or not n:
            continue
        print(f"    {label:<28} n {o['n']:>3} -> {n['n']:<3} "
              f"reg {o['reg_pct']:.3f} -> {n['reg_pct']:.3f}")
    print()


def main() -> None:
    rows = collect()
    if "--chart" in sys.argv:
        print(build_chart(rows))
        return

    print(f"seasons {FIRST_SEASON}-{LAST_SEASON}, 2020 excluded "
          f"({len(SEASONS)} seasons)\n")
    report(rows, f"full sample {FIRST_SEASON}-{LAST_SEASON}")
    report([r for r in rows if r["season"] in PUBLISHED_SEASONS],
           "the published window 2015-2025, corrected")
    report([r for r in rows if r["season"] < 2015],
           "the seasons the published window missed, 2000-2014")

    if "--diff" in sys.argv:
        diff_against_published(rows)

    perfect = [r for r in rows if r["pre_pct"] == 1.0]
    winless = [r for r in rows if r["pre_pct"] == 0.0]
    print(f"--- the tails, full sample")
    print(f"    undefeated preseasons: {len(perfect)}")
    print(f"    winless preseasons:    {len(winless)}")
    worst = sorted(perfect, key=lambda r: r["reg_pct"])[:5]
    best = sorted(perfect, key=lambda r: -r["reg_pct"])[:5]
    print("    worst seasons after an undefeated preseason:")
    for r in worst:
        print(f"      {r['team'].upper()} {r['season']}: "
              f"{r['reg_w']:g}-{r['reg_g']-r['reg_w']:g} ({r['reg_pct']:.3f})")
    print("    best seasons after an undefeated preseason:")
    for r in best:
        print(f"      {r['team'].upper()} {r['season']}: "
              f"{r['reg_w']:g}-{r['reg_g']-r['reg_w']:g} ({r['reg_pct']:.3f})")
    print()

    lions = sorted([r for r in rows if r["team"] == "det"],
                   key=lambda r: r["season"])
    print(f"--- Detroit, {len(lions)} seasons")
    for r in lions:
        print(f"    DET {r['season']}: preseason {r['pre_w']:g}-"
              f"{r['pre_g']-r['pre_w']:g}  regular {r['reg_w']:g}-"
              f"{r['reg_g']-r['reg_w']:g}  ({r['reg_pct']:.3f})")
    lx = [r["pre_pct"] for r in lions]
    ly = [r["reg_pct"] for r in lions]
    lr = correlation(lx, ly)
    print(f"    Detroit correlation {lr:+.3f}, variance explained "
          f"{lr ** 2 * 100:.1f}%")


if __name__ == "__main__":
    main()
