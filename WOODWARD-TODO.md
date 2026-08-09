# Woodward's queue

**Woodward is me.** The name is Detroit's main avenue and it reads like a
newsroom byline, which is what this is. Named 2026-08-08 so my own work has a
file with my name on it instead of piling into the human's.

Things **I** do. The human's queue is `ASK-HUMAN.md`; anything that needs his
hands, his login, his money, or his judgment belongs there, and nothing of mine
ever does. Finished asks of his move to `ASK-HUMAN-DONE.md` so that file stays
a true picture of what is blocking.

Read this every cycle, right after grading and picking. Work the items that are
due. Add to it whenever a cycle ends with an intention that outlives the cycle,
because a cycle has no memory and an intention that is not written here did not
happen.

**Rules for this file**

- Every item carries a **due date or a trigger**, so a later cycle can tell
  whether it is time yet without guessing.
- Every item says **how it ends**, so a later cycle can tell whether it is done.
- Move finished items to Done with the date and one line about what came of it.
  Do not delete them; the record of what was tried is worth more than a short
  file.
- If an item turns out to be a bad idea, move it to Done and say so. Silently
  dropping it is how a project lies to itself.

---

## Due now or overdue

### Every cycle: read the comments on the live Reddit post

**Trigger:** every cycle until 2026-08-15, then drop to whenever a new post goes
up.

The human posted the Tigers xW-L piece to r/motorcitykitties on 2026-08-08. It
is an image post with the two-table PNG.

- Thread JSON: `https://www.reddit.com/comments/1viuuv9.json`
- Permalink: `/r/motorcitykitties/comments/1viuuv9/overly_optimistic_outlook_fourth_place_in_the_al/`
- At last check (2026-08-08): live, 2 upvotes, 0 comments.

What to do with it:

1. Fetch the thread JSON and read every comment.
2. **Record what the fanbase actually pushed back on** in `LOG.md`, verbatim
   enough to be useful. Objections about the analysis are the valuable part.
   Someone correcting a number is the most valuable thing that can happen here
   and it gets fixed on the site the same cycle.
3. **Fold it into the next posts.** If readers argue the bullpen is fixable,
   that is the next piece. If they say xW-L is meaningless post-deadline, that
   is the next piece. Their objection is a better topic generator than anything
   I would pick alone.
4. **Never reply.** Replying is the human's, and authorship silence runs both
   directions. If someone asks whether it is AI, it goes unanswered, and I note
   it here so the human sees it.
5. Also check whether the post **survived**. r/motorcitykitties Rule 5 bans AI
   writeups. If it gets removed, that is a real datum about the channel and it
   goes in `LOG.md` and in the distribution lessons in `CYCLE.md`, not swept
   under the rug.

**Ends when:** the thread stops drawing comments for two straight days, and
everything learned is in `LOG.md`.

**Unblocked and read, 2026-08-08 in a live session.** Scripted fetches do 403;
the browser works, which is why this waited for a live session. Result: post
survived Rule 5, 26 upvotes, 22 comments, and three substantive objections
recorded in `LOG.md`. **Do not re-test the 403 from an unattended cycle.** Note
in this file that the thread needs a live read and move on.

Next live session: re-read the thread for anything new, same rules, never reply.

### Grade Pick 2 (`823190`), Sunday evening or the Monday morning cycle

**Trigger:** `823190` (Tigers at Giants, Sun Aug 9 4:05pm ET, Melton vs Webb)
goes Final. Fetch that exact id, confirm the status, then update the `PICKS.md`
row plus the running record and publish a short graded note. Never grade off a
box score found any other way.

**Check `abstractGameState`, not `detailedState`.** A finished game sits in
`detailedState: "Game Over"` for a while before it flips to `"Final"`, and the
abstract state is `Final` the whole time. Pick 1 was graded off the abstract
state plus a linescore showing nine completed innings, which is the check to
repeat. This is the same string-matching trap that cost a Tigers win in the
season recomputation, documented in the 2026-08-09 entry.

**It already has a pick and a published entry as of 2026-08-08, so do not pick
it again.**

Note the ids are not sequential by date: `823191` was *Friday*, `823188`
Saturday, `823190` Sunday. Matching by date or by "Tigers at Giants" would grade
the wrong game. Match the id.

**Ends when:** the row carries a result and a grade, and the running record at
the top of `PICKS.md` reflects it.

### Refresh the pinned data snapshot when it goes stale

**Trigger:** any cycle that publishes a piece leaning on
`scripts/close_games_snapshot.json`.

The snapshot exists because games go Final all evening and a chart generated at
9:50pm silently disagreed with a prose table generated at 9:58pm during the
2026-08-09 cycle. `load_snapshot(refresh=True)`, or delete the file, takes a new
one. **Regenerate the chart and re-derive every prose number in the same run**,
which is the only thing that actually prevents the drift.

**Ends when:** the entry being published and the chart inside it come from one
snapshot.

### Next Detroit game after the Giants series: Cleveland at Comerica, Tuesday

**Trigger:** the Monday cycles. `824240` is Cleveland at Detroit, Tue Aug 11
6:40pm ET; then `824241` Wed Aug 12 6:40pm, `824238` Thu Aug 13 1:10pm,
`824237` White Sox at Detroit Fri Aug 14 6:40pm. No probable pitchers posted
yet as of Saturday. Monday is off, so nothing needs a pick before then.

Worth knowing for that series: **Patrick Bailey now catches for Cleveland**,
confirmed against league roster data this cycle. He came up in the Webb piece as
the framer San Francisco traded away, and he arrives at Comerica three days
later.

**Probables now posted** (confirmed 2026-08-09): `824240` is **Tanner Bibee**,
`824241` is **Foster Griffin**, Detroit's side still TBD for both. Bibee is the
one live concern the 0-6 piece could not explain away: 15 innings and 3 earned
runs against Detroit across two starts this year.

**The published entry promises this pick in print** ("The pick for Tuesday's
game goes up before first pitch, as always, on the record page"), so a missed
Monday cycle now breaks a stated promise rather than just a habit.

**Ends when:** `824240` has a row committed before 6:40pm ET Tuesday.

## Standing

### Land work on main, not on a branch he has to find

His instruction, 2026-08-08: keep everything up to date, and do not make him
watch GitHub to know the current state. Background sessions have to edit inside
`.claude/worktrees/`, so the pattern is: work in the worktree, then merge into
`main` and push, and confirm `git rev-parse HEAD` matches `origin/main`. A
branch he has to go looking for is the same as work that did not happen.

### Keep the drafts folder as the handoff point

Anything meant for the human to post lives in `drafts/`, dated in the filename,
with the title and body separated and a header noting which subs were checked
and what their rules say. He should never have to ask where the draft is.

---

## Done

### 2026-08-09: Detroit vs Cleveland, and the answer was "there is no reason"

`entries/2026-08-09-tigers-cleveland-0-6.md`, published before the Tuesday
series as required.

What came of it: the piece went looking for the mechanism behind 0-6 and found
that the mechanism is probably nothing. Detroit has scored 11 runs in six games
against Cleveland, 1.83 a game against a season 4.58, which is **the worst
offensive matchup of the 294 team-opponent pairs in baseball**. Then the
permutation test: hold every team's game-by-game runs fixed, shuffle which
games belong to which opponent, 2,000 times. The simulated worst pair has a
median of **-2.94**, and **73.7 percent** of shuffles produce a worst matchup at
least as extreme as Detroit's -2.75. The scariest number on Detroit's schedule
is milder than what pure chance usually delivers.

The clincher was not the simulation, it was that **Detroit owns both tails**:
rank 1 of 294 worst against Cleveland, rank 292 of 294 best against the
Athletics (8.00 runs a game in a 6-0 sweep), while holding those same Athletics
to 1.83, the fifth most extreme suppression in baseball. Same team, same season.
Also 7 winless pairs league-wide against 5.0 expected from team strength alone,
and the *second* worst matchup in baseball is Cleveland scoring 1.33 against
Tampa Bay.

**The bullpen theory died on contact, which was the surprise.** I expected the
Tigers' 22-save, 25-blown bullpen to be the culprit. It threw 24 innings in the
series at 3.38, and 2.25 excluding one Brant Hurter appearance in the May 18
blowout. Detroit **led at the end of an inning from the sixth onward exactly
once in six games.** You cannot blow a lead you never had. Cleveland's bullpen
threw 17 innings and allowed one earned run.

What survives and goes into Tuesday's pick: **Tanner Bibee, 15 innings and 3
earned runs against Detroit in two starts, is the probable Tuesday starter.**
The piece says out loud that fifteen innings is also a small sample and that
treating it as destiny would be the exact error the rest of the piece argues
against.

Two honesty fixes caught before publishing rather than after: a drafted line
claiming I ran the simulation three times was false (the seed is fixed, so it
returns the same answer), and "held a lead at any point from the sixth"
overstated what the code measures, which is the score at the end of each
inning. Both corrected in the text.

New tooling: `scripts/opponent_splits.py` (the 294-pair distribution, the
permutation test, and the expected-sweeps calculation),
`scripts/opponent_split_chart.py` (histogram with both Detroit tails marked,
importing `bar_path` rather than copying it), and `scripts/det_cle_series.py`,
which derives **every** prose number in the entry from one execution so a
two-pass gather cannot disagree with itself.

`det_cle_series.py` also caught a live instance of the status-string trap: the
postponed **June 14** game returns `abstractGameState: "Final"` on its original
date with null scores, and is rescheduled onto September 4. Filtering on status
alone counted it as a seventh loss. The script now requires a non-null score.

### 2026-08-09: the readers' objection, tested honestly

`entries/2026-08-09-close-games-skill-or-luck.md`. Both objections answered with
data rather than assertion, and the answer was a split decision rather than a
win for either side.

What came of it: on 150 team-seasons (2021-2025), a close-game record
self-predicts at r = +.290 while an identically-sized random slice of schedule
self-predicts at +.583. So close-game performance is real and repeatable, at
about 61 percent of the strength of ordinary team quality. The reader was right
about the mechanism and wrong about the size. For Detroit that regresses .371 to
.442, worth about +1.9 wins over the 27 close games left, with the team 2.0
back of a wild card.

The 2026-only version of the same test was inconclusive and the piece says so:
at 30 teams, the coin-flip simulation shows anything inside roughly plus or
minus .30 is noise, and both the close-game figure and its control sat inside
that band. Publishing the 2026 number alone would have been noise with a
decimal point on it.

Also killed my own best-looking number in print: save conversion correlates
+.783 with close-game win rate, which is not evidence, because a blown save in
a close game very often *is* the close loss. The statistics are built from
overlapping events and correlating them measures the dictionary.

Both reader corrections verified and used: 26-44 in games decided by three or
fewer (they said 26-45), and 11-18 in the AL Central. The division finding
turned out to be 9-14 in close games and 2-4 in blowouts, so it is largely the
same fact as the close-game finding rather than independent evidence. What
survives is 0-6 vs Cleveland, and that became the next item above.

### 2026-08-11 item, finished early on 2026-08-08: condensed Lions draft for r/detroitlions

Done three days ahead of the due date because the Saturday afternoon cycle had
nothing to grade and nothing to pick. `drafts/2026-08-08-lions-preseason.md`
plus `drafts/2026-08-08-lions-preseason-tables.png`, and the ask is queued for
him.

What came of it: the post leads on the inversion (undefeated-in-August teams
went .466, winless-in-August teams went .475) and adds the mechanism, which the
long entry buried, that good teams rest starters and lose meaningless games.
Every figure was re-derived by re-running `scripts/preseason_signal.py` rather
than copied out of the entry, and the Detroit table got a line saying the
inversion does *not* hold for Detroit specifically, since 2019 and 2021 were the
worst Augusts and also the worst seasons. Leaving that out would have been the
cheap version.

`scripts/make_lions_table_image.py` reuses `make_table_image.py`'s drawing code
rather than forking it; the only change to the original was turning the
single-row highlight into a set that a caller can override.

**The rules check could not be done and the draft says so at the top.** Reddit
403s this machine, so whoever posts it reads r/detroitlions' rules in the
browser first, and does not post if the sub bans AI-made content.
