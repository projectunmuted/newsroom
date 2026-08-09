---
title: "The Tigers are 0-6 against Cleveland with the worst offensive matchup in baseball. I went looking for the reason and found out there probably isn't one"
date: 2026-08-09
track: analysis
team: tigers
cycle: "Analysis"
summary: "Detroit has scored 11 runs in six games against the Guardians, 1.83 a game against a season average of 4.58. Out of 294 team-opponent pairs in baseball, that is the single worst. Then I shuffled who played whom two thousand times, and pure chance produced a worst matchup more extreme than Detroit's in 74 percent of the shuffles. The tell is that the same Tigers own the other tail too."
---

Cleveland comes to Comerica on Tuesday and the Tigers have not beaten them all
year. Not once. Six games, six losses, and the losses were not the fun kind
where you get blown out and forget about it by Thursday. Four of the six were
decided by one or two runs.

This is the one thing about Detroit's season that the regression argument does
not touch. I wrote last week that Detroit's close-game record is about 61
percent as meaningful as it looks, which covers a lot of ground, and a reader
correctly pointed out that it does not cover this. You can tell me that 26-44
in close games will regress. Fine. Tell me about 0-6 against the one team
sitting directly between Detroit and a wild card, with seven more games left
against them.

So I went and looked at all six games, and then at every other team-opponent
matchup in baseball, and the answer is genuinely not what I expected when I
started.

## First, how bad it actually is

| Date | Game | Result | Margin | Tigers hits | Tigers K | Cleveland starter |
|---|---|---|---|---|---|---|
| May 18 | `824277` | Cleveland 8, Detroit 2 | 6 | 5 | 5 | Slade Cecconi |
| May 19 | `824276` | Cleveland 4, Detroit 3 | 1 | 7 | 13 | Parker Messick |
| May 20 | `824273` | Cleveland 3, Detroit 2 (10) | 1 | 5 | 9 | Tanner Bibee |
| May 21 | `824274` | Cleveland 3, Detroit 1 | 2 | 6 | 13 | Joey Cantillo |
| June 12 | `824425` | Cleveland 3, Detroit 2 | 1 | 2 | 9 | Tanner Bibee |
| June 13 | `824426` | Cleveland 3, Detroit 1 | 2 | 9 | 10 | Joey Cantillo |

*Every completed Detroit-Cleveland game in 2026, matched by the league's own
game id. The June 14 game was postponed and is on the September 4
schedule as a makeup, which is why it is not a seventh loss here.*

Eleven runs in six games. That is 1.83 a game from a team that scores 4.58 for
the season. Detroit struck out in 30.6 percent of its at-bats in these six
games against a season rate of 25.6 percent, and left 92 men on base.

Cleveland scored 24, and 8 of those came in the first game. Take out the
opener and it is Cleveland 16, Detroit 9 across five games. Nobody was hitting.
Detroit was hitting less.

## It is not the bullpen, and I want to be clear about that because it is the easy answer

The Tigers' bullpen is the story of this season. Twenty-two saves and 25 blown
ones. It is the reason the record does not match the run differential, and if
you had asked me to guess why Detroit is 0-6 against Cleveland before I pulled
the game logs, that is what I would have guessed.

It is wrong.

| Staff | Innings | Earned runs | ERA |
|---|---|---|---|
| Cleveland starters | 38.0 | 8 | 1.89 |
| **Cleveland bullpen** | **17.0** | **1** | **0.53** |
| Detroit starters | 29.0 | 13 | 4.03 |
| Detroit bullpen | 24.0 | 9 | 3.38 |

Detroit's relievers threw 24 innings in this series with a 3.38 ERA, and four
of those nine earned runs came in one third of an inning from Brant Hurter in
the May 18 blowout. Take that one appearance out and the bullpen ran a 2.25
across the rest of it. That is not a unit that lost six games.

Here is the number that settles it: **in these six games, Detroit led at the
end of an inning from the sixth onward exactly once.** You cannot blow a lead
you never had. The bullpen was not handing these back. The offense never gave
them anything to hand back.

What did happen is that Cleveland's relievers threw 17 innings and gave up one
earned run. Cade Smith appeared in four of the six. Tanner Bibee started two of
them and went 15 innings with three earned runs, and he is the probable starter
on Tuesday.

## So is this a real thing about the matchup?

Here is where I expected to write a paragraph about how Detroit's lineup has
some specific problem with Cleveland's staff, and instead I have to write this.

Minus 2.75 runs per game is a huge number. Out of every team-opponent pair in
baseball with at least six games played, 294 of them, **Detroit against
Cleveland is the single worst offensive matchup in the sport.** Rank one of
294.

The problem with that sentence is that somebody has to be rank one of 294. The
real question is not whether minus 2.75 is a big number. It is whether minus
2.75 is bigger than the worst number 294 coin flips produce.

So I tested it. Hold every team's actual game-by-game runs scored exactly as
they happened, then shuffle which of those games belong to which opponent,
keeping the number of games in each matchup the same. Recompute all 294 splits.
Write down the worst one. Do that two thousand times, and you have a picture of
what the most extreme matchup in baseball looks like when opponent identity
means literally nothing.

```svg
<svg viewBox="0 0 640 310" width="100%" role="img" aria-labelledby="split-title" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="split-title">Distribution of offensive performance by opponent across all team-opponent pairs in MLB, 2026</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">How much every team's offense changes by opponent</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">Each bar counts team-opponent pairs. Horizontal axis is runs per game in that matchup</text>
<text x="0" y="48" fill="var(--muted)" font-size="11">minus that team's runs per game for the season. Pairs of six games or more.</text>
<rect x="40.8" y="238.4" width="37.1" height="13.6" fill="var(--chart-neg)" opacity="0.55" rx="1.5"><title>4 pairs between -3.0 and -2.5</title></rect>
<rect x="79.5" y="214.7" width="37.1" height="37.3" fill="var(--chart-neg)" opacity="0.55" rx="1.5"><title>11 pairs between -2.5 and -2.0</title></rect>
<rect x="118.1" y="197.7" width="37.1" height="54.3" fill="var(--chart-neg)" opacity="0.55" rx="1.5"><title>16 pairs between -2.0 and -1.5</title></rect>
<rect x="156.8" y="143.4" width="37.1" height="108.6" fill="var(--chart-neg)" opacity="0.55" rx="1.5"><title>32 pairs between -1.5 and -1.0</title></rect>
<rect x="195.5" y="62.0" width="37.1" height="190.0" fill="var(--chart-neg)" opacity="0.55" rx="1.5"><title>56 pairs between -1.0 and -0.5</title></rect>
<rect x="234.1" y="116.3" width="37.1" height="135.7" fill="var(--chart-neg)" opacity="0.55" rx="1.5"><title>40 pairs between -0.5 and +0.0</title></rect>
<rect x="272.8" y="102.7" width="37.1" height="149.3" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>44 pairs between +0.0 and +0.5</title></rect>
<rect x="311.5" y="133.2" width="37.1" height="118.8" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>35 pairs between +0.5 and +1.0</title></rect>
<rect x="350.1" y="197.7" width="37.1" height="54.3" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>16 pairs between +1.0 and +1.5</title></rect>
<rect x="388.8" y="177.4" width="37.1" height="74.6" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>22 pairs between +1.5 and +2.0</title></rect>
<rect x="427.5" y="228.2" width="37.1" height="23.8" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>7 pairs between +2.0 and +2.5</title></rect>
<rect x="466.1" y="231.6" width="37.1" height="20.4" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>6 pairs between +2.5 and +3.0</title></rect>
<rect x="504.8" y="241.8" width="37.1" height="10.2" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>3 pairs between +3.0 and +3.5</title></rect>
<rect x="543.5" y="248.6" width="37.1" height="3.4" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>1 pairs between +3.5 and +4.0</title></rect>
<rect x="582.1" y="248.6" width="37.1" height="3.4" fill="var(--chart-pos)" opacity="0.55" rx="1.5"><title>1 pairs between +4.0 and +4.5</title></rect>
<line x1="40" y1="252" x2="620" y2="252" stroke="var(--rule)" stroke-width="1"/>
<line x1="272.0" y1="58" x2="272.0" y2="252" stroke="var(--rule)" stroke-width="2" stroke-dasharray="3 3"/>
<text x="40.0" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">-3</text>
<text x="117.3" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">-2</text>
<text x="194.7" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">-1</text>
<text x="272.0" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">+0</text>
<text x="349.3" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">+1</text>
<text x="426.7" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">+2</text>
<text x="504.0" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">+3</text>
<text x="581.3" y="268" text-anchor="middle" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">+4</text>
<line x1="59.5" y1="60" x2="59.5" y2="252" stroke="var(--chart-neg)" stroke-width="2"/>
<text x="65.5" y="286" text-anchor="start" fill="var(--fg)" font-size="11" font-weight="600">Tigers vs Cleveland</text>
<text x="65.5" y="300" text-anchor="start" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">-2.75 runs/game</text>
<line x1="536.4" y1="60" x2="536.4" y2="252" stroke="var(--chart-pos)" stroke-width="2"/>
<text x="530.4" y="286" text-anchor="end" fill="var(--fg)" font-size="11" font-weight="600">Tigers vs Athletics</text>
<text x="530.4" y="300" text-anchor="end" fill="var(--muted)" font-size="10.5" font-variant-numeric="tabular-nums">+3.42 runs/game</text>
</svg>
```

| Runs/game vs season average | Team-opponent pairs |
|---|---|
| -3.0 to -2.5 | 4 |
| -2.5 to -2.0 | 11 |
| -2.0 to -1.5 | 16 |
| -1.5 to -1.0 | 32 |
| -1.0 to -0.5 | 56 |
| -0.5 to 0.0 | 40 |
| 0.0 to +0.5 | 44 |
| +0.5 to +1.0 | 35 |
| +1.0 to +1.5 | 16 |
| +1.5 to +2.0 | 22 |
| +2.0 to +2.5 | 7 |
| +2.5 to +3.0 | 6 |
| +3.0 to +3.5 | 3 |
| +3.5 to +4.0 | 1 |
| +4.0 to +4.5 | 1 |

*All 294 team-opponent pairs with six or more completed games, 2026 regular
season. Detroit-Cleveland is in the leftmost bin. Detroit-Athletics is in the
rightmost.*

The result:

- Detroit-Cleveland, observed: **minus 2.75** runs per game.
- The worst pair in a shuffled season, median outcome: **minus 2.94**.
- Shuffles that produced a worst matchup at least as extreme as Detroit's:
  **1,473 of 2,000, or 73.7 percent.**

The most alarming number in the Tigers' season is *milder* than what pure
randomness typically hands you. In a league where nobody has any matchup
problems with anybody, the worst-looking pair is usually worse than this one.

## The part that convinced me

I could have stopped there and some of you would reasonably say the simulation
is a trick. Here is the thing that is not a trick.

Detroit is rank 1 of 294 in the worst direction. Detroit is also **rank 292 of
294 in the best direction**, scoring 8.00 runs a game against the Athletics,
plus 3.42 over their season rate, in a 6-0 sweep. And while doing it, Detroit
held those same Athletics to 1.83 runs a game, which is the *fifth* most
extreme offensive suppression in baseball.

Same team. Same season. Both tails of the distribution, plus a third entry near
the end. If Detroit having the worst offensive matchup in baseball proves
something is broken about how they match up with Cleveland, then Detroit having
nearly the best proves they have solved the Athletics forever, and Tigers fans
who watched this team for four months know exactly how much that is worth.

Two more things in the same direction. Seven team-opponent pairs in baseball
are winless at six or more games, including the Mets at 0-7 against the Cubs
and the Padres at 0-6 against Philadelphia. If you work out how many sweeps you
would expect from team strength alone, using each club's season win rate, the
answer is 5.0. Seven observed against five expected is not a phenomenon. And
Cleveland is not some offense-eating machine: the second-worst matchup in
baseball is **Cleveland** scoring 1.33 a game against Tampa Bay.

## What I would still watch on Tuesday

None of the above means 0-6 was fake. Those are six real losses in the
standings and Detroit is 57-60, two games back of a wild card, with Cleveland
at 58-60 sitting a half game in front of them. The games happened. The argument
is only about what they predict.

The one thing that survives every test above is that **Tanner Bibee has thrown
15 innings against Detroit this year and given up three earned runs**, and he
takes the ball Tuesday at 6:40. That is not a statistical artifact of a small
sample the way the team-level split is, it is one pitcher who has had a
specific plan and executed it twice. It is also, and I have to say this because
it is the same trap, fifteen innings. Two starts. If I told you a pitcher was
now permanently good against a lineup on the strength of two starts I would be
doing exactly the thing this piece just spent a thousand words arguing against.

So: I am not scared of the 0-6. I am mildly scared of Bibee, and mostly I want
to see whether a Detroit lineup that struck out in 30.6 percent of its at-bats
against this staff can hand its bullpen a lead late. Across six games it has
done that once.

The pick for Tuesday's game goes up before first pitch, as always, on the
record page. This piece is not it. This piece is me finding out that the
scariest thing on Detroit's schedule is a coin that came up tails six times.

---

*Method and sources: all game data from the MLB Stats API, regular season only,
matched by gamePk and filtered on `abstractGameState` rather than the detailed
status string, which reports real completed games as "Game Over" and
"Completed Early." Series detail from `scripts/det_cle_series.py`, the
distribution and permutation test from `scripts/opponent_splits.py`, the chart
from `scripts/opponent_split_chart.py`, all in the repository. The permutation
test uses a fixed seed so anyone can reproduce the 73.7 percent exactly.*

*Not betting advice. Just calls, made in public and kept in public.*
