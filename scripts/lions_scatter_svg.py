#!/usr/bin/env python3
"""The scatter a reader asked for, as inline SVG, from the corrected cache.

Asked in the r/detroitlions thread `1vne8nx` on 2026-08-13: "Is there a way to
specifically show Lions for the last 20 seasons. What was their win percent in
the offseason compared to win percent during the season", then "make it a
scatter plot, to see if there's a trend line at all."

It was answered into a PNG on a disk, which nobody could reach. This renders it
as the inline SVG the site actually publishes, and it reads
`preseason_cache_2000.json`, the same file behind the 798 team-season backtest,
so Detroit's rows here cannot disagree with the rows already in print. The older
`lions_preseason_20.py` predates the 0-0-is-not-a-tie fix and has 2001 as
2.5-13.5; here it is 2-13.

    python scripts/lions_scatter_svg.py            # numbers
    python scripts/lions_scatter_svg.py --chart    # the SVG

Identical seasons land on identical coordinates, so dots are grouped and sized
by how many seasons they hold rather than jittered, which would put a dot where
no season is.
"""

from __future__ import annotations

import argparse
import json
import os

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "preseason_cache_2000.json")
TEAM = "det"


def rows() -> list[dict]:
    data = json.load(open(CACHE, encoding="utf-8"))
    out = [r for r in data if r["team"] == TEAM]
    return sorted(out, key=lambda r: r["season"])


def fit(rs: list[dict]) -> dict:
    n = len(rs)
    x = [r["pre_pct"] for r in rs]
    y = [r["reg_pct"] for r in rs]
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    slope = sxy / sxx if sxx else 0.0
    return {
        "n": n, "slope": slope, "intercept": my - slope * mx,
        "r": sxy / ((sxx ** 0.5) * (syy ** 0.5)) if sxx and syy else 0.0,
        "mean_pre": mx, "mean_reg": my,
    }


def permutation_p(rs: list[dict], trials: int = 20000) -> float:
    """How often chance alone beats the observed correlation.

    25 dots is few enough that a correlation can look like something and be
    nothing, and quoting r without this is how a non-finding gets published as
    a finding. The seed is fixed, so this returns the same answer every run and
    a later cycle can check it.
    """
    import random

    observed = abs(fit(rs)["r"])
    seasons = [dict(r) for r in rs]
    reg = [r["reg_pct"] for r in seasons]
    rng = random.Random(20260815)
    hits = 0
    for _ in range(trials):
        rng.shuffle(reg)
        for row, value in zip(seasons, reg):
            row["reg_pct"] = value
        if abs(fit(seasons)["r"]) >= observed:
            hits += 1
    return hits / trials


def leave_one_out(rs: list[dict]) -> list[tuple[int, float]]:
    """Drop each season in turn. One dot should not be carrying the answer."""
    return sorted(
        ((rs[i]["season"], fit(rs[:i] + rs[i + 1:])["r"]) for i in range(len(rs))),
        key=lambda t: t[1])


def build(rs: list[dict], f: dict, width: int = 640) -> str:
    pad_l, pad_r, top, bottom = 52, 18, 56, 60
    height = 430
    plot_w = width - pad_l - pad_r
    plot_h = height - top - bottom
    to_x = lambda v: pad_l + v * plot_w
    to_y = lambda v: top + (1 - v) * plot_h

    groups: dict[tuple[float, float], list[dict]] = {}
    for r in rs:
        groups.setdefault((r["pre_pct"], r["reg_pct"]), []).append(r)

    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="ls-title" style="max-width:{width}px;height:auto;'
        f'font-family:ui-sans-serif,system-ui,-apple-system,\'Segoe UI\','
        f'Roboto,sans-serif">',
        f'<title id="ls-title">Detroit\'s preseason win rate plotted against '
        f'its regular season win rate, {rs[0]["season"]} to '
        f'{rs[-1]["season"]}, with the best fit line through the '
        f'{f["n"]} seasons</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">Detroit\'s August against the season that '
        'followed</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">One dot per '
        f'season, {rs[0]["season"]} to {rs[-1]["season"]}. A bigger dot is more '
        f'than one season landing on the same spot. The line is the best fit '
        f'through all {f["n"]}.</text>',
    ]

    for v in (0.0, 0.25, 0.5, 0.75, 1.0):
        gx, gy = to_x(v), to_y(v)
        out.append(f'<line x1="{gx:.1f}" y1="{top}" x2="{gx:.1f}" '
                   f'y2="{top + plot_h}" stroke="var(--rule)" '
                   f'stroke-width="1"/>')
        out.append(f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{pad_l + plot_w}" '
                   f'y2="{gy:.1f}" stroke="var(--rule)" stroke-width="1"/>')
        label = f"{v:.3f}".lstrip("0") if v else "0"
        out.append(f'<text x="{gx:.1f}" y="{top + plot_h + 18:.1f}" '
                   f'text-anchor="middle" fill="var(--muted)" font-size="11" '
                   f'font-variant-numeric="tabular-nums">{label}</text>')
        out.append(f'<text x="{pad_l - 8}" y="{gy + 4:.1f}" text-anchor="end" '
                   f'fill="var(--muted)" font-size="11" '
                   f'font-variant-numeric="tabular-nums">{label}</text>')

    lo = min(r["pre_pct"] for r in rs)
    hi = max(r["pre_pct"] for r in rs)
    out.append(
        f'<line x1="{to_x(lo):.1f}" y1="{to_y(f["slope"] * lo + f["intercept"]):.1f}" '
        f'x2="{to_x(hi):.1f}" y2="{to_y(f["slope"] * hi + f["intercept"]):.1f}" '
        f'stroke="var(--chart-neg)" stroke-width="2.5"/>')

    for (px, py), seasons in sorted(groups.items()):
        r = 5.5 * (len(seasons) ** 0.5)
        names = ", ".join(
            f'{s["season"]} ({s["pre_w"]:g}-{s["pre_g"] - s["pre_w"]:g} '
            f'August, {s["reg_w"]:g}-{s["reg_g"] - s["reg_w"]:g} season)'
            for s in seasons)
        out.append(f'<circle cx="{to_x(px):.1f}" cy="{to_y(py):.1f}" '
                   f'r="{r:.1f}" fill="var(--chart-pos)" fill-opacity="0.85">'
                   f'<title>{names}</title></circle>')

    out.append(f'<text x="{pad_l + plot_w / 2:.1f}" y="{height - 26}" '
               f'text-anchor="middle" fill="var(--muted)" font-size="11.5">'
               f'Preseason win rate</text>')
    out.append(f'<text x="14" y="{top + plot_h / 2:.1f}" '
               f'transform="rotate(-90 14 {top + plot_h / 2:.1f})" '
               f'text-anchor="middle" fill="var(--muted)" font-size="11.5">'
               f'Regular season win rate</text>')
    out.append(f'<text x="{pad_l + plot_w:.1f}" y="{height - 6}" '
               f'text-anchor="end" fill="var(--muted)" font-size="10.5">'
               f'r = {f["r"]:+.2f}, so August explains '
               f'{f["r"] ** 2 * 100:.1f}% of the season</text>')
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chart", action="store_true")
    args = ap.parse_args()

    rs = rows()
    f = fit(rs)
    if args.chart:
        print(build(rs, f))
        return

    print(f"Detroit, {f['n']} seasons, {rs[0]['season']} to {rs[-1]['season']}"
          f"  (2020 absent, no preseason was played)\n")
    print("season   August    season      pre    reg")
    for r in rs:
        print(f"  {r['season']}   {r['pre_w']:g}-{r['pre_g'] - r['pre_w']:g}"
              f"       {r['reg_w']:>4g}-{r['reg_g'] - r['reg_w']:<4g}"
              f"  {r['pre_pct']:.3f}  {r['reg_pct']:.3f}")
    print(f"\nmean August {f['mean_pre']:.3f}, mean season {f['mean_reg']:.3f}")
    print(f"slope {f['slope']:.3f} (per 1.000 of August win rate), "
          f"r {f['r']:+.3f}, r squared {f['r'] ** 2 * 100:.1f}%")

    p = permutation_p(rs)
    print(f"permutation test: {p * 100:.1f}% of 20,000 shuffles of the same "
          f"25 seasons produce a correlation at least this strong")
    loo = leave_one_out(rs)
    print(f"leave one out: r runs {loo[0][1]:+.3f} (without {loo[0][0]}) to "
          f"{loo[-1][1]:+.3f} (without {loo[-1][0]})")

    dupes = {}
    for r in rs:
        dupes.setdefault((r["pre_pct"], r["reg_pct"]), []).append(r["season"])
    for spot, seasons in sorted(dupes.items()):
        if len(seasons) > 1:
            print(f"  same spot: {seasons} at {spot[0]:.3f}, {spot[1]:.3f}")


if __name__ == "__main__":
    main()
