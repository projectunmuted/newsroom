"""Scatter of every NBA team's opening 4: opponent strength against expected wins.

The argument the chart carries: those are two different questions. A team can
draw the hardest opponents in the league and still be favoured in most of the
games, because the schedule is only half of it.

Colours come from the site's CSS custom properties so the figure follows light
and dark mode. Usage: python scripts/nba_opening_chart.py [n] > out.svg
"""
import importlib.util, sys

_spec = importlib.util.spec_from_file_location("sos", __file__.replace("nba_opening_chart.py", "nba_opening_sos.py"))
sos = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sos)

W, H = 640, 420
L, R, T, B = 48, 14, 52, 46


def build(rows, n, highlight="DET"):
    xs = [r["opp_pct"] for r in rows]
    ys = [r["exp_wins"] for r in rows]
    x0, x1 = min(xs) - 0.015, max(xs) + 0.015
    y0, y1 = min(ys) - 0.15, max(ys) + 0.15
    px = lambda v: L + (v - x0) / (x1 - x0) * (W - L - R)
    py = lambda v: T + (1 - (v - y0) / (y1 - y0)) * (H - T - B)

    det = next(r for r in rows if r["team"] == highlight)
    out = [
        f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="nos-title" '
        f'style="max-width:{W}px;height:auto;font-family:ui-sans-serif,system-ui,'
        f"-apple-system,'Segoe UI',Roboto,sans-serif\">",
        f'<title id="nos-title">Every NBA team\'s first {n} games of 2026-27. Horizontal axis '
        f'is the mean 2025-26 winning percentage of the opponents drawn, vertical axis is how '
        f'many of the {n} the team would be expected to win given its own 2025-26 record and '
        f'where the games are played. Detroit sits far right at {det["opp_pct"]:.3f} and high '
        f'at {det["exp_wins"]:.2f} expected wins, so it drew hard opponents and is still '
        f'favoured in most of them.</title>',
        f'<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
        f'Opponent strength against expected wins, first {n} games of 2026-27</text>',
        '<text x="0" y="34" fill="var(--muted)" font-size="11">'
        'Opponents rated by 2025-26 record. Expected wins from the same records, adjusted for home and away</text>',
    ]
    for gx in [x for x in (0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65) if x0 < x < x1]:
        out.append(f'<line x1="{px(gx):.1f}" y1="{T}" x2="{px(gx):.1f}" y2="{H-B}" '
                   f'stroke="var(--rule)" stroke-width="1" stroke-dasharray="3 5"/>')
        out.append(f'<text x="{px(gx):.1f}" y="{H-B+15}" text-anchor="middle" '
                   f'fill="var(--muted)" font-size="10">.{int(round(gx*1000)):03d}</text>')
    for gy in [y for y in (1.0, 1.5, 2.0, 2.5, 3.0) if y0 < y < y1]:
        out.append(f'<line x1="{L}" y1="{py(gy):.1f}" x2="{W-R}" y2="{py(gy):.1f}" '
                   f'stroke="var(--rule)" stroke-width="1" stroke-dasharray="3 5"/>')
        out.append(f'<text x="{L-6}" y="{py(gy)+3:.1f}" text-anchor="end" '
                   f'fill="var(--muted)" font-size="10">{gy:.1f}</text>')
    for r in rows:
        hit = r["team"] == highlight
        col = "var(--chart-neg)" if hit else "var(--chart-pos)"
        out.append(f'<circle cx="{px(r["opp_pct"]):.1f}" cy="{py(r["exp_wins"]):.1f}" '
                   f'r="{6.5 if hit else 4.5}" fill="{col}" opacity="{1 if hit else 0.5}">'
                   f'<title>{r["team"]}: opponents {r["opp_pct"]:.3f}, '
                   f'{r["exp_wins"]:.2f} expected wins, {r["road"]} on the road</title></circle>')
        if hit:
            out.append(f'<text x="{px(r["opp_pct"])-11:.1f}" y="{py(r["exp_wins"])+4:.1f}" '
                       f'text-anchor="end" fill="var(--fg)" font-size="11" '
                       f'font-weight="600">Detroit</text>')
    out.append(f'<text x="{W/2:.0f}" y="{H-6}" text-anchor="middle" fill="var(--muted)" '
               f'font-size="10">Mean opponent 2025-26 winning percentage, harder to the right</text>')
    out.append(f'<text x="12" y="{T-8}" fill="var(--muted)" font-size="10">Expected wins</text>')
    out.append('</svg>')
    return "\n".join(out)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    prior = sos.prior_records()
    sos.TEAMS = sorted(prior)
    _, _, hpct = sos.home_win_pct()
    ho = hpct / (1 - hpct)
    rows = []
    for t in sos.TEAMS:
        first = sos.schedule(t)[:n]
        rows.append({
            "team": t,
            "opp_pct": sum(prior[o][2] for _, o, _, _, _ in first) / n,
            "road": sum(1 for _, _, h, _, _ in first if not h),
            "exp_wins": sum(sos.log5(prior[t][2], prior[o][2], ho if h else 1 / ho)
                            for _, o, h, _, _ in first),
        })
    sys.stdout.write(build(rows, n))


if __name__ == "__main__":
    main()
