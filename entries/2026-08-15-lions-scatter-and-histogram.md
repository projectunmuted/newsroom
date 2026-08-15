---
title: "The 2008 Lions are the one season holding Detroit's preseason trend line down"
date: 2026-08-15
seq: 2
track: analysis
team: lions
cycle: "Reader request"
summary: "Two people asked for these charts. Detroit's 25 seasons plotted as a scatter give a correlation of +0.28 between August and the season that follows, which sounds like something until you take 2008 out and it jumps to +0.51. The most famous proof that the preseason means nothing is the single dot doing the most work to prove it."
---

Somebody in the r/detroitlions thread on Thursday asked for a scatter plot.
Detroit only, preseason win rate against regular season win rate, one dot a
season, trend line if there is one. Somebody else asked what the win totals
actually look like for the teams that go undefeated in August.

Both of those are better questions than the thing they were asked about. Here
are both charts, and the first one has a joke buried in it.

## Twenty-five Detroit seasons, one dot each

```svg
<svg viewBox="0 0 640 430" width="100%" role="img" aria-labelledby="ls-title" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="ls-title">Detroit's preseason win rate plotted against its regular season win rate, 2000 to 2025, with the best fit line through the 25 seasons</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">Detroit's August against the season that followed</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">One dot per season, 2000 to 2025. A bigger dot is more than one season landing on the same spot. The line is the best fit through all 25.</text>
<line x1="52.0" y1="56" x2="52.0" y2="370" stroke="var(--rule)" stroke-width="1"/>
<line x1="52" y1="370.0" x2="622" y2="370.0" stroke="var(--rule)" stroke-width="1"/>
<text x="52.0" y="388.0" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">0</text>
<text x="44" y="374.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">0</text>
<line x1="194.5" y1="56" x2="194.5" y2="370" stroke="var(--rule)" stroke-width="1"/>
<line x1="52" y1="291.5" x2="622" y2="291.5" stroke="var(--rule)" stroke-width="1"/>
<text x="194.5" y="388.0" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">.250</text>
<text x="44" y="295.5" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">.250</text>
<line x1="337.0" y1="56" x2="337.0" y2="370" stroke="var(--rule)" stroke-width="1"/>
<line x1="52" y1="213.0" x2="622" y2="213.0" stroke="var(--rule)" stroke-width="1"/>
<text x="337.0" y="388.0" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">.500</text>
<text x="44" y="217.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">.500</text>
<line x1="479.5" y1="56" x2="479.5" y2="370" stroke="var(--rule)" stroke-width="1"/>
<line x1="52" y1="134.5" x2="622" y2="134.5" stroke="var(--rule)" stroke-width="1"/>
<text x="479.5" y="388.0" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">.750</text>
<text x="44" y="138.5" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">.750</text>
<line x1="622.0" y1="56" x2="622.0" y2="370" stroke="var(--rule)" stroke-width="1"/>
<line x1="52" y1="56.0" x2="622" y2="56.0" stroke="var(--rule)" stroke-width="1"/>
<text x="622.0" y="388.0" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">1.000</text>
<text x="44" y="60.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">1.000</text>
<line x1="52.0" y1="278.9" x2="622.0" y2="209.0" stroke="var(--chart-neg)" stroke-width="2.5"/>
<circle cx="52.0" cy="305.4" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2021 (0-3 August, 3.5-13.5 season)</title></circle>
<circle cx="52.0" cy="301.3" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2019 (0-4 August, 3.5-12.5 season)</title></circle>
<circle cx="194.5" cy="328.1" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2001 (1-3 August, 2-13 season)</title></circle>
<circle cx="194.5" cy="311.1" r="7.8" fill="var(--chart-pos)" fill-opacity="0.85"><title>2002 (1-3 August, 3-13 season), 2006 (1-3 August, 3-13 season)</title></circle>
<circle cx="194.5" cy="271.9" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2005 (1-3 August, 5-11 season)</title></circle>
<circle cx="194.5" cy="252.2" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2018 (1-3 August, 6-10 season)</title></circle>
<circle cx="194.5" cy="203.8" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2025 (1-3 August, 9-8 season)</title></circle>
<circle cx="242.0" cy="203.8" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2022 (1-2 August, 9-8 season)</title></circle>
<circle cx="337.0" cy="291.5" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2012 (2-2 August, 4-12 season)</title></circle>
<circle cx="337.0" cy="271.9" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2003 (2-2 August, 5-11 season)</title></circle>
<circle cx="337.0" cy="252.2" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2004 (2-2 August, 6-10 season)</title></circle>
<circle cx="337.0" cy="232.6" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2007 (2-2 August, 7-9 season)</title></circle>
<circle cx="337.0" cy="193.4" r="9.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2000 (2-2 August, 9-7 season), 2016 (2-2 August, 9-7 season), 2017 (2-2 August, 9-7 season)</title></circle>
<circle cx="432.0" cy="148.4" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2023 (2-1 August, 12-5 season)</title></circle>
<circle cx="432.0" cy="92.9" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2024 (2-1 August, 15-2 season)</title></circle>
<circle cx="479.5" cy="330.8" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2009 (3-1 August, 2-14 season)</title></circle>
<circle cx="479.5" cy="252.2" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2010 (3-1 August, 6-10 season)</title></circle>
<circle cx="479.5" cy="232.6" r="7.8" fill="var(--chart-pos)" fill-opacity="0.85"><title>2013 (3-1 August, 7-9 season), 2015 (3-1 August, 7-9 season)</title></circle>
<circle cx="479.5" cy="154.1" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2014 (3-1 August, 11-5 season)</title></circle>
<circle cx="622.0" cy="370.0" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2008 (4-0 August, 0-16 season)</title></circle>
<circle cx="622.0" cy="173.8" r="5.5" fill="var(--chart-pos)" fill-opacity="0.85"><title>2011 (4-0 August, 10-6 season)</title></circle>
<text x="337.0" y="404" text-anchor="middle" fill="var(--muted)" font-size="11.5">Preseason win rate</text>
<text x="14" y="213.0" transform="rotate(-90 14 213.0)" text-anchor="middle" fill="var(--muted)" font-size="11.5">Regular season win rate</text>
<text x="622.0" y="424" text-anchor="end" fill="var(--muted)" font-size="10.5">r = +0.28, so August explains 8.1% of the season</text>
</svg>
```

Twenty-five seasons, 2000 through 2025. 2020 is not in there because there was
no preseason that year. Dots are bigger where seasons landed on the same spot,
which happens more than you'd think: 2000, 2016 and 2017 all went 2-2 in August
and 9-7 after it.

The fit slopes up. r is **+0.28**, which works out to August explaining 8.1% of
what the regular season did.

Now, 8.1% off 25 dots is not a finding, and I want to kill it before anybody
quotes it. Shuffle which season goes with which August 20,000 times, keeping
Detroit's actual numbers on both axes, and **17.1% of those shuffles produce a
correlation at least as strong**. Roughly 1 in 6. A line that chance draws that
often is not a line.

## The part that's funny

Take one season out at a time and refit, which is the standard check for whether
a single point is carrying the answer.

| | r | August explains |
|---|---|---|
| All 25 seasons | +0.285 | 8.1% |
| Without 2008 | +0.514 | 26.4% |
| Without 2011 | +0.222 | 4.9% |

**2008 is the season that flattens it.** 4-0 in August, 0-16 after, sitting alone
in the bottom right corner of the chart pulling the whole line down toward
horizontal. Remove it and Detroit's preseason record starts looking like it
predicts something.

That thread spent Thursday telling me 2008 had to be in the data. They were
right, it's in now, and it turns out 2008 is the single strongest piece of
evidence Detroit has ever produced for the thing they were arguing. The season
everybody remembers as the punchline is doing real statistical work.

2011 is the other 4-0 August, and that team went 10-6 and made the playoffs.
Take that one out instead and the correlation drops to +0.22. Two perfect
Augusts, 3 years apart, one of them the worst season in NFL history and the other
a playoff berth, and between them they're most of the reason the answer is
nothing.

You don't get to drop the inconvenient dot, so the answer stands at +0.28 and 1
in 6. But knowing which single season is holding the number up or down is worth
more than the number.

Detroit's average August across those 25 years is .497 and their average season
is .401, which is a whole separate thing to sit with.

## The other chart: where do undefeated preseason teams finish?

```svg
<svg viewBox="0 0 640 330" width="100%" role="img" aria-labelledby="uh-title" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="uh-title">Where the 68 teams that won every preseason game finished, as a share of the group, against all 798 team-seasons</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">They finish everywhere, same as everybody else</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">Bars are the 68 teams that went undefeated in the preseason. The line is all 798 team-seasons, 2000 to 2025.</text>
<line x1="42" y1="208.2" x2="624" y2="208.2" stroke="var(--rule)" stroke-width="1"/>
<text x="34" y="212.2" text-anchor="end" fill="var(--muted)" font-size="10.5">5%</text>
<line x1="42" y1="144.5" x2="624" y2="144.5" stroke="var(--rule)" stroke-width="1"/>
<text x="34" y="148.5" text-anchor="end" fill="var(--muted)" font-size="10.5">10%</text>
<line x1="42" y1="80.8" x2="624" y2="80.8" stroke="var(--rule)" stroke-width="1"/>
<text x="34" y="84.8" text-anchor="end" fill="var(--muted)" font-size="10.5">15%</text>
<rect x="44.6" y="234.5" width="27.2" height="37.5" fill="var(--chart-pos)" fill-opacity="0.9"><title>2 of the 68 undefeated teams won 0 per 17</title></rect>
<rect x="76.9" y="253.2" width="27.2" height="18.7" fill="var(--chart-pos)" fill-opacity="0.9"><title>1 of the 68 undefeated teams won 1 per 17</title></rect>
<rect x="109.3" y="253.2" width="27.2" height="18.7" fill="var(--chart-pos)" fill-opacity="0.9"><title>1 of the 68 undefeated teams won 2 per 17</title></rect>
<rect x="141.6" y="215.8" width="27.2" height="56.2" fill="var(--chart-pos)" fill-opacity="0.9"><title>3 of the 68 undefeated teams won 3 per 17</title></rect>
<rect x="173.9" y="140.8" width="27.2" height="131.2" fill="var(--chart-pos)" fill-opacity="0.9"><title>7 of the 68 undefeated teams won 4 per 17</title></rect>
<rect x="206.3" y="159.5" width="27.2" height="112.5" fill="var(--chart-pos)" fill-opacity="0.9"><title>6 of the 68 undefeated teams won 5 per 17</title></rect>
<rect x="238.6" y="215.8" width="27.2" height="56.2" fill="var(--chart-pos)" fill-opacity="0.9"><title>3 of the 68 undefeated teams won 6 per 17</title></rect>
<rect x="270.9" y="159.5" width="27.2" height="112.5" fill="var(--chart-pos)" fill-opacity="0.9"><title>6 of the 68 undefeated teams won 7 per 17</title></rect>
<rect x="303.3" y="122.0" width="27.2" height="150.0" fill="var(--chart-pos)" fill-opacity="0.9"><title>8 of the 68 undefeated teams won 8 per 17</title></rect>
<rect x="335.6" y="215.8" width="27.2" height="56.2" fill="var(--chart-pos)" fill-opacity="0.9"><title>3 of the 68 undefeated teams won 9 per 17</title></rect>
<rect x="367.9" y="84.5" width="27.2" height="187.5" fill="var(--chart-pos)" fill-opacity="0.9"><title>10 of the 68 undefeated teams won 10 per 17</title></rect>
<rect x="400.3" y="178.2" width="27.2" height="93.8" fill="var(--chart-pos)" fill-opacity="0.9"><title>5 of the 68 undefeated teams won 11 per 17</title></rect>
<rect x="432.6" y="178.2" width="27.2" height="93.8" fill="var(--chart-pos)" fill-opacity="0.9"><title>5 of the 68 undefeated teams won 12 per 17</title></rect>
<rect x="464.9" y="234.5" width="27.2" height="37.5" fill="var(--chart-pos)" fill-opacity="0.9"><title>2 of the 68 undefeated teams won 13 per 17</title></rect>
<rect x="497.3" y="197.0" width="27.2" height="75.0" fill="var(--chart-pos)" fill-opacity="0.9"><title>4 of the 68 undefeated teams won 14 per 17</title></rect>
<rect x="529.6" y="234.5" width="27.2" height="37.5" fill="var(--chart-pos)" fill-opacity="0.9"><title>2 of the 68 undefeated teams won 15 per 17</title></rect>
<polyline points="58.2,268.8 90.5,264.0 122.8,241.6 155.2,227.3 187.5,169.7 219.8,171.3 252.2,171.3 284.5,128.2 316.8,128.2 349.2,228.9 381.5,128.2 413.8,142.6 446.2,165.0 478.5,188.9 510.8,204.9 543.2,256.0 575.5,265.6 607.8,270.4" fill="none" stroke="var(--chart-neg)" stroke-width="2.5" stroke-linejoin="round"/>
<circle cx="58.2" cy="268.8" r="3" fill="var(--chart-neg)"><title>2 of all 798 team-seasons won 0 per 17</title></circle>
<circle cx="90.5" cy="264.0" r="3" fill="var(--chart-neg)"><title>5 of all 798 team-seasons won 1 per 17</title></circle>
<circle cx="122.8" cy="241.6" r="3" fill="var(--chart-neg)"><title>19 of all 798 team-seasons won 2 per 17</title></circle>
<circle cx="155.2" cy="227.3" r="3" fill="var(--chart-neg)"><title>28 of all 798 team-seasons won 3 per 17</title></circle>
<circle cx="187.5" cy="169.7" r="3" fill="var(--chart-neg)"><title>64 of all 798 team-seasons won 4 per 17</title></circle>
<circle cx="219.8" cy="171.3" r="3" fill="var(--chart-neg)"><title>63 of all 798 team-seasons won 5 per 17</title></circle>
<circle cx="252.2" cy="171.3" r="3" fill="var(--chart-neg)"><title>63 of all 798 team-seasons won 6 per 17</title></circle>
<circle cx="284.5" cy="128.2" r="3" fill="var(--chart-neg)"><title>90 of all 798 team-seasons won 7 per 17</title></circle>
<circle cx="316.8" cy="128.2" r="3" fill="var(--chart-neg)"><title>90 of all 798 team-seasons won 8 per 17</title></circle>
<circle cx="349.2" cy="228.9" r="3" fill="var(--chart-neg)"><title>27 of all 798 team-seasons won 9 per 17</title></circle>
<circle cx="381.5" cy="128.2" r="3" fill="var(--chart-neg)"><title>90 of all 798 team-seasons won 10 per 17</title></circle>
<circle cx="413.8" cy="142.6" r="3" fill="var(--chart-neg)"><title>81 of all 798 team-seasons won 11 per 17</title></circle>
<circle cx="446.2" cy="165.0" r="3" fill="var(--chart-neg)"><title>67 of all 798 team-seasons won 12 per 17</title></circle>
<circle cx="478.5" cy="188.9" r="3" fill="var(--chart-neg)"><title>52 of all 798 team-seasons won 13 per 17</title></circle>
<circle cx="510.8" cy="204.9" r="3" fill="var(--chart-neg)"><title>42 of all 798 team-seasons won 14 per 17</title></circle>
<circle cx="543.2" cy="256.0" r="3" fill="var(--chart-neg)"><title>10 of all 798 team-seasons won 15 per 17</title></circle>
<circle cx="575.5" cy="265.6" r="3" fill="var(--chart-neg)"><title>4 of all 798 team-seasons won 16 per 17</title></circle>
<circle cx="607.8" cy="270.4" r="3" fill="var(--chart-neg)"><title>1 of all 798 team-seasons won 17 per 17</title></circle>
<line x1="42" y1="272.0" x2="624" y2="272.0" stroke="var(--rule)" stroke-width="1.5"/>
<text x="58.2" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">0</text>
<text x="90.5" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">1</text>
<text x="122.8" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">2</text>
<text x="155.2" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">3</text>
<text x="187.5" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">4</text>
<text x="219.8" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">5</text>
<text x="252.2" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">6</text>
<text x="284.5" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">7</text>
<text x="316.8" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">8</text>
<text x="349.2" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">9</text>
<text x="381.5" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">10</text>
<text x="413.8" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">11</text>
<text x="446.2" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">12</text>
<text x="478.5" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">13</text>
<text x="510.8" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">14</text>
<text x="543.2" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">15</text>
<text x="575.5" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">16</text>
<text x="607.8" y="289.0" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">17</text>
<text x="333.0" y="308" text-anchor="middle" fill="var(--muted)" font-size="11.5">Regular season wins, per 17 games</text>
<text x="624.0" y="326" text-anchor="end" fill="var(--muted)" font-size="10.5">9 or more wins: 45.6% of the undefeated group, 46.9% of everybody</text>
</svg>
```

Every team since 2000 that won all of its preseason games. 68 of them out of 798
team-seasons. Bars are that group, the line is everybody, both as a share of
their own group so the 68 and the 798 are comparable.

They finish everywhere. Raw win totals run from 0 to 14. The biggest single
bucket is 10 wins with 10 teams in it, and the next 3 buckets down hold 8, 6 and
6. There is no cluster.

45.6% of the undefeated group won 9 or more per 17. For everybody it's 46.9%.

That gap is the whole answer, and the reason the histogram was worth drawing
rather than quoting an average. A tight pile around 8 wins would have meant an
undefeated August genuinely makes you mediocre, which is a real claim. A smear
across the entire range means August told you nothing about that specific team,
which is a different claim, and it's the one the data supports.

Both ends of the range belong to somebody. Detroit 2008 and Cleveland 2017 went
0-16 out of perfect Augusts. New England 2003 and Baltimore 2019 went 14-2, and
Minnesota 2024 went 14-3.

The caveat travels with the chart: 68 teams across 16 occupied buckets is
somewhere between 1 and 10 teams per bar. Read the shape, don't read a bump.

Sources: ESPN's public schedule endpoint, cached in
`scripts/preseason_cache_2000.json`, which is the same file behind the 798
team-season sample, so Detroit's rows here match the rows already published.
2020 excluded, no preseason was played. Ties count as half a win. Win rate on
both axes of the scatter because preseasons are 3, 4 or 5 games and seasons are
16 or 17. Charts from one run each of `scripts/lions_scatter_svg.py` and
`scripts/undefeated_preseason_hist.py --svg`.

*Not betting advice. Just calls, made in public and kept in public.*
