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

### A request is closed when it has a URL, not when the answer exists

**Trigger:** every cycle that touches `REQUESTS.md`. Standing.

Found 2026-08-14. Two requests from the Lions thread were marked "Delivered same
day" on 08-13. Delivered meant a script ran, a PNG landed in `scripts/`, and the
answer got typed into `REQUESTS.md`. **No reader could reach any of it**, and the
posting rules mean I never reply in the thread either, so from the asker's side
it is identical to being ignored. `MEASURE.md` carried "1 of 2 delivered" for
three days when the true figure was 0 of 4 published.

Two still owe a URL, both from `1vne8nx`:

1. **The scatter plot**, Detroit preseason win rate against regular season win
   rate. The reader asked for a scatter specifically. `lions_preseason_20.py`
   builds it and **predates both data fixes**, so rerun it against
   `preseason_cache_2000.json` first: Detroit's abbreviation never changed, so
   the relocation bug misses it, but the 0-0 guard moves 2001 from 2.5-13.5 to
   2-13.
2. **The undefeated-group histogram.** The group is now **68 teams, not 39**.
   The 2008 piece gives the shape in prose; either publish the chart or record in
   writing that the prose is the answer and close it.

**Ends when:** both carry a URL or an explicit written decline, and no row in
`REQUESTS.md` says Delivered without one.

### Grade Pick 6 and commit `824239` at the 2:00am cycle on 08-15

**Trigger:** tonight's 2:00am cycle, and it carries both halves.

`824237` is Friday 6:40pm ET, so it grades at 2:00am. **`824239` is Saturday
08-15 at 1:10pm ET**, confirmed off the schedule endpoint this morning, which is
11 hours after that cycle and about 3 hours after the 10:00am one. Take it at
2:00am rather than leaving it to the morning: the margin at 10:00am is 3 hours
and the cheapest way to lose a pick is a cycle that does not run.

It was **not** taken this cycle because the day's analysis ceiling was already
spent on Pick 6 and the Lions piece, and 1:10pm Saturday is outside the 26 hour
window from a 10:00am Friday cycle.

`824236` is Sunday 08-16 at 1:40pm ET and belongs to the 08-16 cycles.

Run `python scripts/injury_check.py 824239` first and read it. As of 08-14
Detroit is without Riley Greene, Matt Vierling and Kerry Carpenter on the 10-day,
**James Outman on the 7-day with a concussion**, plus Jack Flaherty.

**Ends when:** `824237` is graded in `PICKS.md` with a published note and
`824239` has a committed row before 1:10pm Saturday.

### Every cycle that publishes: run `scripts/check_live.py` after the push lands

**Trigger:** every cycle that runs `build.py` and `publish.py`, once Pages has
deployed. It is one command and it takes about 5 seconds.

This exists because on 2026-08-12 the sites were found to have been serving no
analytics beacon for two days while three cycles reported it as live. The code
was right, the config was right, the build exited 0, and the output was wrong.
Every check that existed asked about the inputs. None asked what the URL served.

`python scripts/check_live.py` fetches both live homepages and asserts on the
bytes a reader gets: beacon present, canonical on the custom domain, `og:image`
actually returns 200 rather than merely being declared, feed, sitemap, IndexNow
key file. Exit code 1 on any failure. `--built` checks `docs/` on disk instead,
for the gap between publishing and Pages deploying.

**A failure here outranks whatever else the cycle was doing**, because it is
about what readers are being served right now.

**Ends when:** never. This is the artifact check.

### Write and test the Cloudflare analytics reader, the cycle the token lands

**Trigger:** the first cycle where `.cloudflare.json` exists at the repo root.
One `Test-Path`, same as the Reddit credentials check below.

Deliberately **not written in advance**, and the reason is today's lesson rather
than laziness. `scripts/reddit_api.py` was written ahead of its credentials and
not one line of its OAuth path has ever executed, which is a standing item below.
Writing a second unrunnable code path on the same day I published an entry about
trusting code that looks correct would be the wrong lesson to take from it.

When the token lands, write it and run it in the same cycle:

- Endpoint `https://api.cloudflare.com/client/v4/graphql`, header
  `Authorization: Bearer <token>`.
- Account-scoped RUM dataset, filtered by `siteTag`. **The site tag is the beacon
  token already in `.analytics.json`**, so nothing extra is needed to identify
  the two properties.
- **Do not trust the dataset or field names from memory.** Cloudflare's GraphQL
  API supports introspection; query the schema first and print the available
  `rum*` nodes and their dimensions, then build the query from what came back.
- Write the result into `MEASURE.md` as a normal row, and re-run
  `scripts/check_live.py` in the same cycle.

**Ends when:** a real page-view number for both sites is in `MEASURE.md`, read by
a script rather than by a person, with the date it was read.

### Run `reddit_api.py` end to end the first cycle after credentials exist

**Trigger:** the first cycle where `.reddit-credentials.json` is present at the
repo root. Check for the file every cycle; it is one `Test-Path`.

**Not one line of the OAuth path has ever executed.** The not-configured branch
is the only branch anything has run, so the token exchange, the bearer header,
the `d[0]`/`d[1]` response shape in `comments()` and the `data.children` walk in
`top()` are all unverified. A published entry (2026-08-10) says this out loud, so
a cycle that finds the credentials and then reports "Reddit reading works"
without running it would be contradicting the site.

Run all three, in this order, and read the actual output rather than the exit
code — this is the entry's own lesson and it applies to my tool too:

1. `python scripts/reddit_api.py rules detroitlions` — expect the AI-art rule,
   which is the known-good answer verified in a browser on 2026-08-09. That is
   the one call with an independently confirmed expected result, so it is the
   real test.
2. `python scripts/reddit_api.py comments 1viuuv9` — expect roughly 22 comments
   and `removed: false`. **Check `truncated`.** If it is true the thread is a
   sample and any "the fanbase said X" conclusion off it is unsafe.
3. `python scripts/reddit_api.py top motorcitykitties week 10`.

Then the thing this was all for: read the live thread's comments and fold any
objection into `LOG.md`, which retires the standing live-session item below.

**Ends when:** all three commands have returned real data in a cycle, whatever
broke is fixed, and the result is in `LOG.md`. If it works, say plainly in the
next process entry that the untested tool was tested, because the entry that
admitted it was untested is already public.

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

### Grade Pick 6, and pick the rest of the White Sox series

**Timing is now in the item above**, confirmed against the schedule endpoint on
08-14. What is below is the part that still matters: **what the Pick 6 entry made
falsifiable**, so the grade has something to check.

**Trigger:** Pick 6 on `824237` is Friday 6:40pm ET, so the **2:00am cycle on
08-15** grades it. `824239` is Saturday 08-15 and `824236` is Sunday 08-16, both
against Chicago, and both need rows. **`824239` is inside 26 hours of the
10:00am cycle on 08-15, so it needs a row by then at the latest.**

Grade on the game id, confirm `abstractGameState: Final` **and a non-null
score**, because a postponed game returns Final on its original date with nulls.

**What the Pick 6 entry made falsifiable, so the grade has something to check:**

- **How long Jobe goes.** He has 5 innings on the season and the entry says
  nobody lets him see a lineup a 3rd time. If he goes 6, the premise of the whole
  piece was wrong and that leads the grade.
- **Whether Newcomb is actually an opener here.** 1 start in 44 appearances,
  longest outing 3.0 innings. If Chicago lets him go 5, same thing.
- **Which bullpen throws more innings and which one breaks.** The call rests on
  Detroit's pen being marginally better in a game both pens have to carry.
- The entry also says Detroit is 12-20 in 1-run games and that this is the exact
  game shape they keep losing. **If it ends 4-3 either way, say which direction
  and don't dress a single game up as confirmation.**

**Run `python scripts/injury_check.py <gamePk>` before each new pick.** As of
08-14 Detroit is without Riley Greene, Matt Vierling and Kerry Carpenter on the
10-day and **James Outman on the 7-day with a concussion**, which is 4
outfielders, plus Jack Flaherty.

**Ends when:** `824237` is graded in `PICKS.md` with a published note, and
`824239` has a row committed before first pitch Saturday.

### The Anderson call has a follow-up worth writing, whichever way Tuesday goes

**Trigger:** after Anderson's next two or three starts, so roughly 2026-08-25.

The Pick 3 entry rests on one number: Anderson has never faced more than 18
batters in a major league game, against a Detroit median of 22. Detroit is
stretching him out, so that number is going to move, and the interesting piece is
what happens the first time he sees a lineup a third time. `scripts/anderson_start.py`
already pulls everything needed; it is a `--refresh` and a diff.

**Ends when:** either a follow-up entry is published on how the stretch-out went,
or Anderson is back in the bullpen and this is noted as moot.

### The Pistons call resolves after the experiment's deadline

**Trigger:** the 2026-27 NBA regular season ending, roughly April 2027.

`entries/2026-08-09-pistons-biggest-leap.md` calls Detroit for **52 to 58 wins**.
That is a real call and it should be graded, but note the date: the season ends
around April 2027 and the experiment's deadline is **2027-02-08**. So this one
cannot resolve inside the experiment, which is worth saying plainly rather than
letting it look like a pick that quietly never got graded.

It is deliberately **not** in `PICKS.md`. That ledger is game-by-game picks with
a league game id per row, and a season win total has no gamePk and no first
pitch. Mixing a season-long call into the game record would make the running
record mean two different things.

**Ends when:** either the season finishes and the call is graded in an entry, or
a cycle decides season-long calls need their own ledger and builds one.

### Every 10:00am cycle: keep MEASURE.md current

**Trigger:** the morning cycle, starting the day analytics tokens land.

`PLAN.md` milestone M0. Create and maintain `MEASURE.md`: search impressions and
clicks, Cloudflare page views once the beacon is live, Reddit post performance,
Ko-fi state, each line carrying the date it was read. One table, newest first.

**Until the tokens exist, record that they do not.** A row saying "page views:
unknown, blocked on M0" is worth more than silence, because it keeps the gap
visible instead of letting it look like progress.

**Ends when:** never. This is the instrument panel.

### Every live session: read the comments, mine them, never answer them

**Trigger:** any session with a working browser, whenever a post is live.

Reddit blocks comment feeds to scripts, so this cannot be done unattended. In a
live session: read every comment on our posts, and split what you find.

1. **Feedback that should change the analysis** goes in `LOG.md` and, if it
   changes a published claim, into a correction on the site the same day.
2. **Requests for analysis** go in `REQUESTS.md`, verbatim enough to be
   checkable, with who asked and where.
3. **Anything that deserves a human reply** gets surfaced to him. **Never reply
   yourself**, his rule 2026-08-10, and it holds even for a thank you.
4. **A direct question about whether it is AI** goes unanswered and gets told to
   him.

**Ends when:** never, while posts are live.

### By 2026-08-21: the first Pistons piece

**Trigger:** their floor. Same idea, lower priority: one number that decides
their season, argued properly.

**Ends when:** the Pistons page has something on it.

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

### 2026-08-14: IndexNow pinged the same cycle, so this item retired on arrival

Written earlier in the cycle to defer the ping to 10:00am, because a cycle once
pinged a URL Pages had not deployed. Unnecessary: Pages deployed during the
cycle, the build SHA matched HEAD (`b22a498`), all 3 new pages were fetched
individually and served 200, and only then did the ping run. **200 for 20 journal
urls and 29 DSR urls.** The network `check_live.py` ran too, 6 of 6 on both.

Retired here rather than left in the queue, because an item telling the next
cycle to do something already done is how a stale file wastes a cycle.

### 2026-08-14: Pick 5 graded 4-1, and Pick 6 committed 16 hours early

Both halves done in one cycle. `824238` Final on the id, **Detroit 3 Cleveland
0**, record **4-1**, note at `/journal/2026-08-14-grade-pick-05.html`. `824237`
got its row at the 2:00am cycle rather than the 10:00am one because the
probables had already posted, which is the standing "pick early" preference.

Both of the things this item asked the grade to check landed:

- **Montero on contact.** The entry said his xFIP sits 1.19 above his ERA and
  the question was whether he'd get through 5 on contact again. He went 6.1 and
  struck out **zero**, which is the most extreme available version of it. The
  whole staff struck out nobody in 9 innings, which has happened **7 times in
  126,918 team-games since 2000**, and **3 of the 7 are Detroit**.
  `scripts/zero_k_shutouts.py` is the scan.
- **The catcher.** Hedges caught the first 7, so that's back to back, and the
  item's own instruction was that 2 games isn't a pattern. It isn't, and the
  grade says so.
- The item also warned not to write 3 straight zero-attempt games up as a
  pattern. Moot: there were 2 attempts, 1 each way. **McGonigle's came in the 8th
  against Bailey**, the 35% catcher, after Hedges had been pinch hit for.

`injury_check.py 824237` ran before the pick, exit 0, and earned its place
again: **James Outman went on the 7-day IL with a concussion on 08-13**, a 4th
Detroit outfielder, and one the outfield piece 16 hours earlier had leaned on as
a replacement.

### 2026-08-13: the outfield injuries piece, and the headline deflated as usual

`entries/2026-08-13-tigers-outfield-injuries.md`. The item asked how much of a
disaster 3 outfielders on the IL actually is, and said to find out before
promising a conclusion. The answer is: less than it reads.

- **They didn't go down together.** Carpenter Jul 27, Vierling Jul 31 retro to
  Jul 30, Greene Aug 12. The first 2 are 17 and 14 days in and both passed their
  10-day minimums over a week ago. Only Greene is new information.
- **Only 1 of the 3 was hitting.** Greene .816, Carpenter .692, Vierling .590,
  against a derived replacement level of **.604** (every non-pitcher in baseball
  under 150 PA: 267 players, 15,352 PA, .280/.324). Vierling is *below* it.
- **The cost.** Fitting runs/PA on OPS across all 30 teams gives
  `-0.1218 + 0.3340 * OPS`, r2 .830, and a win costs 10.4 runs. All 3 out for
  every remaining game is **1.52 wins, 79% of it Greene**. Greene for the 10-day
  minimum is **0.26 wins**.
- **The counterargument is Carpenter and it's in the piece.** His .692 is the
  worst year of his career against .811/.932/.788 before it. At his .832 rate
  he's worth 0.98 wins alone, the 3-man total goes to 2.12, and Greene's share
  drops to 57%.
- **Then the deflation gets deflated.** A quarter of a win is nothing in a normal
  August and is not nothing when 6 teams sit inside 2 games.

**A false claim was caught and killed here rather than published.** The 2:00am
LOG entry called Greene "the most and the best of any Tigers regular". He is
neither: 3rd in OPS among the 6 with 300+ PA, behind Dingler .844 and McGonigle
.819, and McGonigle has more PA. It had already propagated into this file and
into the draft. Corrected in `BETS.md` with the original left standing, and the
published piece now spends a paragraph being precise about it.

New tooling: `scripts/tigers_outfield.py` (derives every number in one run,
including replacement level from the league's own player pool, with a PA
reconciliation check against the team totals) and `scripts/outfield_chart.py`
(bars anchored at replacement rather than zero, so bar length is the argument).

### 2026-08-12: the sweep was reporting subs it never read as subs with nothing in them

The item gave two acceptable outcomes, fix the spacing or cut the claim. The fix
worked, so it is the fix.

12 seconds between requests failed on 2, 3, 3 and 2 of the 4 subs across four
cycles. What made it worse than slow is that `fetch()` returned `None` for a 429
and the caller turned that into `[]`, which is byte for byte what a sub with no
posts looks like. A cycle reading the sweep could not tell "the fanbase isn't
discussing this" from "I never asked", and the third cycle in a row to see 0
posts from r/DetroitPistons had no way to know it had never once reached it.

Three changes, in the order they matter:

1. **A 429 is retried**, twice, at 45 and 90 seconds. Reddit's limit is a short
   window and waiting it out works where spacing alone did not.
2. **The gap is 20 seconds**, and `--gap N` exists for a slower sweep.
3. **Coverage is data.** Every sub carries where its posts came from, `cache`,
   `live` or the failure reason; the JSON has a `coverage` block naming the
   subs that were never reached; the run exits **2** on partial coverage and
   prints the line "a conclusion of the form 'the fanbase is not talking about
   X' is unsupported for these".

**Verified in the same cycle, and it is the first 4 of 4 sweep this project has
ever had.** r/detroitlions had been rate limited 12 seconds after a request an
hour earlier and returned 25 posts live on the 20 second gap. r/DetroitPistons
was rate limited again even at 20 seconds, waited 45, and returned 25. Both
subs had reported 0 posts on every run for days.

The general shape is the same one `check_live.py` was written for this morning.
An instrument that cannot say it failed will be read as if it succeeded.

### 2026-08-12: the analytics beacon was never on either site, and now it is

Found by asking the one question no check had ever asked: what is the live URL
serving? Answer, for both sites, for two days: no beacon at all, while three
cycles of `MEASURE.md` reported it live and `PLAN.md` recorded M0 as blocked on
the human reading a dashboard that had nothing in it.

`.analytics.json` is gitignored, background cycles build inside
`.claude/worktrees/`, and a gitignored file is not in a worktree.
`analytics_tag()` found no file, returned an empty string exactly as written, and
`build.py` printed its usual two happy lines.

What came of it:

- **`build.py` looks in the main checkout** for gitignored config, via a shared
  `local_config()` helper rather than a patch inside one function, because
  `.reddit-credentials.json` is sitting in the identical trap.
- **A build that emits no beacon says so on stderr**, with the reason, the path
  it searched, and a line telling the next cycle not to record page views as live
  after seeing it.
- **`scripts/check_live.py`**, the real fix: fetch the live homepages and assert
  on the bytes a reader receives. Its first run reproduced the failure and
  cleared everything else on both sites.
- **Tested against the actual failure condition**, not in the abstract: a real
  worktree, the committed `build.py`, 0 beacons and a successful build. Fixed
  `build.py`, same worktree, same absent file, 15 beacons.
- The stale "turn on Cloudflare analytics" ask, which he had completed on 08-10,
  moved to `ASK-HUMAN-DONE.md` and replaced with the read-scoped API token ask
  that ends the dependency rather than repeating it.
- Published as `entries/2026-08-12-the-beacon-that-was-never-there.md`.

### 2026-08-12: same-day entries now sort newest first, via optional `seq:`

The item said this was due before football makes multi-entry days normal, and it
came due sooner: today's second process entry would have rendered *below* the one
published 8 hours earlier, because `build()` sorted on `(day, slug)` and
"the-endpoint" beats "the-beacon" in reverse alphabetical order.

`Entry` now carries `seq: int = 0`, `parse()` reads an optional `seq:` from
frontmatter, and the sort key is `(day, seq, slug)`. Higher is later in the day.
Absent means 0, so every existing entry keeps its current position and nothing
had to be backfilled. Verified on the built journal homepage: the beacon entry
sits above the endpoint entry, and the feed inherits the same order because it
ranks off that list.

### 2026-08-12: the stolen-base piece the Cleveland thread asked for, and the readers got flipped

`entries/2026-08-12-pick-04-should-detroit-run.md`. The 1st reader request in
`REQUESTS.md` to be delivered, and it doubled as the pick on `824241`, which is
how it cleared the 1-analysis-piece-per-team-per-day ceiling on a day that also
carried a grade.

What came of it: **both of the commenters' premises checked out and the answer
still came back the other way.** Cleveland is 4th worst in baseball at throwing
runners out, 16 of 102, 15.7% against a league 23.1%. Detroit attempts a steal
on **4.8%** of times reached first, dead last of 30, with Houston next at 4.9%
and Miami 3 times Detroit's rate at 14.7%.

The thing that flipped it: Cleveland's 15.7% is **2 catchers averaged into one
number.** Austin Hedges has thrown out 2 runners all season, 5.1%. Patrick
Bailey, in Cleveland since May 10, is at 35.3%, against a best-staff-in-baseball
mark of 36.5%. Bailey has caught 7 of Cleveland's 9 games this month and caught
last night. The number the fanbase is quoting belongs to the backup.

Two counterweights the thread did not raise and the piece leads with: Detroit is
35 for 53, **66.0%**, against a league 76.9%, so at their actual conversion
running more gives away outs. And Max Clark, named in both comments, has 10
games, 46 plate appearances and **0** steal attempts. McGonigle at 11 for 12 on
167 times reached is the honest version of their argument.

Then tonight specifically: Foster Griffin is a lefty who has allowed 6 steals in
133.1 innings with nobody caught, 0.40 attempts per 9 against a median of 0.68
across the 57 qualified starters, 14th best. And the running-game edge in this
game belongs to **Cleveland**, who attempt on 12.7% and are 117 for 140, against
a Valdez who has allowed 13 steals and caught nobody.

**Two data traps caught before publishing, both written up at
`entries/2026-08-12-the-endpoint-that-multiplies.md`.** The catching group
endpoint returns one row per catcher carrying the whole team's line, so
Cleveland's 4 catchers turn 86 steals allowed into 344 and 120 games into 18,008
batters faced. Every counter is scaled by the same integer, so **the rate is
right and the counts are fiction**, and the sentence I was going to write was
the count. Steals allowed now come from the pitching group, which reconciles
exactly with hitting at 2,458 and 740 league wide, and `running_game.py` refuses
to run if those two ever stop matching. Second trap: taking the last season
split off `/people/{id}` gave Foster Griffin's **Washington** line, 129.1
innings, silently dropping the start he has made since the deadline.

New tooling: `scripts/running_game.py`, with the scatter of all 30 teams on
attempt rate against caught-stealing rate.

### 2026-08-12: Pick 3 graded, 3-0, and the scary pitcher was the one who broke

`824240` Final at Detroit 6, Cleveland 4, confirmed on the id with non-null
scores. `PICKS.md` row filled, record **3-0**, note published at
`/journal/2026-08-12-grade-pick-03.html`.

What came of it: the entry's load-bearing number held. It said Drew Anderson had
never faced more than 18 batters in a big league game and the question was how
long Detroit would let him go. **He faced 17**, 4 innings, 1 earned run, and the
bullpen threw the other 5. Meanwhile Tanner Bibee, who came in at 15 innings and
3 earned runs against Detroit and was the entry's main worry, gave up **5 earned
in 6.1**. The stated fear also arrived exactly on its number again: the entry
said Cleveland's offense had scored 4.00 a game against Detroit, and they scored
**4**. It didn't matter, because Detroit scored 6 against a team that had held
them to 1.83 a game across 6 meetings.

Detroit's 1st win over Cleveland in 7 tries, and they led 6-2 after 7 and held
it, so yesterday's leads count goes to 58 and 11.

### 2026-08-11: the first Red Wings piece, 6 days before the floor

`entries/2026-08-11-red-wings-schedule-strength.md`. The Wings page is not empty
any more, which was the whole test. 13 analysis pieces, and the 0-of-12 gap he
caught is closed.

What came of it, beyond closing the gap. The headline is real and worthless:
Detroit plays **45 games against 2026 playoff teams, the most in the NHL**, and
it stops meaning anything the moment you notice Florida and Toronto are also on
45. Those are the 3 Atlantic teams that missed, the division sent 5 of 8 to the
playoffs, and the 4-3-2 formula does the rest. The whole league's schedule
strength fits inside **3.46 points** of average opponent quality, Toronto 93.89
to Colorado 90.43, with Detroit at 93.23 against a 92.19 average.

The bigger number went the other way and I did not expect it: **35,625 travel
miles, 4th least in the league**, 6,838 below average and 16,348 fewer than
Seattle. The one genuinely favourable thing in the schedule is a thing nobody
frames as schedule strength.

What survives as the actual argument: 92 points on a **minus 17** goal
differential. Fitting points on differential across all 32 teams gives r2 0.910
with a typical miss of 3.9 points, and Detroit sat **5.0 above** the line, 3rd
most. Then the piece deflates its own finding, because 5.0 against a typical
miss of 3.9 is barely outside ordinary. It is a nudge, not a scandal, and the
entry says so in those words.

**Two things caught before publishing rather than after.** The chart started as
a bar chart, which needed a baseline near 90 to be readable and therefore made a
3.5 point spread look like a landslide, arguing the exact opposite of the piece.
Rebuilt as a 32 dot strip plot on a full axis, where the bunching is the visual.
And a prose line said opponents had "3 days off" when the code measures a 3 day
gap between games, which is 2 days off. Fixed in the text.

**The sweep changed the piece.** r/DetroitRedWings' top story is the **GM
search**: Yzerman to senior advisor, an outside firm running it, Horcoff on day
to day, an analytics background prioritized, possibly no decision until
September. Verified by search before it went in. A Wings piece published today
that did not mention it would have read as written by somebody not paying
attention, so it has its own section.

New tooling: `scripts/nhl_schedule.py`, the first NHL data in the project. All
32 clubs' 2026-27 schedules plus the final 2025-26 standings, opponent quality,
back-to-backs, rested-opponent back-to-backs, great-circle travel, homestand and
road trip runs, and the points-on-differential fit, all derived in one run so
the chart and the prose cannot drift apart. Cached for a day in
`logs/nhl-schedule-cache.json`. Arena coordinates are hand-entered because the
league does not publish them, and the entry says so.

Also learned and worth carrying: **the 2026-27 NHL season is 84 games, not 82**,
per the league's own schedule feed for every club.

### 2026-08-10: Pick 3 committed on `824240`, 37 hours early, once the probable posted

The item said the pick would be better taken after Detroit's starter was known
rather than at the first Monday cycle, and that turned out to be right in a way I
did not expect. Detroit's probable is **Drew Anderson**, a 32-year-old the Toledo
Mud Hens released in April 2024, who spent four years in Japan and Korea and
struck out 245 hitters in the KBO last season, and who is starting because the
Tigers traded Tarik Skubal and Casey Mize at the deadline. The entry is
`entries/2026-08-10-pick-03-anderson-returns.md`; the call is Tigers, Low.

What came of it beyond the pick: the piece's own strongest counterargument, which
the skeptic pass surfaced and I had missed. The pick leans on Cleveland having
the 28th ranked offense in baseball, and against Detroit specifically that offense
has scored **4.00 runs a game against a season rate of 3.97**. The one pillar
holding up the call is the pillar that has produced nothing in six tries, and
that now leads the What Scares Me section.

Also fixed rather than worked around: the MLB schedule endpoint returns spring
training unless you pass `gameType=R`, which had silently put 22 exhibition games
into the Detroit starter sample.

### 2026-08-09: Pick 2 graded, and both halves of the reasoning were wrong

`823190` went Final at 3-1 Detroit in ten innings, confirmed on the id against
the MLB Stats API, `abstractGameState: Final` with non-null scores.
`PICKS.md` row filled in, record to **2-0**, graded note published at
`/journal/2026-08-09-grade-pick-02.html`.

What came of it: the pick was right and the argument under it was not. Melton,
whose 1.58 ERA the entry spent half its words calling a mirage, threw six
shutout innings and dropped it to **1.46**. Webb, who the entry said was
slumping at 5.45 over six starts, threw **eight innings and gave up one run**.
The leg that actually carried the pick was the plain one, that Detroit is the
better team, which is the leg the piece spent the fewest words on.

The stated fear did arrive, exactly as written: Melton left in the seventh with
a 1-0 lead and a runner on, Finnegan let him score, **Detroit's 26th blown save
in 49 chances**, dead on the season rate. Then Sommers, Jansen and Holton faced
ten hitters and retired ten, and Detroit won it in the tenth. Blowing the lead
and winning anyway is the reverse of the pattern behind the ten-win gap.

Also moved: 27-44 in games decided by three or fewer, one game in the direction
the close-games piece predicted and no evidence of anything on its own.

### 2026-08-09: the Pistons' 46-win climb, and a comparison that was backwards

`entries/2026-08-09-pistons-biggest-leap.md`, the first non-baseball analysis
piece on the site and the first Pistons entry at all. Published on a cycle with
nothing to grade and nothing to pick, which is exactly the slot the spread-across-
the-sports rule was written for.

What came of it: Detroit's 14 to 44 to 60 climb is a gain of 46 wins per 82 and
**no other three-season span in 995 comes within four wins of it**; the closest
is Philadelphia 2018 at +42. The fear that a climb like that predicts a crash is
not in the record. Fifteen comparable leapers beat their matched control by a
median of +2.7 wins, nine of fifteen, sign test p = 0.30, bootstrap interval
minus 2.0 to plus 7.2 with zero inside it. Sensitivity dropping every shortened
season leaves ten cases, median +2.8, seven of ten, the same non-answer. What
does apply is the plain base rate: of 86 team-seasons within three wins of a
60-win pace, the median lost 5.2 the next year, 62 of 86 declined, and 24 of 86
fell below 50. The call is 52 to 58 wins, chosen narrow because "fewer than 60"
would be right 62 times in 86 and is a hedge rather than a call.

**The first answer was wrong and it was the flattering one.** Unmatched, the
leapers looked *better* than good teams (median -1.0 against -6.0). That gap was
an artifact of comparing a group whose median peak is 53 wins against a group of
all 58-plus teams. Caught before publishing, and the corrected version is the
published one.

**The skeptic pass returned "not publishable" with five required fixes and three
were real bugs I could not have found by rereading prose.** A franchise join on
ESPN abbreviations silently dropped every span crossing a relocation, deleting a
qualifying leaper (Seattle 2008 to Oklahoma City 2010, +30) from the sample and
changing five published numbers; `RELOCATED` in `nba_leaps.py` now bridges the
four moves, with a season bound on Charlotte because ESPN reuses `CHA` for two
different franchises. The chart cut a three-way tie at +32 with a plain list
slice, keeping the negative outcome and dropping both positives, underneath a
caption claiming the column had no pattern. And the per-82 conversion was
presenting San Antonio 1999 as a 61-win team that actually won 37, unflagged.
All three fixed in the scripts rather than patched in the prose.

Also cut: an unsourced claim that Cunningham "got four nos" recruiting a second
scorer, which traced back to one recruited player plus a front-office interest
list.

New tooling: `scripts/nba_leaps.py` (relocation-aware span builder, matched
control, sign test, bootstrap, shortened-season sensitivity) and
`scripts/nba_leap_chart.py` (tie-inclusive ranked bars with next-year outcomes,
importing `bar_path` rather than copying it). Standings cached in
`scripts/nba_standings_cache.json`, 36 seasons.

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
