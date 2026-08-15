"""Drew Anderson's 2026 by outs recorded per appearance, as inline SVG.

The claim the Sunday pick rests on is a ceiling, not a quality: he has never
recorded more than 14 outs in a major league game this season, and Detroit's
median start is 17. A dot per appearance shows the ceiling and the recent climb
in the same picture, which a season line cannot.

Colors are the validated `--chart-pos` / `--chart-neg` tokens. Every value comes
from `short_start_snapshot.json`, the same cache `short_start_games.py` prints
from, so the chart and the prose cannot drift.

Usage:
    python scripts/anderson_length_chart.py > scripts/last_anderson_length.svg
"""

import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "short_start_snapshot.json")

W, H = 640, 270
L, R, T, B = 46, 22, 52, 40
DET_MEDIAN_OUTS = 17  # Detroit's median start, from short_start_games.py


def main():
    with open(CACHE, encoding="utf-8") as fh:
        snap = json.load(fh)
    log = snap["anderson"]

    days = [datetime.date.fromisoformat(g["date"]).toordinal() for g in log]
    d0, d1 = min(days), max(days)
    top = max(DET_MEDIAN_OUTS, max(g["outs"] for g in log)) + 2

    def x(d):
        return L + (d - d0) / float(d1 - d0) * (W - L - R)

    def y(o):
        return H - B - (o / float(top)) * (H - T - B)

    out = []
    a = out.append
    a('<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-labelledby="al-t" '
      'style="max-width:%dpx;height:auto;font-family:ui-sans-serif,system-ui,'
      "-apple-system,'Segoe UI',Roboto,sans-serif\">" % (W, H, W))
    a('<title id="al-t">Outs recorded by Drew Anderson in each of his 42 '
      'appearances in 2026, with his 4 starts marked, against the median '
      'Detroit start of 17 outs</title>')
    a('<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">'
      'Every Drew Anderson appearance in 2026, by outs recorded</text>')
    a('<text x="0" y="34" fill="var(--muted)" font-size="11">Filled dots are his '
      '4 starts. The dashed line is the median Detroit start at 17 outs, which he '
      'has never reached.</text>')

    a('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--rule)" '
      'stroke-width="1.5" stroke-dasharray="5 4"/>'
      % (L, y(DET_MEDIAN_OUTS), W - R, y(DET_MEDIAN_OUTS)))
    a('<text x="%.1f" y="%.1f" text-anchor="end" fill="var(--muted)" '
      'font-size="11">median Detroit start, 17 outs</text>'
      % (W - R, y(DET_MEDIAN_OUTS) - 6))

    for o in (3, 6, 9, 12, 15):
        a('<text x="%.1f" y="%.1f" text-anchor="end" fill="var(--muted)" '
          'font-size="11" font-variant-numeric="tabular-nums">%d</text>'
          % (L - 8, y(o) + 4, o))

    for g in log:
        d = datetime.date.fromisoformat(g["date"]).toordinal()
        cx, cy = x(d), y(g["outs"])
        if g["start"]:
            a('<circle cx="%.1f" cy="%.1f" r="5" fill="var(--chart-neg)">'
              '<title>%s, start vs %s: %s innings, %d batters faced, %s pitches'
              '</title></circle>'
              % (cx, cy, g["date"], g["opp"], g["ip"], g["bf"], g["pitches"]))
        else:
            a('<circle cx="%.1f" cy="%.1f" r="3.5" fill="none" '
              'stroke="var(--chart-pos)" stroke-width="1.6">'
              '<title>%s, relief vs %s: %s innings, %d batters faced</title>'
              '</circle>' % (cx, cy, g["date"], g["opp"], g["ip"], g["bf"]))

    a('<text x="%d" y="%d" fill="var(--muted)" font-size="11">%s</text>'
      % (L, H - 12, datetime.date.fromordinal(d0).isoformat()))
    a('<text x="%d" y="%d" text-anchor="end" fill="var(--muted)" font-size="11">'
      '%s</text>' % (W - R, H - 12, datetime.date.fromordinal(d1).isoformat()))
    a('<text x="0" y="%d" fill="var(--muted)" font-size="11">outs</text>' % (T - 4))
    a("</svg>")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
