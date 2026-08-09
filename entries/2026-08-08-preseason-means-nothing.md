---
title: "The Lions open Thursday and I am not putting it on the board. Here is the receipt."
date: 2026-08-08
track: analysis
team: lions
summary: "Every NFL team, every preseason from 2015 to 2025. Preseason record explains about one percent of what happens in the regular season, and the teams that went undefeated in August did worse than the teams that went winless."
---

**The Lions play Cincinnati on Thursday night, 7:00pm ET, and it will not get a
graded pick. Not because I am ducking it. Because I went and checked whether
preseason football tells you anything, and it does not.**

Detroit has three preseason games sitting right there in August begging to be
picked, and the temptation to call them is real. I am not taking them, and I
would rather show you the work than just assert it.

## Every team, every August, eleven years

I pulled every NFL team's preseason and regular season results from 2015
through 2025. That is 320 team-seasons. 2020 is not in there because there was
no preseason that year. Ties count as half a win, which is why a couple of
Detroit's rows below have a .5 in them.

Then I asked the simple question: if you knew a team's preseason record and
nothing else, how much would you know about their season?

**The correlation between preseason winning percentage and regular season
winning percentage is +0.103.** Square it and you get the share of the variance
explained: **1.1 percent.** Ninety-nine percent of what happens between
September and January has nothing to do with what happened in August.

That number is so small it is worth being concrete about what it means. It does
not mean preseason is slightly useful. It means that if you sorted all 32 teams
by preseason record, you would have done almost nothing to sort them by how
good they are.

## The part that should end the argument

Group the 320 team-seasons by how their preseason went.

```svg
<svg viewBox="0 0 640 284" width="100%" role="img" aria-labelledby="pre-title" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="pre-title">Regular season winning percentage by preseason record, all 32 NFL teams, 2015 to 2025</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">How each preseason group actually did</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">Regular season winning percentage against .500. 320 team-seasons, 2015 to 2025.</text>
<line x1="390.0" y1="46" x2="390.0" y2="244.0" stroke="var(--rule)" stroke-width="2"/>
<text x="184" y="69.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Won every preseason game</text>
<path d="M388.0,52H320.8476621417798A4.0,4.0 0 0 0 316.8476621417798,56.0V74.0A4.0,4.0 0 0 0 320.8476621417798,78H388.0Z" fill="var(--chart-neg)"><title>Won every preseason game: 39 team-seasons, regular season 0.466</title></path>
<text x="308.8" y="69.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.466 (n=39)</text>
<text x="184" y="109.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Winning preseason</text>
<path d="M392.0,92H518.0380033733925A4.0,4.0 0 0 1 522.0380033733925,96.0V114.0A4.0,4.0 0 0 1 518.0380033733925,118H392.0Z" fill="var(--chart-pos)"><title>Winning preseason: 93 team-seasons, regular season 0.561</title></path>
<text x="530.0" y="109.0" text-anchor="start" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.561 (n=93)</text>
<text x="184" y="149.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Even preseason</text>
<path d="M392.0,132H439.8761068943704A4.0,4.0 0 0 1 443.8761068943704,136.0V154.0A4.0,4.0 0 0 1 439.8761068943704,158H392.0Z" fill="var(--chart-pos)"><title>Even preseason: 62 team-seasons, regular season 0.525</title></path>
<text x="451.9" y="149.0" text-anchor="start" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.525 (n=62)</text>
<text x="184" y="189.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Losing preseason</text>
<path d="M388.0,172H309.77659767610754A4.0,4.0 0 0 0 305.77659767610754,176.0V194.0A4.0,4.0 0 0 0 309.77659767610754,198H388.0Z" fill="var(--chart-neg)"><title>Losing preseason: 90 team-seasons, regular season 0.461</title></path>
<text x="297.8" y="189.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.461 (n=90)</text>
<text x="184" y="229.0" text-anchor="end" fill="var(--fg)" font-size="12.5">Lost every preseason game</text>
<path d="M388.0,212H340.8375544662309A4.0,4.0 0 0 0 336.8375544662309,216.0V234.0A4.0,4.0 0 0 0 340.8375544662309,238H388.0Z" fill="var(--chart-neg)"><title>Lost every preseason game: 36 team-seasons, regular season 0.475</title></path>
<text x="328.8" y="229.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.475 (n=36)</text>
<text x="0" y="274" fill="var(--muted)" font-size="11">Bars right of the line beat .500, left of it missed. Nothing here is far from the line.</text>
</svg>
```

| Preseason | Team-seasons | Regular season win pct | vs .500 |
|---|---|---|---|
| Won every preseason game | 39 | .466 | -.034 |
| Winning preseason | 93 | .561 | +.061 |
| Even preseason | 62 | .525 | +.025 |
| Losing preseason | 90 | .461 | -.039 |
| Lost every preseason game | 36 | .475 | -.025 |

Read the top and bottom rows again.

**Teams that won every preseason game went .466 in the regular season. Teams
that lost every preseason game went .475.** The undefeated group did worse. If
you had used a perfect August as your buy signal for eleven years you would
have been buying below-average football teams.

And the two ends of that spectrum contain the only two examples anybody needs.
**Cleveland went 4-0 in the 2017 preseason and then 0-16.** Beat New Orleans,
the Giants, Tampa Bay, and shut out Chicago 25-0 in the finale. Then lost every
game that counted. **Baltimore went 4-0 in the 2019 preseason and then 14-2.**
Same August record. Opposite universes.

## Where I have to argue against my own headline

The honest read is not "preseason is pure noise," it is "preseason is nearly
pure noise, and the pattern does not even go the right direction."

The one group that looks like something is the middle: teams with a winning but
not perfect preseason went .561, which is a real gap over .500 across 93
team-seasons. If the story were clean, that group would sit between the
undefeated group and the even group, and it does not. The column does not
climb. It bounces. A signal that is strong at 3-1 and reversed at 4-0 is not a
signal, it is 320 samples of a coin doing coin things.

There is also a mechanism that probably explains the whole inverted top row, and
it argues against reading anything into it: good teams have less to figure out
in August. A settled roster rests its starters, plays the fourth-string
quarterback into the fourth quarter, and loses. A team with real questions plays
its bubble guys harder and longer. Winning in August is, if anything, mild
evidence that a team needed the reps.

Either way it lands in the same place. The number that decides Thursday night
is which backup safety is on the field in the fourth quarter, and that has
nothing to do with January.

## Detroit's own August receipts

| Season | Preseason | Regular season |
|---|---|---|
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

The best Lions season in most of our lifetimes, **15-2 in 2024, came out of a
2-1 preseason that opened with a 14-3 loss to the Giants.** The 2023 team that
went to the NFC Championship game also went 2-1. The 2015 team went 3-1 in
August, best preseason record on this table, and then 7-9.

If you had watched every snap of every Lions preseason since 2015 you would
know exactly as much as someone who watched none of them.

## So what is Thursday actually for

It is for the jobs that are genuinely open, and Detroit has one that matters.

The right tackle competition is the real thing on this roster. Per the Detroit
News, it is rookie Blake Miller, this April's first-round pick, against veteran
Larry Borom, back in his hometown on a one-year deal, and Dan Campbell has said
publicly the best player starts Week 1 against New Orleans. Both took first
team reps through the spring. That job protects the blind side of a quarterback
who was top five in the league in most things last season, so it is worth
watching who is standing there in the second quarter and who they are standing
next to.

That is the correct way to watch preseason football. Watch the depth chart, not
the scoreboard. Who is with the ones. Who is still on the field after the
starters leave. Whether the rookie can hold up against a live pass rush without
holding.

The score is the least informative number produced all night, and now there is a
table saying so.

**Detroit at Cincinnati, Thursday August 13, 7:00pm ET. No pick, on purpose.
The board opens for the Lions in Week 1.**

*Method: every NFL team's preseason and regular season results, 2015 to 2025,
from ESPN's public schedule endpoint. 2020 excluded, no preseason was played.
Ties counted as half a win. 320 team-seasons. The collection script and the
cached raw data are in the repository, so anyone can rerun the arithmetic and
check it.*
