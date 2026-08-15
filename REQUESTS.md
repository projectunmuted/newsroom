# Reader requests

Analyses somebody actually asked for. Newest at top.

Opened 2026-08-10 on his instruction: the AI reads comments and mines them for
requests, and readers may eventually ask for specific analysis directly. **A
request from a real reader outranks any topic picked unprompted**, because it is
the only evidence available that a piece will be read before it is written.

## How a request gets here

1. A comment on one of our posts, or a comment anywhere that amounts to "I wish
   somebody would look at X." Found by reading threads in a live browser session,
   since Reddit's comment feeds are blocked to scripts.
2. Recorded below **verbatim enough to be checkable**, with who asked, where,
   and when. Paraphrase loses the thing that made it worth doing.
3. Turned into a piece, or explicitly declined with a reason. Both outcomes get
   written here. A request quietly dropped is worse than one refused out loud.

## The rule that governs the reply

**Never reply to the commenter.** Not to acknowledge, not to say it is coming,
not when it is published. Replies are the human's alone, his call 2026-08-10. If
answering someone would be valuable, say so to him and let him decide whether to
speak.

---

## A request is not answered until it has a URL

**Added 2026-08-14, and it is the reason this file needed a rule.** Two of the
requests below were marked "Delivered same day" on 08-13. What that meant was: a
script existed, a chart was rendered to `scripts/`, and the answer was typed into
this file. **Nothing was published.** The rules also say I never reply in the
thread, correctly. So from the asker's side it is indistinguishable from being
ignored.

Delivered now means **there is a URL a reader can reach**. Anything short of
that is Worked, not Delivered, and the row says which. See
`entries/2026-08-14-the-answers-nobody-could-read.md`.

---

## Open

### Does Cleveland actually have Detroit's number, or is it 3 bad months?

**Asked 2026-08-10**, 7 upvotes: "Cleveland just knows how to pitch against the
Tigers. For the last 3 seasons. I don't remember many games where the Tigers
scored 4 or more against them." A second commenter pushed the other way: 4 of
the 6 games this year were in May, when the team was different.

Partly answered in the thread already (60 runs in 2024, 34 in 2025, 11 in 2026),
but the real question is whether Detroit's offence declines specifically against
Cleveland or against good pitching generally. That separates "they have our
number" from "good arms beat this lineup", and only one of those is a story.

## Delivered

### Should Detroit run on Cleveland? — answered 2026-08-12

**Asked 2026-08-10** on `1vkuuh2`, by 2 separate commenters, 13 and 5 upvotes.
Verbatim: "Cleveland and Chicago are the worst and 2nd worst teams in baseball
at throwing out runners. Time to let Max show off those wheels." And: "We have
to try and do that small ball BS at some point with Zach, Max or someone else
who is kind of fast (Tork, looking at you)." A 3rd commenter sharpened it: the
organisation seems to avoid stealing on principle, which is defensible with slow
rosters and not with McGonigle and Clark.

Answered inside `entries/2026-08-12-pick-04-should-detroit-run.md`, because it
turned out to be the same question as the pick on `824241`.

**They were right on both premises and the conclusion still flipped.** Cleveland
is 4th worst in baseball at throwing runners out, 16 of 102, 15.7% against a
league 23.1%. Detroit attempts a steal on 4.8% of times reached first, which is
dead last of 30. Both claims check out.

What neither comment knew: that 15.7% is 2 catchers averaged into one number.
Austin Hedges has thrown out **2 runners all season**, 5.1%. Patrick Bailey,
since arriving from San Francisco on May 10, is at **35.3%**, which is about the
best rate in the sport. Bailey has caught 7 of Cleveland's 9 games this month.
The lane the sub is pointing at belongs to the backup.

Two counterweights they did not raise. Detroit is 35 for 53, **66.0%**, against
a league 76.9%, so running more at that conversion gives away outs. And Max
Clark, the name in both comments, has 10 games, 46 plate appearances and **0**
attempts, which is nothing to build a strategy on. McGonigle at 11 for 12 is the
real version of their argument.

### Detroit only, 20 seasons, preseason vs regular season — PUBLISHED 2026-08-15

**Answered at `/journal/2026-08-15-lions-scatter-and-histogram.html`**, as inline
SVG rather than a PNG on a disk, which is the difference between an answer and a
file. Rerun on `preseason_cache_2000.json`, the same receipt behind the 798
team-season sample, so Detroit's rows here match the rows already in print. That
moves 2001 from 2.5-13.5 to 2-13 and extends the reader's 20 seasons to **25**,
2000 through 2025 with 2020 absent.

**The number they asked for, and the reason it needed more than a number.**
Correlation **+0.285**, r squared 8.1%, against +0.20 and 3.9% on the older
19-season version. That is higher than the league-wide +.106, and it is still
nothing: a permutation test shuffling which season follows which August, 20,000
times with a fixed seed, produces a correlation at least that strong in **17.1%**
of shuffles.

**The finding worth the piece is the leave-one-out.** Drop 2008 and r goes to
**+0.514**, r squared 26.4%. Drop 2011 and it falls to +0.222. The season the
thread demanded be included is the single dot doing the most work to prove the
thread's own point, and the other perfect August is the dot pulling hardest the
other way. `scripts/lions_scatter_svg.py` derives all of it in one run.

**Asked 2026-08-13, same thread.** "Is there a way to specifically show Lions
for the last 20 seasons. What was their win percent in the offseason compared to
win percent during the season", then "make it a scatter plot, to see if there's
a trend line at all."

**Delivered same day.** `scripts/lions_preseason_20.py`, its own cache, same
ESPN endpoint and same rules as the league backtest so the overlapping seasons
must agree with the published piece. Two views: paired bars per season
(`last_lions_preseason.png`) and the scatter with a fitted line
(`last_lions_scatter.png`).

**This also pays the 2008 debt from the same thread**, which was the point of
going back 20 years rather than 11. 2006 to 2025, 19 seasons after dropping 2020.

The answer for Detroit specifically:

- Correlation +0.20, r squared 3.9%. The fit rises 15 points of season win rate
  per 100 points of preseason win rate, which across 19 dots is not
  distinguishable from flat.
- **Detroit's best August in 20 years is 2008 at 4-0. They went 0-16.** The
  worst regular season in NFL history followed the best preseason this franchise
  has had this century.
- **The other 4-0 August was 2011, and that team went 10-6 and made the
  playoffs.** Two perfect Augusts, one 0-16 and one a playoff berth. That is the
  entire argument inside one franchise, and it answers both readers at once: the
  one who raised 2008 and the one who raised 2011.
- Mean August .535 against a mean season .428, so if anything Detroit has been
  better in the preseason than in the games that count, which is its own joke.

Worth noting the r squared is 3.9% here against 1.1% league-wide. That is not
Detroit being more predictable, it is 19 data points instead of 320.

### The win distribution for the 39 undefeated-preseason teams — PUBLISHED 2026-08-15

**Answered at `/journal/2026-08-15-lions-scatter-and-histogram.html`**, in the
same entry as the scatter, because they came from the same thread on the same
afternoon. The chart they asked for is now inline SVG on the site instead of
`scripts/last_undefeated_hist.png`.

Rerun on the corrected sample, so the group is **68 teams out of 798**, not 39 of
320. The finding does not move: raw win totals run 0 to 14, the biggest bucket is
10 wins with 10 teams in it, and **45.6%** of the undefeated group won 9 or more
per 17 against **46.9%** of everybody. A smear, not a cluster.

`undefeated_preseason_hist.py` grew a `--svg` mode and a `--cache` switch rather
than being forked, and its "individual bars are 1 to 7 teams" caveat is now
derived from the data instead of written down, because that sentence had already
gone stale once when the sample grew from 39 to 68.

**Asked in the r/detroitlions thread `1vne8nx`, 2026-08-13.** "Out of the 39
teams that won all preseason games, how would they be grouped by total number of
wins? What does that histogram look like?"

**Delivered same day.** `scripts/undefeated_preseason_hist.py`, reading the same
`preseason_cache.json` the backtest uses so it cannot disagree with the
published piece. Chart at `scripts/last_undefeated_hist.png`.

The answer is that the group is not clustered anywhere. Raw win totals run 0 to
14, and per 17 games the distribution tracks the league's shape with a mild lean
low: 46.2% of the undefeated group won 9 or more against 50.6% of everybody.

That distinction is worth the piece it would make. A tight cluster around 8 wins
would have meant an undefeated August genuinely predicts mediocrity, which is a
real finding. A smear across the whole range means August told you nothing about
that specific team, which is the opposite claim and the one the data supports.
The .466 average was hiding a distribution, as averages do.

Caveat that travels with it: 39 teams over 13 occupied buckets is 1 to 7 per
bar. No individual bar means anything.

**Still owed from the same thread:** the 2008 Lions and the pre-2015 window,
above. That one is the bigger debt.

### The 2008 Lions, and everything before 2015 — PUBLISHED 2026-08-14

**Answered at `/journal/2026-08-14-preseason-2008-lions.html`.** They were right,
and the reason the piece gave for the window was wrong: ESPN carries preseason
schedules back to **2000**, not 2015. Rerun on **798 team-seasons** instead of
320.

- **2008 is in there and it is the worst season in the sample.** So is Cleveland
  2017. Both 0-16 seasons in NFL history followed a 4-0 preseason, and so did
  San Diego's 1-15 in 2000. The 3 worst seasons in 25 years, all out of perfect
  Augusts. Their case was stronger than they made it.
- **2011 is in there too**, 4-0 and then 10-6 and the playoffs, which is the
  third commenter's point and it belongs in the same table.
- **The headline survives**: correlation +.106, 1.1% of variance explained,
  against 1.0% on the published window. 478 more team-seasons moved it by a
  tenth of a point.
- **The fun line does not survive.** The post said undefeated-in-August teams
  (.466) did worse than winless ones (.475). On the full sample it is .475
  against .473, which is nothing. That was an artifact of an 11-season window
  and the correction is in the piece.
- **Two data defects found while doing it**, both in print since 08-08.
  Relocated franchises were matched by abbreviation, so ESPN answering `lar`
  with a box score saying `STL` matched nothing and the code used whichever team
  was listed first: **8 wrong rows**, including San Diego 2015 published as 10-6
  when they went 4-12. And never-played fixtures come back **0-0 rather than
  null**, scoring as a tie: 41 games, **10 more wrong rows**. Fixed by matching
  on ESPN's numeric team id and refusing a 0-0.

The 08-08 entry now carries a correction box pointing here, left as published
underneath.

**Original request, as asked:**

**Asked repeatedly, r/detroitlions `1vne8nx`, 2026-08-13, within an hour of the
post going up.** Top comment of the thread at 13 up, and a second commenter
made the same point independently:

> "That was ridiculous that OP made this post and excluded the year we were the
> pre-season champs of the NFL."

> "But do you remember how the 0-16 Lions won all their preseason games?!?!?!
> Has anyone ever mentioned that?!?!?"

**They are right, and this is the strongest objection the piece has taken.** The
2008 Lions went 4-0 in the preseason and 0-16 in the regular season. That is the
single most famous confirming case in football for the exact claim the post
makes, it belongs to this subreddit specifically, and the sample starts in 2015
so it is not in the data. The post argued preseason records mean nothing to an
audience whose own proof of it was excluded by the window.

The window was set by the ESPN endpoint's coverage, which is a reason and not a
justification. Two things to do, in order:

1. **Find out how far back the data actually goes** rather than assuming 2015 is
   the floor. If it reaches 2008 the whole backtest gets rerun and the headline
   number changes slightly; if it does not, say so in the piece rather than
   letting the window look like a choice.
2. **The 2008 row goes in either way**, sourced by hand if necessary. A single
   famous case is not evidence and the piece should say that, but leaving it out
   reads as hiding it, which costs more credibility than the row costs rigour.

A third commenter offered 2011, preseason champs then 10-6 and a playoff berth,
which is the same shape pointing the other way and belongs in the same rerun.

**Also from that thread, a mechanism worth testing rather than a request:**

> "When you're only playing your starters in the preseason game you have a
> problem."

4 upvotes, and it is the reader's version of the theory the post already floats
about good teams resting starters. It is testable: preseason starter snap counts
against regular season record. That is a real piece if the snap data is
reachable.

## Declined

*Nothing yet. When something lands here it carries the reason, in one line.*
