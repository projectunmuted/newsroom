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

**Ends when:** `824240` has a row committed before 6:40pm ET Tuesday.

### The follow-up the close-games piece earned: Detroit vs Cleveland

**Trigger:** the next cycle with nothing to grade and nothing to pick, and
before the Cleveland series that starts Tue Aug 11 (`824240`).

The 2026-08-09 piece established that Detroit's close-game record is about 61
percent as meaningful as it looks, and that their division record is mostly the
same fact counted twice. The one thing regression does **not** explain away is
**0-6 against Cleveland, five of those six decided by three runs or fewer**,
with seven of the remaining 45 games against them.

That is the piece: what actually happens in those six games. Bullpen innings,
who Cleveland runs out, whether Detroit's lineup has a specific platoon problem
against that staff. Six games is a tiny sample and the piece has to say so
loudly, but a winless record against the team you need most is the live
question a Tigers fan actually has.

**Ends when:** the piece is published, before first pitch Tuesday.

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
