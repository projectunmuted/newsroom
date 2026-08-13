#!/usr/bin/env python3
"""Detroit's outfielders, out and available, measured against replacement level.

Bars are anchored at the replacement baseline rather than at zero, because the
whole question of the piece is what each man is worth *over the guy who takes
his place*. Bar length is therefore the argument itself: Greene is long,
Carpenter is short, Vierling points the other way.

Imports bar_path from pythag_chart rather than copying it, per the standing
habit in this repo.

Usage:  python scripts/outfield_chart.py [--refresh]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from pythag_chart import bar_path  # noqa: E402
from tigers_outfield import load  # noqa: E402

PAD_L = 132
PAD_R = 18
TOP = 62
BOTTOM = 46
BAR_H = 20
ROW_GAP = 8


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build(rows, repl, league, width=640):
    """rows: list of (name, detail, ops, is_out)."""
    vals = [r[2] for r in rows]
    lo = min(min(vals), repl) - 0.05
    hi = max(max(vals), league) + 0.05
    plot_w = width - PAD_L - PAD_R
    span = hi - lo
    to_x = lambda v: PAD_L + (v - lo) / span * plot_w
    base = to_x(repl)

    height = TOP + len(rows) * (BAR_H + ROW_GAP) - ROW_GAP + BOTTOM
    out = [
        '<svg viewBox="0 0 %d %d" width="100%%" role="img" '
        'aria-labelledby="of-title of-desc" '
        'style="max-width:%dpx;height:auto;font-family:ui-sans-serif,'
        "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif\">" % (width, height, width),
        '<title id="of-title">Detroit outfielders by OPS, measured against '
        'replacement level</title>',
        '<desc id="of-desc">Riley Greene sits well above the replacement '
        'baseline. Kerry Carpenter sits a little above it and Matt Vierling '
        'sits below it, so 2 of the 3 injured outfielders were producing at or '
        'under the level of the players replacing them.</desc>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        'Only 1 of the 3 was hitting</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">'
        'Bars run from replacement level (%.3f OPS, the league\'s own '
        'under-150-PA hitters). Right is better.</text>' % repl,
    ]

    # league average reference
    lx = to_x(league)
    out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--rule)" '
               'stroke-width="1" stroke-dasharray="3 3"/>'
               % (lx, TOP - 8, lx, height - BOTTOM + 6))
    out.append('<text x="%.1f" y="%d" fill="var(--muted)" font-size="10" '
               'text-anchor="middle">league %.3f</text>'
               % (lx, height - BOTTOM + 20, league))

    y = TOP
    for name, detail, ops, is_out in rows:
        x = to_x(ops)
        colour = "var(--chart-pos)" if ops >= repl else "var(--chart-neg)"
        opacity = "1" if is_out else "0.42"
        out.append('<text x="%d" y="%d" fill="var(--fg)" font-size="11" '
                   'text-anchor="end" font-weight="%s">%s</text>'
                   % (PAD_L - 8, y + 14, "600" if is_out else "400", esc(name)))
        out.append('<path d="%s" fill="%s" opacity="%s"><title>%s: %s</title></path>'
                   % (bar_path(base, x, y, BAR_H), colour, opacity,
                      esc(name), esc(detail)))
        label_x = x + 6 if ops >= repl else x - 6
        anchor = "start" if ops >= repl else "end"
        out.append('<text x="%.1f" y="%d" fill="var(--muted)" font-size="10" '
                   'text-anchor="%s">%.3f</text>' % (label_x, y + 14, anchor, ops))
        y += BAR_H + ROW_GAP

    # baseline on top of the bars
    out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="var(--fg)" '
               'stroke-width="1.5"/>' % (base, TOP - 8, base, height - BOTTOM + 6))
    out.append('<text x="%.1f" y="%d" fill="var(--fg)" font-size="10" '
               'text-anchor="middle" font-weight="600">replacement %.3f</text>'
               % (base, height - BOTTOM + 34, repl))
    out.append('<text x="0" y="%d" fill="var(--muted)" font-size="10">'
               'Solid bars are the injured. Faded bars are the men taking the '
               'at-bats.</text>' % (height - 6))
    out.append("</svg>")
    return "\n".join(out)


def main():
    d = load("--refresh" in sys.argv)
    repl = d["replacement_ops"]
    teams = d["teams"]
    lg_pa = sum(t["pa"] for t in teams)
    league = sum(t["ops"] * t["pa"] for t in teams) / lg_pa

    by_name = {p["name"]: p for p in d["tigers"]}
    active = d["active"]

    order = [
        ("Riley Greene", True),
        ("Kerry Carpenter", True),
        ("Matt Vierling", True),
        ("Max Clark", False),
        ("Ben Malgeri", False),
        ("James Outman", False),
    ]
    rows = []
    for name, is_out in order:
        p = by_name.get(name)
        if p is None:
            print("  ! %s not in the data, skipping" % name, file=sys.stderr)
            continue
        if is_out and p["id"] in active:
            print("  ! %s is on the active roster now; the chart is stale"
                  % name, file=sys.stderr)
        detail = "%d PA, %.3f OPS" % (p["pa"], p["ops"])
        rows.append((name, detail, p["ops"], is_out))

    svg = build(rows, repl, round(league, 3))
    path = os.path.join(os.path.dirname(__file__), "last_outfield_chart.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(svg)
    print("\nwrote %s" % path, file=sys.stderr)


if __name__ == "__main__":
    main()
