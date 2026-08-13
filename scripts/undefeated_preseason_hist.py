#!/usr/bin/env python3
"""Where did the 39 undefeated-preseason teams actually finish?

A reader on r/detroitlions asked the obvious follow-up to the backtest: the
group averages .466, fine, but what does the spread look like? An average can
hide two completely different worlds. A tight cluster around 8 wins would mean
"an undefeated August makes you mediocre", which would be a real finding. A flat
smear across the whole range means the preseason record told you nothing about
this team, which is the opposite claim.

It is the second one, and it is not close.

Reads `preseason_cache.json`, the same receipt the backtest uses, so this cannot
disagree with the published piece. Nothing is hand-entered.

    python scripts/undefeated_preseason_hist.py           # numbers to stdout
    python scripts/undefeated_preseason_hist.py --png     # attachable PNG

Seasons run 2015-2025 with 2020 excluded (no preseason). 16-game and 17-game
seasons are both in here, so anything comparing the two is stated as a win pace
over 17 rather than a raw win total. Ties count as half a win.
"""

from __future__ import annotations

import argparse
import collections
import json
import os

CACHE = os.path.join(os.path.dirname(__file__), "preseason_cache.json")
OUT = os.path.join(os.path.dirname(__file__), "last_undefeated_hist.png")

# Categorical slots 1 and 2. Neither series is good or bad here, so the site's
# pos/neg tokens would be lying: this is identity, not polarity. Validated
# together on the light surface, worst adjacent pair ΔE 24.7 protan, 33.6 normal,
# both well clear of the floor.
S1 = "#2a78d6"   # the 39 undefeated teams
S2 = "#eb6834"   # every team, the reference
INK = "#1a1a19"
MUTE = "#6b6a66"
RULE = "#e3e0d9"
CARD = "#ffffff"


def load() -> tuple[list[dict], list[dict]]:
    rows = [r for r in json.load(open(CACHE, encoding="utf-8")) if r["pre_g"] > 0]
    undefeated = [r for r in rows if r["pre_w"] == r["pre_g"]]
    return rows, undefeated


def pace(r: dict) -> int:
    """Wins per 17 games, rounded. 13 of these seasons are 16-game and 26 are
    17-game; comparing raw win totals across that would be quietly wrong."""
    return min(17, int(round(r["reg_pct"] * 17)))


def report() -> None:
    rows, u = load()
    n, nu = len(rows), len(u)
    hu = collections.Counter(pace(r) for r in u)
    ha = collections.Counter(pace(r) for r in rows)

    print(f"Teams that won every preseason game, {nu} of {n} team-seasons\n")
    print(" wins/17  undefeated        all teams")
    for w in range(18):
        if not (hu[w] or ha[w]):
            continue
        bar = "#" * hu[w]
        print(f"   {w:>2}     {hu[w]:>2} {bar:<10}  {ha[w] / n * 100:5.1f}%")

    raw = collections.Counter(r["reg_w"] for r in u)
    lo, hi = min(raw), max(raw)
    nine_u = sum(v for k, v in hu.items() if k >= 9) / nu * 100
    nine_a = sum(v for k, v in ha.items() if k >= 9) / n * 100
    print(f"\nrange of raw win totals: {lo:g} to {hi:g}")
    print(f"9+ wins: undefeated {nine_u:.1f}%, all teams {nine_a:.1f}%")
    print(f"mean win pct: undefeated {sum(r['reg_pct'] for r in u) / nu:.3f}, "
          f"all teams {sum(r['reg_pct'] for r in rows) / n:.3f}")

    print("\nthe tails, which are the whole point:")
    for r in sorted(u, key=lambda r: r["reg_w"])[:2]:
        print(f"   {r['team'].upper():<4} {r['season']}  {r['reg_w']:g}-"
              f"{r['reg_g'] - r['reg_w']:g}")
    for r in sorted(u, key=lambda r: -r["reg_w"])[:3]:
        print(f"   {r['team'].upper():<4} {r['season']}  {r['reg_w']:g}-"
              f"{r['reg_g'] - r['reg_w']:g}")

    # 39 across 15 occupied buckets is 2 to 3 per bucket. Any single bar moving
    # by one team is noise, and a reader is owed that before reading the shape.
    print(f"\nn = {nu} over {len([w for w in range(18) if hu[w]])} occupied "
          f"buckets. Individual bars are 1 to 7 teams; do not read a bump.")


def png() -> None:
    """One histogram, with the league drawn over it as the thing to compare to.

    The earlier version put the two groups in side-by-side bars, which makes a
    reader do the comparison 18 times. The point is a single visual claim, that
    the shapes are the same, so the league becomes one line and the eye checks
    it in one pass.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows, u = load()
    n, nu = len(rows), len(u)
    hu = collections.Counter(pace(r) for r in u)
    ha = collections.Counter(pace(r) for r in rows)
    xs = list(range(0, 18))
    obs = [hu[w] / nu * 100 for w in xs]
    exp = [ha[w] / n * 100 for w in xs]

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=130)
    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    # Bars are the group being asked about. 0.86 leaves a surface gap between
    # neighbours so a run of similar bars still reads as separate columns.
    ax.bar(xs, obs, width=0.86, color=S1, zorder=3,
           label="Teams that won every preseason game (39)")
    # The league is a reference, not a rival series, so it sits on top as a line
    # rather than stealing half the width of every bar.
    ax.plot(xs, exp, color=S2, linewidth=2, marker="o", markersize=6,
            markeredgecolor=CARD, markeredgewidth=1.5, zorder=4,
            label="Every team (320)")

    ax.set_title("They finish everywhere, same as everybody else",
                 fontsize=16, color=INK, loc="left", pad=32)
    ax.text(0, 1.035, "Regular season wins after an undefeated preseason, "
            "2015 to 2025", transform=ax.transAxes, fontsize=10.5, color=MUTE)
    ax.set_xlabel("Regular season wins, per 17 games", color=MUTE, fontsize=10.5)
    ax.set_ylabel("Share of group", color=MUTE, fontsize=10.5)
    ax.set_xticks(xs)
    ax.set_xlim(-0.8, 17.8)
    ax.tick_params(colors=MUTE, labelsize=9.5, length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="y", color=RULE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    # Headroom above the tallest bar, so the labels below have somewhere to go
    # and the legend is not sitting on the data.
    ax.set_ylim(0, max(max(obs), max(exp)) * 1.34)
    ax.legend(frameon=False, fontsize=10, labelcolor=INK, loc="upper right")

    # Only the two tails get labelled. A number on every bar would bury the one
    # thing worth seeing, and these 2 teams are the argument by themselves.
    worst, best = min(u, key=lambda r: r["reg_w"]), max(u, key=lambda r: r["reg_w"])
    for r, xoff in ((worst, 1.7), (best, -1.7)):
        x = pace(r)
        label = (f"{r['team'].upper()} {r['season']}\n"
                 f"went {r['reg_w']:g}-{r['reg_g'] - r['reg_w']:g}")
        ax.annotate(label,
                    xy=(x, hu[x] / nu * 100 + 0.3),
                    xytext=(x + xoff, hu[x] / nu * 100 + 6.0),
                    fontsize=9.5, color=INK, ha="center", linespacing=1.4,
                    arrowprops=dict(arrowstyle="-", color=MUTE, lw=1,
                                    shrinkA=2, shrinkB=3))

    fig.text(0.012, 0.070,
             "Averages are close too: .466 for the undefeated teams, .505 for "
             "the league.\nOnly 39 teams across 13 buckets, 1 to 7 per bar, so "
             "read the shape and not any single column.",
             fontsize=8.6, color=INK, linespacing=1.5)
    fig.text(0.012, 0.008,
             "ESPN public schedule endpoint. 2020 excluded, no preseason was "
             "played. Ties count as half a win.\n16 and 17 game seasons are "
             "both in here, so wins are shown per 17.",
             fontsize=7.6, color=MUTE, linespacing=1.5)
    fig.tight_layout(rect=(0, 0.145, 1, 1))
    fig.savefig(OUT, facecolor=CARD)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args()
    report()
    if a.png:
        png()
