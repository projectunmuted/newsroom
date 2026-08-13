#!/usr/bin/env python3
"""Detroit's preseason win percentage against its regular season win percentage,
one team, 20 seasons.

Asked in the r/detroitlions thread on 2026-08-13, and it is the right question
to ask of a league-wide backtest: fine, it means nothing in aggregate, but what
did it do to us? A league study answers a question nobody in a fan sub asked.

It also pays the debt from that same thread. The published piece started in 2015
because that is where the league-wide cache starts, which left out 2008: 4-0 in
August, 0-16 in the regular season, the most famous confirming case in football
and the one belonging to this subreddit. 20 seasons reaches back to 2006 and
picks it up.

    python scripts/lions_preseason_20.py           # numbers to stdout
    python scripts/lions_preseason_20.py --png     # attachable PNG

Same ESPN endpoint and the same rules as the league backtest, so the Detroit
rows here must match the Detroit rows there for the overlapping seasons: 2020 is
excluded, ties count as half a win. Its own cache file is the receipt.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "lions_preseason_cache.json")
OUT = os.path.join(HERE, "last_lions_preseason.png")
API = ("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/"
       "det/schedule?season={season}&seasontype={st}")

# 20 seasons ending with the last completed one. 2020 had no preseason, so it is
# dropped rather than counted as a 0-0 August.
SEASONS = [s for s in range(2006, 2026) if s != 2020]

S1 = "#2a78d6"   # preseason
S2 = "#eb6834"   # regular season
INK, MUTE, RULE, CARD = "#1a1a19", "#6b6a66", "#e3e0d9", "#ffffff"


def fetch(season: int, st: int) -> tuple[float, float]:
    """Wins and games for one season and season type. Ties are half a win."""
    url = API.format(season=season, st=st)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.loads(r.read())
            break
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == 3:
                raise SystemExit(f"{season} type {st}: {e}")
            time.sleep(2 * (attempt + 1))

    wins = games = 0.0
    for ev in data.get("events", []):
        comp = (ev.get("competitions") or [{}])[0]
        if comp.get("status", {}).get("type", {}).get("state") != "post":
            continue
        us = next((c for c in comp.get("competitors", [])
                   if c.get("team", {}).get("abbreviation", "").lower() == "det"),
                  None)
        if not us:
            continue
        games += 1
        if us.get("winner"):
            wins += 1
        elif all(not c.get("winner") for c in comp.get("competitors", [])):
            wins += 0.5   # tie
    return wins, games


def build() -> list[dict]:
    if os.path.exists(CACHE):
        return json.load(open(CACHE, encoding="utf-8"))
    rows = []
    for s in SEASONS:
        pw, pg = fetch(s, 1)      # 1 = preseason
        rw, rg = fetch(s, 2)      # 2 = regular season
        if pg == 0 or rg == 0:
            print(f"  {s}: skipped, pre {pg:g} games, reg {rg:g} games")
            continue
        rows.append({"season": s, "pre_w": pw, "pre_g": pg, "reg_w": rw,
                     "reg_g": rg, "pre_pct": pw / pg, "reg_pct": rw / rg})
        print(f"  {s}: pre {pw:g}-{pg - pw:g}, reg {rw:g}-{rg - rw:g}")
        time.sleep(0.4)
    json.dump(rows, open(CACHE, "w", encoding="utf-8"), indent=1)
    return rows


def report(rows: list[dict]) -> None:
    print(f"\nDetroit, {len(rows)} seasons, {rows[0]['season']} to "
          f"{rows[-1]['season']}\n")
    print("season   preseason   regular      pre%   reg%")
    for r in rows:
        print(f"  {r['season']}   {r['pre_w']:g}-{r['pre_g'] - r['pre_w']:g}"
              f"        {r['reg_w']:g}-{r['reg_g'] - r['reg_w']:g}"
              f"{'':<4}  {r['pre_pct']:.3f}  {r['reg_pct']:.3f}")

    n = len(rows)
    mp = sum(r["pre_pct"] for r in rows) / n
    mr = sum(r["reg_pct"] for r in rows) / n
    # Pearson r by hand; scipy is not a dependency of this repo and this is 8
    # lines of arithmetic.
    sp = sum((r["pre_pct"] - mp) * (r["reg_pct"] - mr) for r in rows)
    vp = sum((r["pre_pct"] - mp) ** 2 for r in rows) ** 0.5
    vr = sum((r["reg_pct"] - mr) ** 2 for r in rows) ** 0.5
    corr = sp / (vp * vr) if vp and vr else 0.0

    print(f"\nmean preseason {mp:.3f}, mean regular season {mr:.3f}")
    print(f"correlation {corr:+.3f}, r squared {corr ** 2 * 100:.1f}%")

    best_pre = max(rows, key=lambda r: (r["pre_pct"], -r["season"]))
    worst_pre = min(rows, key=lambda r: (r["pre_pct"], r["season"]))
    print(f"\nbest August:  {best_pre['season']} at {best_pre['pre_w']:g}-"
          f"{best_pre['pre_g'] - best_pre['pre_w']:g}, then "
          f"{best_pre['reg_w']:g}-{best_pre['reg_g'] - best_pre['reg_w']:g}")
    print(f"worst August: {worst_pre['season']} at {worst_pre['pre_w']:g}-"
          f"{worst_pre['pre_g'] - worst_pre['pre_w']:g}, then "
          f"{worst_pre['reg_w']:g}-{worst_pre['reg_g'] - worst_pre['reg_w']:g}")

    # The seasons where August and the season pointed opposite ways, which is
    # the whole argument in a handful of rows.
    print("\nAugust said one thing and the season said the other:")
    for r in rows:
        if (r["pre_pct"] >= 0.75 and r["reg_pct"] <= 0.4) or \
           (r["pre_pct"] <= 0.25 and r["reg_pct"] >= 0.6):
            print(f"   {r['season']}: {r['pre_w']:g}-"
                  f"{r['pre_g'] - r['pre_w']:g} August, "
                  f"{r['reg_w']:g}-{r['reg_g'] - r['reg_w']:g} season")


def png(rows: list[dict]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    seasons = [r["season"] for r in rows]
    xs = list(range(len(rows)))
    pre = [r["pre_pct"] * 100 for r in rows]
    reg = [r["reg_pct"] * 100 for r in rows]

    fig, ax = plt.subplots(figsize=(11.5, 5.8), dpi=130)
    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    # Paired bars per season, because the question is literally "these two
    # numbers, side by side, for each year". The eye should be able to check
    # every season for agreement and find it absent.
    ax.bar([x - 0.2 for x in xs], pre, width=0.38, color=S1, zorder=3,
           label="Preseason win %")
    ax.bar([x + 0.2 for x in xs], reg, width=0.38, color=S2, zorder=3,
           label="Regular season win %")
    ax.axhline(50, color=MUTE, linewidth=1, linestyle=(0, (4, 3)), zorder=4)
    ax.text(-0.75, 51.5, ".500", fontsize=8.5, color=MUTE, ha="left")

    ax.set_title("Detroit's August has never once told you about the season",
                 fontsize=16, color=INK, loc="left", pad=58)
    ax.text(0, 1.105, f"Lions preseason vs regular season win percentage, "
            f"{seasons[0]} to {seasons[-1]}",
            transform=ax.transAxes, fontsize=10.5, color=MUTE)
    ax.set_ylabel("Win percentage", color=MUTE, fontsize=10.5)
    ax.set_xticks(xs)
    ax.set_xticklabels([str(s) for s in seasons], rotation=45, ha="right")
    ax.set_ylim(0, 106)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.tick_params(colors=MUTE, labelsize=9, length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    # Above the plot entirely, so it cannot land on 2008's 100% bar.
    ax.legend(frameon=False, fontsize=10, labelcolor=INK, loc="lower left",
              ncols=2, bbox_to_anchor=(0, 1.005))

    # No per-season callouts. His call 2026-08-13. The years are on the axis,
    # so anyone who wants 2008 can find 2008; annotating it tells a reader which
    # bars to care about, and the point is that none of them behave.

    n = len(rows)
    mp = sum(r["pre_pct"] for r in rows) / n
    mr = sum(r["reg_pct"] for r in rows) / n
    sp = sum((r["pre_pct"] - mp) * (r["reg_pct"] - mr) for r in rows)
    vp = sum((r["pre_pct"] - mp) ** 2 for r in rows) ** 0.5
    vr = sum((r["reg_pct"] - mr) ** 2 for r in rows) ** 0.5
    corr = sp / (vp * vr) if vp and vr else 0.0

    fig.text(0.012, 0.070,
             f"Across these {n} seasons the correlation between Detroit's "
             f"August and its regular season is {corr:+.2f}, which is "
             f"{corr ** 2 * 100:.0f}% of the variance.\nThe bars agree when they "
             "feel like it.",
             fontsize=8.8, color=INK, linespacing=1.5)
    fig.text(0.012, 0.008,
             "ESPN public schedule endpoint. 2020 excluded, no preseason was "
             "played. Ties count as half a win.\nWin percentage rather than "
             "win totals, since preseasons are 3, 4 or 5 games and seasons are "
             "16 or 17.",
             fontsize=7.6, color=MUTE, linespacing=1.5)
    fig.tight_layout(rect=(0, 0.145, 1, 1))
    fig.savefig(OUT, facecolor=CARD)
    print(f"wrote {OUT}")


def scatter(rows: list[dict]) -> None:
    """One dot per season, and the trend line the dots refuse to make.

    The paired bars answer "what happened each year". This answers the question
    underneath it: does a better August go with a better season at all? A
    scatter is the honest form for that, because a fitted line through a cloud
    is visibly a line through a cloud, where a correlation quoted in prose can
    sound like a finding.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = [r["pre_pct"] * 100 for r in rows]
    y = [r["reg_pct"] * 100 for r in rows]
    n = len(rows)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    slope = sxy / sxx if sxx else 0.0
    intercept = my - slope * mx
    corr = sxy / ((sxx ** 0.5) * (syy ** 0.5)) if sxx and syy else 0.0

    fig, ax = plt.subplots(figsize=(9.4, 6.4), dpi=130)
    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    ax.axhline(50, color=RULE, linewidth=1, zorder=1)
    ax.axvline(50, color=RULE, linewidth=1, zorder=1)

    # The fit, drawn across the observed range only. Extending it to the axis
    # edges would imply data where there is none.
    lo, hi = min(x), max(x)
    ax.plot([lo, hi], [slope * lo + intercept, slope * hi + intercept],
            color=S2, linewidth=2, zorder=3)

    ax.scatter(x, y, s=110, color=S1, zorder=4, edgecolor=CARD, linewidth=1.5)

    # No labelled seasons. His call 2026-08-13, and it is right for a scatter in
    # particular: labelling 4 dots turns a cloud into 4 anecdotes and an
    # audience argues anecdotes. The shape of the cloud is the finding.

    ax.set_title("19 seasons of Lions Augusts, plotted against what followed",
                 fontsize=15.5, color=INK, loc="left", pad=34)
    ax.text(0, 1.045, f"Each dot is one season, {rows[0]['season']} to "
            f"{rows[-1]['season']}. The line is the best fit through them.",
            transform=ax.transAxes, fontsize=10.5, color=MUTE)
    ax.set_xlabel("Preseason win percentage", color=MUTE, fontsize=10.5)
    ax.set_ylabel("Regular season win percentage", color=MUTE, fontsize=10.5)
    ax.set_xlim(-8, 112)
    ax.set_ylim(-8, 110)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.tick_params(colors=MUTE, labelsize=9.5, length=0)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(color=RULE, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)

    fig.text(0.012, 0.070,
             f"The fit rises {slope * 100:.0f} points of season win rate for "
             f"every 100 points of preseason win rate, and r is {corr:+.2f}, so "
             f"it explains {corr ** 2 * 100:.0f}% of the\nvariance. With "
             f"{n} dots that is indistinguishable from a flat line drawn "
             "through the middle.",
             fontsize=8.8, color=INK, linespacing=1.5)
    fig.text(0.012, 0.008,
             "ESPN public schedule endpoint. 2020 excluded, no preseason was "
             "played. Ties count as half a win.\nWin percentage on both axes, "
             "since preseasons are 3, 4 or 5 games and seasons are 16 or 17.",
             fontsize=7.6, color=MUTE, linespacing=1.5)
    fig.tight_layout(rect=(0, 0.135, 1, 1))
    out = os.path.join(HERE, "last_lions_scatter.png")
    fig.savefig(out, facecolor=CARD)
    print(f"wrote {out}")
    print(f"slope {slope:.3f}, r {corr:+.3f}, r2 {corr ** 2 * 100:.1f}%")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--scatter", action="store_true")
    a = ap.parse_args()
    rows = build()
    report(rows)
    if a.png:
        png(rows)
    if a.scatter:
        scatter(rows)
