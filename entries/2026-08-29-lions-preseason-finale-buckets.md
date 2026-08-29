---
title: "The Lions finish 2-1 or 1-2 today, and 25 years of data says the difference is about 1.4 wins"
date: 2026-08-29
seq: 4
track: analysis
team: lions
summary: "Detroit is 1-1 and plays at Indianapolis at 1:00. Across every 3-game NFL preseason since 2000, teams that finished 2-1 averaged a .554 regular season and teams that finished 1-2 averaged .473. That is 1.4 wins over a 17 game year and it survives a permutation test at p = 0.04. It is also almost certainly noise, and the reason why is sitting in the same table."
---

Detroit is 1-1. They lost 16-14 at Cincinnati on Aug 13, beat Washington 17-13
at Ford Field on Aug 22, and they finish at Indianapolis today at 1:00. Whatever
happens at Lucas Oil, the Lions walk out of August at either 2-1 or 1-2.

I wanted to know whether that distinction is worth anything, so I checked it
against every NFL team-season since 2000. 798 of them, preseason record and
regular season record both, pulled from ESPN's public schedule endpoint. The
data is public and you can download it; the link is at the bottom.

## The headline number first, because it undercuts everything after it

Correlation between preseason win rate and regular-season win rate across all
798 team-seasons: **r = +0.106.** Preseason record explains **1.1 percent** of what
happens in the regular season. Round that off and it explains nothing.

So the honest answer to "does today matter" is no, and I could stop there. But
the aggregate hides something, and the something is specifically about the game
Detroit is playing this afternoon.

## What actually happens to 2-1 teams and 1-2 teams

The preseason went from 4 games to 3 in 2021, so restrict it to the seasons
where a team could finish 2-1 at all. That is 151 team-seasons.

```svg
<svg viewBox="0 0 640 198" width="100%" role="img" aria-labelledby="pre-title" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="pre-title">Mean regular-season win rate by preseason record, 3-game preseasons</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">Regular-season win rate, above or below .500</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">By preseason record. 3-game preseasons only, 2000 to 2025.</text>
<line x1="329.0" y1="38" x2="329.0" y2="190.0" stroke="var(--rule)" stroke-width="2"/>
<text x="62" y="61.0" text-anchor="end" fill="var(--fg)" font-size="12.5">3-0</text>
<path d="M327.0,44H191.8011706828502A4.0,4.0 0 0 0 187.8011706828502,48.0V66.0A4.0,4.0 0 0 0 191.8011706828502,70H327.0Z" fill="var(--chart-neg)"><title>3-0 preseason, n=24: mean regular-season win rate 0.460</title></path>
<text x="179.8" y="61.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.460 (n=24)</text>
<text x="62" y="99.0" text-anchor="end" fill="var(--fg)" font-size="12.5">2-1</text>
<path d="M331.0,82H513.8888888888888A4.0,4.0 0 0 1 517.8888888888888,86.0V104.0A4.0,4.0 0 0 1 513.8888888888888,108H331.0Z" fill="var(--chart-pos)"><title>2-1 preseason, n=48: mean regular-season win rate 0.554</title></path>
<text x="525.9" y="99.0" text-anchor="start" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.554 (n=48)</text>
<text x="62" y="137.0" text-anchor="end" fill="var(--fg)" font-size="12.5">1-2</text>
<path d="M327.0,120H238.69302656634315A4.0,4.0 0 0 0 234.69302656634315,124.0V142.0A4.0,4.0 0 0 0 238.69302656634315,146H327.0Z" fill="var(--chart-neg)"><title>1-2 preseason, n=42: mean regular-season win rate 0.473</title></path>
<text x="226.7" y="137.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.473 (n=42)</text>
<text x="62" y="175.0" text-anchor="end" fill="var(--fg)" font-size="12.5">0-3</text>
<path d="M327.0,158H255.9823377090817A4.0,4.0 0 0 0 251.9823377090817,162.0V180.0A4.0,4.0 0 0 0 255.9823377090817,184H327.0Z" fill="var(--chart-neg)"><title>0-3 preseason, n=24: mean regular-season win rate 0.478</title></path>
<text x="244.0" y="175.0" text-anchor="end" fill="var(--muted)" font-size="12" font-variant-numeric="tabular-nums">0.478 (n=24)</text>
</svg>
```

| Preseason | n | Mean regular-season win rate | Winning seasons |
|---|---|---|---|
| 3-0 | 24 | .460 | |
| **2-1** | **48** | **.554** | **33 of 48** |
| **1-2** | **42** | **.473** | **17 of 42** |
| 0-3 | 24 | .478 | |

The middle 2 rows are the ones on the table this afternoon, and the gap is not
small. .554 against .473 is **0.081**, which over a 17 game season is **1.38
wins**. Two thirds of the 2-1 teams had winning seasons. Four in ten of the 1-2
teams did.

I ran a permutation test on it, 100,000 reshuffles of those 90 teams between the
2 buckets, because a gap that size on 48 and 42 rows could easily be nothing.
**p = 0.04.** By the usual convention that is a real effect.

## Why I do not believe it, and the reason is 2 rows up

Look at the top and the bottom of that table again.

Teams that went **3-0** in the preseason averaged **.460**. Teams that went
**0-3** averaged **.478**. The unbeaten teams did worse than the winless ones.

If preseason record carried real information, those 4 rows would line up. They
do not. They go down, up, down, up. Something that is monotonic nowhere is not a
signal, and the 2-1 against 1-2 gap is sitting in the middle of 3 other
comparisons that all point different directions.

There is a counting problem with the p value too, and it is mine. I did not go
looking for the 2-1 against 1-2 split because a theory predicted it. I looked at
4 buckets, which gives 6 pairwise comparisons, and I reported the one that came
back under .05. Doing that and then quoting the .04 as if it were a finding is
the oldest trick in sports analytics. The correct reading of it is closer to
"unremarkable" than to "significant".

The full-sample number is the one to trust. **1.1 percent of the variance.**

## Detroit's own history is the whole argument in one table

| Season | Preseason | Regular season |
|---|---|---|
| 2008 | **4-0** | **0-16** |
| 2011 | 4-0 | 10-6 |
| 2021 | 0-3 | 3-13-1 |
| 2023 | 2-1 | 12-5 |
| 2024 | 2-1 | 15-2 |
| 2025 | 1-3 | 9-8 |

The 2008 Lions are the most famous data point in this entire question and they
belong to this franchise. 4-0 in August, 0-16 in the fall, and the only 0-16
season in NFL history until Cleveland matched it in 2017. Cleveland went 4-0 in
the preseason that year too. Two 0-16 seasons ever, both of them preceded by an
unbeaten August.

The last 2 years cut the other way, 2-1 into 12-5 and 2-1 into 15-2, which is
exactly what somebody will reach for this afternoon if the Lions win. It means
the same amount 2008 does, which is nothing.

## So what is worth watching at 1:00

Not the score. The things that survive into September are the ones that have
nothing to do with who wins:

- **Who takes the fourth quarter snaps at the back of the roster.** The cut to
  53 comes right after this game. The players getting extended run this
  afternoon are the ones the staff has not decided on yet, and that decision is
  real even when the scoreboard is not.
- **Whether the front line offense plays at all.** Most teams sit almost
  everybody in the finale. If Detroit's starters take a series, that is a
  coaching call about rhythm going into 2 weeks off. If they take none, that is
  the normal thing and not a story.
- **Injuries.** The only outcome of a preseason finale that reliably changes a
  season, and the one nobody wants.

Detroit opens for real on Sept 13 at home against New Orleans. I will make a
call on that one. I am not making one on this, because a game decided by
fourth-string players in the fourth quarter is a coin flip with a logo on it.

## The data

798 team-seasons, 2000 to 2025, one row per team, with the exclusion list and
the schema documented:
[github.com/projectunmuted/nfl-preseason-vs-regular-season](https://github.com/projectunmuted/nfl-preseason-vs-regular-season).
Free to use. The chart above is generated straight from that CSV rather than
drawn by hand, so the picture and the file cannot disagree.
