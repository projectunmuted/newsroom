"""Bar chart: mean regular-season win rate by preseason record, 3-game era.

Reads the published dataset
(datasets/nfl-preseason-vs-regular-season-2000-2025.csv) so the chart cannot
drift from the CSV a reader can download. Bars are the deviation from .500,
drawn against a zero rule, same convention as pythag_chart.py.

Colors come from the site's CSS custom properties (--chart-pos, --chart-neg,
--fg, --muted, --rule) so the figure follows light and dark mode.

Usage: python scripts/preseason_bucket_chart.py [games] > chart.svg
       games defaults to 3 (the 2021-onward preseason length).
"""
import csv
import pathlib
import statistics
import sys

CSV = (pathlib.Path(__file__).resolve().parent.parent / "datasets"
       / "nfl-preseason-vs-regular-season-2000-2025.csv")

PAD_L, PAD_R, TOP, BOTTOM = 74, 56, 44, 14
BAR_H, ROW_GAP = 26, 12


def buckets(games: int) -> list[dict]:
    rows = []
    with CSV.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if float(r["preseason_games"]) != games:
                continue
            rows.append((float(r["preseason_wins"]),
                         float(r["regular_win_pct"])))
    out = []
    for w in range(games, -1, -1):
        vals = [p for pw, p in rows if pw == w]
        if not vals:
            continue
        out.append({"label": f"{w}-{games - w}", "n": len(vals),
                    "mean": statistics.mean(vals)})
    return out


def bar_path(x0: float, x1: float, y: float, h: float, r: float = 4.0) -> str:
    if abs(x1 - x0) < r:
        return f"M{x0},{y}H{x1}V{y+h}H{x0}Z"
    if x1 > x0:
        return (f"M{x0},{y}H{x1-r}A{r},{r} 0 0 1 {x1},{y+r}"
                f"V{y+h-r}A{r},{r} 0 0 1 {x1-r},{y+h}H{x0}Z")
    return (f"M{x0},{y}H{x1+r}A{r},{r} 0 0 0 {x1},{y+r}"
            f"V{y+h-r}A{r},{r} 0 0 0 {x1+r},{y+h}H{x0}Z")


def build(rows: list[dict], games: int, width: int = 640) -> str:
    devs = [r["mean"] - 0.5 for r in rows]
    lim = max(0.06, max(abs(d) for d in devs) * 1.35)
    plot_w = width - PAD_L - PAD_R
    to_x = lambda v: PAD_L + (v + lim) / (2 * lim) * plot_w
    zero = to_x(0)
    height = TOP + len(rows) * (BAR_H + ROW_GAP) - ROW_GAP + BOTTOM

    out = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-labelledby="pre-title" style="max-width:{width}px;height:auto;'
        f"font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,"
        f'sans-serif">',
        f'<title id="pre-title">Mean regular-season win rate by preseason '
        f'record, {games}-game preseasons</title>',
        '<text x="0" y="16" fill="var(--fg)" font-size="13" '
        'font-weight="600">Regular-season win rate, above or below .500</text>',
        f'<text x="0" y="34" fill="var(--muted)" font-size="11">By preseason '
        f'record. {games}-game preseasons only, 2000 to 2025.</text>',
        f'<line x1="{zero:.1f}" y1="{TOP-6}" x2="{zero:.1f}" '
        f'y2="{height-BOTTOM+6:.1f}" stroke="var(--rule)" stroke-width="2"/>',
    ]
    for i, r in enumerate(rows):
        y = TOP + i * (BAR_H + ROW_GAP)
        dev = r["mean"] - 0.5
        x_end = to_x(dev)
        color = "var(--chart-pos)" if dev >= 0 else "var(--chart-neg)"
        x_start = zero + (2 if dev >= 0 else -2)
        out.append(
            f'<text x="{PAD_L-12}" y="{y+BAR_H/2+4:.1f}" text-anchor="end" '
            f'fill="var(--fg)" font-size="12.5">{r["label"]}</text>')
        out.append(
            f'<path d="{bar_path(x_start, x_end, y, BAR_H)}" fill="{color}">'
            f'<title>{r["label"]} preseason, n={r["n"]}: mean regular-season '
            f'win rate {r["mean"]:.3f}</title></path>')
        anchor, dx = ("start", 8) if dev >= 0 else ("end", -8)
        out.append(
            f'<text x="{x_end+dx:.1f}" y="{y+BAR_H/2+4:.1f}" '
            f'text-anchor="{anchor}" fill="var(--muted)" font-size="12" '
            f'font-variant-numeric="tabular-nums">{r["mean"]:.3f}'
            f' (n={r["n"]})</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print(build(buckets(g), g))
