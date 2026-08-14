---
title: "You were right about 2008. Here is what happens when you put it back in."
date: 2026-08-14
track: analysis
team: lions
seq: 2
summary: "The preseason backtest ran 2015 to 2025 and left out the 2008 Lions. The data goes back to 2000, so here is all of it: 798 team-seasons. The 2008 Lions are the worst season in it, the answer barely moves, and the one fun line from the first version does not survive."
---

**The 2008 Lions went 4-0 in the preseason and 0-16 in the regular season, and
they were not in the sample. Several of you said so, correctly and repeatedly.
So I went and got every season the data goes back to, which is 2000, not 2015.
798 team-seasons instead of 320.**

Here is what that does.

## First, the part that was just wrong

The original run said the window came from the endpoint's coverage. It doesn't.
ESPN serves NFL preseason schedules back to **2000**. 1999 and earlier return
regular season games and no preseason at all, so 2000 is the real floor, and
everything from 2000 to 2014 was sitting there the whole time. That's 15 extra
seasons and 478 extra team-seasons, and it's where 2008 lives.

## The 2008 Lions are the worst season in 25 years of this

Sorted by regular season winning percentage, across all 798 team-seasons:

| Team | Season | Preseason | Regular season |
|---|---|---|---|
| **Detroit** | **2008** | **4-0** | **0-16** |
| Cleveland | 2017 | 4-0 | 0-16 |
| San Diego | 2000 | 4-0 | 1-15 |
| Carolina | 2001 | 2-2 | 1-15 |
| Miami | 2007 | 2-2 | 1-15 |
| St. Louis | 2009 | 3-1 | 1-15 |
| Cleveland | 2016 | 0-4 | 1-15 |

**The 3 worst regular seasons in the sample all came out of a perfect
preseason.** Both 0-16 seasons in NFL history, and the 1-15 Chargers. That's not
a small thing to have left out, and it's the version of this the sub has been
telling each other for 18 years.

Add the near misses and it gets worse. **St. Louis went 4-0 in the 2011
preseason and 2-14.** Washington went 4-0 in 2013 and 3-13. Arizona 2003, Philadelphia
2012 and the Giants in 2019 all went 4-0 in August and 4-12 after it.

## And then the other Lions team

**2011. Also 4-0 in the preseason. 10-6, and the playoffs.**

Same franchise, same perfect August, 3 seasons apart, and the two outcomes are
the worst season anybody has ever had and the first Lions playoff berth in 12
years. If you want to know why the correlation is what it is, that's the whole
argument inside one team.

Detroit's 25 seasons, since you asked for them:

| Season | Preseason | Regular season |
|---|---|---|
| 2000 | 2-2 | 9-7 |
| 2001 | 1-3 | 2-13 |
| 2002 | 1-3 | 3-13 |
| 2003 | 2-2 | 5-11 |
| 2004 | 2-2 | 6-10 |
| 2005 | 1-3 | 5-11 |
| 2006 | 1-3 | 3-13 |
| 2007 | 2-2 | 7-9 |
| **2008** | **4-0** | **0-16** |
| 2009 | 3-1 | 2-14 |
| 2010 | 3-1 | 6-10 |
| **2011** | **4-0** | **10-6** |
| 2012 | 2-2 | 4-12 |
| 2013 | 3-1 | 7-9 |
| 2014 | 3-1 | 11-5 |
| 2015 | 3-1 | 7-9 |
| 2016 | 2-2 | 9-7 |
| 2017 | 2-2 | 9-7 |
| 2018 | 1-3 | 6-10 |
| 2019 | 0-4 | 3-12-1 |
| 2021 | 0-3 | 3-13-1 |
| 2022 | 1-2 | 9-8 |
| 2023 | 2-1 | 12-5 |
| 2024 | 2-1 | 15-2 |
| 2025 | 1-3 | 9-8 |

Detroit's average preseason over those 25 years is **.497** and their average
regular season is **.401**, which is its own joke: this franchise has been almost
exactly a .500 team in August and nowhere near it afterwards.

Detroit on its own correlates at **+.285**, which looks like something and isn't.
That's 25 dots. The 2 seasons that would move it most are 2008 and 2011, and
they point opposite directions.

## The answer, on 798 team-seasons

```svg
<svg viewBox="0 0 640 290" width="100%" role="img" aria-labelledby="pre26-title" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="pre26-title">Regular season winning percentage by preseason record, all NFL teams, 2000 to 2025</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">How each preseason group actually did</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">Regular season winning percentage against .500. 798 team-seasons, 2000 to 2025, 2020 excluded.</text>
<text x="0" y="49" fill="var(--muted)" font-size="11">Every season ESPN carries preseason results for.</text>
<line x1="390.0" y1="52" x2="390.0" y2="250.0" stroke="var(--rule)" stroke-width="2"/>
<text x="184" y="75.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Won every preseason game</text>
<path d="M388.0,58H339.16712322183787A4.0,4.0 0 0 0 335.16712322183787,62.0V80.0A4.0,4.0 0 0 0 339.16712322183787,84H388.0Z" fill="var(--chart-neg)"><title>Won every preseason game: 68 team-seasons, regular season 0.475</title></path>
<text x="327.2" y="75.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.475 (n=68)</text>
<text x="184" y="115.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Winning preseason</text>
<path d="M392.0,98H468.1250079715723A4.0,4.0 0 0 1 472.1250079715723,102.0V120.0A4.0,4.0 0 0 1 468.1250079715723,124H392.0Z" fill="var(--chart-pos)"><title>Winning preseason: 226 team-seasons, regular season 0.538</title></path>
<text x="480.1" y="115.0" text-anchor="start" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.538 (n=226)</text>
<text x="184" y="155.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Even preseason</text>
<path d="M392.0,138H430.81934474920376A4.0,4.0 0 0 1 434.81934474920376,142.0V160.0A4.0,4.0 0 0 1 430.81934474920376,164H392.0Z" fill="var(--chart-pos)"><title>Even preseason: 217 team-seasons, regular season 0.521</title></path>
<text x="442.8" y="155.0" text-anchor="start" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.521 (n=217)</text>
<text x="184" y="195.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Losing preseason</text>
<path d="M388.0,178H302.6527237032116A4.0,4.0 0 0 0 298.6527237032116,182.0V200.0A4.0,4.0 0 0 0 302.6527237032116,204H388.0Z" fill="var(--chart-neg)"><title>Losing preseason: 217 team-seasons, regular season 0.458</title></path>
<text x="290.7" y="195.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.458 (n=217)</text>
<text x="184" y="235.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Lost every preseason game</text>
<path d="M388.0,218H335.53573095905017A4.0,4.0 0 0 0 331.53573095905017,222.0V240.0A4.0,4.0 0 0 0 335.53573095905017,244H388.0Z" fill="var(--chart-neg)"><title>Lost every preseason game: 70 team-seasons, regular season 0.473</title></path>
<text x="323.5" y="235.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.473 (n=70)</text>
<text x="0" y="280" fill="var(--muted)" font-size="11">Bars right of the line beat .500, left of it missed. Nothing here is far from the line.</text>
</svg>
```

| Preseason | Team-seasons | Regular season win pct | vs .500 |
|---|---|---|---|
| Won every preseason game | 68 | .475 | -.025 |
| Winning preseason | 226 | .538 | +.038 |
| Even preseason | 217 | .521 | +.021 |
| Losing preseason | 217 | .458 | -.042 |
| Lost every preseason game | 70 | .473 | -.027 |

Correlation between preseason win rate and regular season win rate:
**+.106**. Variance explained: **1.1 percent**.

On 320 team-seasons it was 1.0 percent. On 798 it's 1.1 percent. Adding 2008,
and 2011, and 476 other team-seasons, moves the answer by a tenth of a
percentage point. **The thing the post said is still the thing the data says.**

## The line that does not survive

Here's what does change, and it's the sentence people quoted.

The first version said teams that went undefeated in August (.466) did *worse*
than teams that went winless (.475). That inversion was fun and it's gone. On
the full sample it's **.475 for the undefeated group against .473 for the
winless group**, which is a 2 point gap across 138 teams and means nothing at
all.

Look at it a different way and the undefeated group stops being the story
entirely. Share of teams that won 9 or more per 17 games:

| Group | Share at 9+ wins |
|---|---|
| Undefeated preseason | .456 |
| Everybody | .469 |
| Winless preseason | .357 |

**An undefeated August tells you nothing. A winless August is mild bad news.**
That's close to the opposite of the punchy version, and it's the one with 798
team-seasons behind it rather than 320.

The other thing worth putting next to the 0-16 table: of the 68 teams that swept
their preseason, the biggest single group won **10** games. 10 teams did that. 4
won 14, and 2 won 15. New England went 4-0 in the 2003 preseason and 14-2.
Baltimore did the same in 2019. The win totals after a perfect August run from 0
to 15 with no cluster anywhere, which is what "no signal" actually looks like
when you stop averaging it.

## Two things in the data that were wrong

Worth saying plainly, because both changed numbers.

**Relocated franchises were being counted as their opponents.** The code found
its team in a box score by matching the abbreviation. ESPN answers a request for
`lar` in any season but writes the abbreviation the franchise used *that year*
inside the game, so a 2015 Rams game says STL, nothing matched, and the old code
fell back to whichever team was listed first. Often the opponent.

That put **8** wrong rows into the published 320, and some of them badly wrong:
San Diego's 2015 season was in there as 10-6 when they went 4-12, and Oakland's
2016 was in there as 8-8 when they went 12-4. The fix is to match on ESPN's
numeric team id, which stays the same through all 3 moves.

**And 0-0 was being read as a tie.** Some fixtures come back with a 0-0 score
rather than a null: games that were genuinely never played, like the Hall of Fame
games cancelled in 2011 and 2016, the Dallas and Houston preseason game called
off for Hurricane Harvey in 2017, and Buffalo at Cincinnati in January 2023.
Also some real games where the score just isn't in the feed, mostly in 2000 and
2001. There are 41 of them. Every one was scoring as half a win to both teams,
and that moved another **10** rows inside the published window.

That's why Detroit 2001 shows 2-13 above rather than 2-14: one Lions game that
season has no score in the feed, so it's out of the sample rather than counted as
a draw. No NFL game has finished 0-0 since 1943, so a 0-0 is a missing result,
not a result.

Neither of those changed the conclusion. Both changed the sample, and the tail
buckets are exactly where 18 misplaced rows do the most damage, which is why
this matters more than the size of the correction suggests.

## So, Thursday

Detroit lost 16-14 at Cincinnati. It counts for nothing, and now it counts for
nothing with 2008 in the room rather than conveniently outside it. Anybody
reaching for that result as a worry has the 2008 table above pointing the other
way, which is the whole problem with reading August.

Watch the roster bubble instead, because that's the only thing in the preseason
with a real consequence attached. The record is noise, and the 2 most famous 4-0
Lions preseasons in living memory are a 0-16 and a playoff team.

The board opens for the Lions in Week 1.

*Method: every NFL team's preseason and regular season results, 2000 to 2025,
from ESPN's public schedule endpoint. 2020 excluded, no preseason was played.
Ties count as half a win. Fixtures with no recorded score are excluded rather
than counted. Teams are matched by ESPN team id, not abbreviation.
`scripts/preseason_full.py` derives every number here in one run.*
