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

# Site tokens, already validated for colorblind separation and for contrast in
# both themes. Reused rather than re-picked so every chart matches.
POS = "#1b7a5a"
NEG = "#b4472f"
INK = "#1a1a19"
MUTE = "#6b6a66"
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

    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=120)
    fig.patch.set_facecolor(CARD)
    ax.set_facecolor(CARD)

    ax.bar([x - 0.21 for x in xs], obs, width=0.42, color=POS,
           label=f"Won every preseason game (n={nu})")
    ax.bar([x + 0.21 for x in xs], exp, width=0.42, color=MUTE, alpha=0.55,
           label=f"Every team (n={n})")

    ax.set_title("Undefeated in August, then what?\nRegular season wins, "
                 "2015 to 2025, per 17 games",
                 fontsize=14, color=INK, loc="left", pad=14)
    ax.set_xlabel("Regular season wins (per 17 games)", color=MUTE, fontsize=10)
    ax.set_ylabel("Share of group", color=MUTE, fontsize=10)
    ax.set_xticks(xs)
    ax.tick_params(colors=MUTE, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#e3e0d9")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="y", color="#e3e0d9", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=9.5, labelcolor=INK)

    worst = min(u, key=lambda r: r["reg_w"])
    best = max(u, key=lambda r: r["reg_w"])
    ax.annotate(f"{worst['team'].upper()} {worst['season']}: {worst['reg_w']:g}-"
                f"{worst['reg_g'] - worst['reg_w']:g}",
                xy=(pace(worst), hu[pace(worst)] / nu * 100), xytext=(0.6, 9),
                fontsize=9, color=NEG,
                arrowprops=dict(arrowstyle="-", color=NEG, lw=0.9))
    ax.annotate(f"{best['team'].upper()} {best['season']}: {best['reg_w']:g}-"
                f"{best['reg_g'] - best['reg_w']:g}",
                xy=(pace(best), hu[pace(best)] / nu * 100), xytext=(13.4, 12),
                fontsize=9, color=POS,
                arrowprops=dict(arrowstyle="-", color=POS, lw=0.9))

    fig.text(0.012, 0.015,
             "ESPN public schedule endpoint. 2020 excluded, no preseason. "
             "Ties count as half a win. 16 and 17 game seasons both included, "
             "so wins are shown per 17.",
             fontsize=7.6, color=MUTE)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(OUT, facecolor=CARD)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args()
    report()
    if a.png:
        png()
