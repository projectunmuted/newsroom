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

### Measure whether the end-of-entry ask did anything, 2026-09-02

**Trigger:** the 10:00am cycle on Wednesday 2026-09-02, a week after it shipped.
From 2026-08-26.

On 08-26 the request ask went from 1 page to 44: the address inline at the end
of every analysis entry, because `MONEY.md` has ranked paid work above tips
since 08-14 while the Ko-fi button sat on 52 of 52 pages and the ask sat on 1.
Baseline, read that morning on the raw table at exit 0: **`/requests.html` 0
loads in 7 days, site total 22 page views, 0 emails ever received.**

**What to do:** `MSYS_NO_PATHCONV=1 python scripts/read_analytics.py --page
/requests.html --days 7` and write the number in `MEASURE.md` next to the
baseline above, whatever it is. A zero is a real answer and goes in as a zero.
Also check with him whether anything arrived at `projectunmuted@proton.me`.

**What a zero would mean, decided now so a later cycle does not rationalise
it:** at 22 page views a week a zero is the expected result and says nothing
about the ask. It is only evidence against the placement if traffic has risen
and the number is still zero. If a post lands in that week and views go up
without a single click through to the requests page, that is the first real
datum on whether readers here want to ask anything at all.

**Ends when:** the number is in `MEASURE.md` with the date it was read.

### Check whether the findings repo produced a non-Reddit visit, 2026-09-24

**Trigger:** the 10:00am cycle on Wednesday 2026-09-24, 4 weeks after it shipped.
From 2026-08-27.

`github.com/projectunmuted/api-gotchas` went public on 08-27: verified technical
findings, each titled as the symptom somebody would search, each carrying a link
home. It is the first distribution artifact in this project that needs no account
of his and no attention of his, and `MONEY.md` ranks it first among the things
that can move with nobody.

**Widened 2026-08-28: this check now covers both repositories.**
`github.com/projectunmuted/nfl-preseason-vs-regular-season` went public this
morning, 798 NFL team-seasons as a CSV, and api-gotchas went from 4 findings to
6. Same test, same date, one check. Baseline for both is in `MEASURE.md` under
2026-08-28.

**The test, set the day it shipped:** one inbound visit that did not come from
Reddit. Baseline this morning, exit 0 on the raw table:
**detroitsportsreporter.com 21 page views in 7 days, project-unmuted.com 2, and
0 referrals from anywhere that is not Reddit ever recorded.**

**What to do:** `MSYS_NO_PATHCONV=1 python scripts/read_analytics.py --days 7`,
and check the referrer breakdown if the API exposes one. Write the number in
`MEASURE.md` next to the baseline above. Also re-run
`scripts/search_index_check.py`; a 2 stays a 2 and does not become a zero.

**What a zero means, decided now so a later cycle does not rationalise it:** a
zero at 4 weeks means a repository nothing links to does not get found either,
and that the GitHub surface is a slower route than `MONEY.md` currently ranks it.
That re-ranks the list rather than earning a defence of it. It does **not** mean
delete the repo; the marginal cost of it existing is zero.

**Ends when:** the number is in `MEASURE.md` with the date it was read.

### Standing: send a digest when something shipped, and check it has not lapsed

**Trigger:** any cycle that publishes an artifact, changes the plan, or ends a
week without him having heard anything. From 2026-08-28.

He asked for "some sort of notification process" on 2026-08-26 and
`scripts/notify.py` was built for it. **It then went 2 days without a single
digest ever being sent**, while 3 public artifacts shipped. A notification
channel nobody uses is the `ASK-HUMAN.md` failure in a new file: the tool
existed, so everyone assumed the problem was solved.

`python scripts/notify.py --digest --body-file <file>` opens an issue that
closes itself. It reaches him as email because the repo is his and the issue
@mentions him. **Do not use `--blocker` for these**; that one is only for the 4
things in `CYCLE.md` that may be asked of him.

**What a digest is for:** where the dollar stands, what shipped, what changed
about the plan, and what is still in his queue. One screen, no question at the
end. First one is issue #4, 2026-08-28, and it is the format to copy.

**What it is not for:** asking him anything. If a digest ends in a question it
should have been a blocker or, far more likely, a decision I should have made
myself.

**Ends when:** never.

### Standing: the published dataset gets regenerated before it is cited

**Trigger:** any cycle that quotes a number from
`github.com/projectunmuted/nfl-preseason-vs-regular-season`, or that changes
`scripts/preseason_full.py` or its cache. From 2026-08-28.

Everything in `datasets/` is generated by `scripts/export_dataset.py`, including
the README prose, so no number in it can drift from the CSV beside it.
`publish_dataset.py` runs `export_dataset.py --check` first and **refuses to
push** if the working copy does not match what the cache generates.

**What to do:** `python scripts/export_dataset.py && python
scripts/publish_dataset.py`, then verify over the network rather than on the
exit code, the way 08-28 did: fetch all 3 files from `raw.githubusercontent.com`
and compare the served CSV to the local one row by row.

**The one thing not to do:** do not hand-edit anything in `datasets/`. It is
build output, same contract as `docs_dsr/` and `findings/`. A hand-edit survives
until the next regeneration and then vanishes without a trace.

**It is a closed historical dataset**, so unlike every draft this project has
lost, it does not decay. 2025 is complete. The only thing that will ever change
it is adding the 2026 season once it finishes, which is a February 2027 job.

**Ends when:** never.

### Standing: findings get published, not just written up

**Trigger:** any cycle that finds and verifies a reusable technical defect,
meaning one that returned a 200 or an exit 0 while carrying a wrong answer.
From 2026-08-27.

The 4 in `findings/` sat inside `LOG.md` and journal entries for up to 15 days
before any of them was somewhere a stranger could find it. `LOG.md` is the
project's memory and it is not a distribution surface.

**What to do:** write it as `findings/<symptom-slug>.md`, titled as the symptom
somebody would type rather than as an essay, carrying the exact call, the exact
output, the date it was last reproduced, the cause, and the fix. Reproduce it
against a live call before publishing; 2 of the original 4 were, and one of them
turned out to still be broken upstream, which is what makes it worth reading.
Then `python scripts/publish_findings.py`.

**Ends when:** never.

### Write and publish the first Four Numbers column, Monday 2026-08-31

**Trigger:** the 10:00am cycle on Monday 2026-08-31, and every Monday after
that. From 2026-08-25. This is `PLAN.md` M2 and it is the only rung on that
ladder I can climb without him.

The instrument exists: `python scripts/four_numbers.py` pulls candidates for all
4 clubs from primary sources, prints the arithmetic, labels how fast each number
decays, and exits 2 on a partial read. Run it first, then write.

**What the column is:** one number for each of the Tigers, Lions, Pistons and
Red Wings, whatever the most interesting one is that week, published Monday
morning on Detroit Sports Reporter. It is **not** a recap of the prediction
record; that version broke the standing rule of 2026-08-09 and was replaced.

**The hard part, already priced.** On 2026-08-25 the script produced 5 live
candidates for the Tigers and 2 each for the Pistons and Red Wings, both of them
last season's closed numbers. Two of the four teams are dark until October, so
budget the time for the hockey and basketball numbers and expect to have to go
find them rather than read them off a standings page. The offseason scripts that
already exist are the place to start: `nhl_depth_scoring.py`,
`nba_opening_sos.py`, `nhl_schedule.py`.

**It needs a name.** "Four Numbers" is what the script is called, not a decision.
Pick one on the 31st and keep it forever; the whole return mechanism is that a
reader can bookmark a name and a day.

**Ends when:** the column has run 4 times. At that point `PLAN.md` M2's own test
applies: if nothing indicates a returning reader after 4 editions, the return
mechanism is wrong and comments or email are next.

### Standing: run `scripts/coverage_floor.py` at the top of every cycle

**Trigger:** every cycle, right after the series-preview check. From 2026-08-26.

The Lions floor was **4 days past due** this morning and nothing in the repo said
so. Last Lions analysis piece was 2026-08-15, the Lions have played preseason
games on 08-13 and 08-22 with a 3rd on 08-29, and the in-season floor is 7 days.
`CALENDAR.md` had a row for the 08-22 game and no cycle wrote anything about it.
Two of the last three floors in that file were met early and logged proudly,
which is exactly why nobody looked.

The floor was a rule with no instrument. Now there is one: it reads the `team:`
and `date:` frontmatter off every analysis entry, derives each club's season
state from the schedule endpoints rather than a hardcoded date, and applies 7
days in season or 14 out. Exit 0 all clear, exit 1 somebody is over, exit 2 the
season state could not be read.

Its offseason dates agree with `CALENDAR.md` independently: Wings Sep 1, Pistons
Sep 3. That agreement is the test that it encodes the written rule.

**One trap already found and fixed:** a symmetric 30 day window called the Red
Wings in season off a preseason game 26 days out, which would have silently
moved their floor from 14 days to 7. The window is 30 days back, 10 days
forward.

**What to do with an exit 1:** it does not automatically become the cycle's work.
The floor is a minimum, not a quota, and `CALENDAR.md` says a thin piece is worse
than a gap. Write the piece or log the miss, but do it deliberately rather than
by not noticing.

**Ends when:** never.

### Standing: do not try to read Reddit's rules pages again without a login

**Trigger:** any cycle tempted to have another go at `about/rules`. From
2026-08-20.

5 routes tried and logged in `MEASURE.md`: `old.reddit.com` (JavaScript shell,
no rule text in the bytes), the `.json` endpoint (403), the Wayback Machine (no
snapshot, and its availability API returned 429), 9 public mirrors (6 dead or
403), and a web search (which returns research papers about subreddit AI
policies, not the policies).

The 1 mirror that answered serves an Anubis proof of work challenge whose own
page text says it exists because of AI scrapers. **It is solvable in a few lines
and I am not solving it.** That is a standing decision, not an unfinished task.
Defeating an anti-bot gate aimed at exactly this is the kind of thing a reader
finding out about it would hold against everything else on the site, and mission
rule 3 already says a dollar that breaks a platform's rules is a loss.

**Ends when:** the human pastes the rules, or a Reddit credential exists. Both
are his, and the ask is in `ASK-HUMAN.md`.

### Standing: a finished draft that is not in `ASK-HUMAN.md` is not queued

**Trigger:** any cycle that writes a Reddit draft, and any cycle that reads
`drafts/POSTED.md` and finds a row under "Queued, not yet posted". From
2026-08-19.

`drafts/2026-08-14-lions-2008-followup.md` sat finished and unposted for **5
days** while `drafts/POSTED.md` recorded it as "queued". It was never in the
human's queue, so from his side it did not exist. Five days of the only channel
ever measured to send a reader here, idle, holding a post aimed at the one
subreddit of four known to allow this.

The posting model is draft, **he approves**, I post. The approval step lives in
`ASK-HUMAN.md` and nowhere else. A folder is not a queue.

**Ends when:** never. Every cycle, cross-check the "Queued, not yet posted"
section of `drafts/POSTED.md` against the Open section of `ASK-HUMAN.md`. If a
draft is in the first and not the second, put it in the second this cycle.

### Standing: never call search a channel again without re-measuring it

**Trigger:** any cycle about to write that search, SEO or IndexNow is working,
seeded, or bringing readers. From 2026-08-19.

`CYCLE.md` carried "search is seeded" for 11 days on the strength of IndexNow
returning 200. It means the submission was accepted. On 2026-08-19 the first
actual check found **zero pages from either domain** in any index, on 6 queries
with a passing control.

`scripts/search_index_check.py` holds the method. **It exits 2 from an
unattended cycle** because all 4 scriptable engines captcha this machine, and a
2 means the run proves nothing. Do not turn a 2 into a zero. Re-measure by hand,
or from a session with a search tool, roughly monthly, and only claim movement
with the control result printed next to it.

**Ends when:** a run finds one of our pages, at which point M3 in `PLAN.md` is
live and this becomes a monitoring item instead of a warning.

### Standing: a cycle that wakes into a gap says so, in writing, before anything else

**Trigger:** every cycle. Compare `git log -1 --date=iso` against the current
time. From 2026-08-24.

Nothing ran on this machine between 2026-08-21 06:56 and 2026-08-24 09:47. Six
scheduled cycles missed, 2 Detroit games unpicked, 1 grade 3 days late, and the
Royals draft expired in the folder. I only found the gap because I read the
commit dates carefully; nothing in the repo announces it, and a cycle has no
memory to notice with.

**What to do when the gap is more than about 14 hours:**

1. Grade every pending pick by `gamePk` before anything else, however old.
2. **Never backfill a pick on a game that has started.** Name the unpicked games
   under the table in `PICKS.md` instead, so the ledger shows the hole.
3. Check `drafts/` for anything that expired while the machine was down and mark
   it dead in `drafts/POSTED.md` rather than leaving it queued.
4. Say the gap out loud in the LOG entry with the 3 pieces of evidence that
   establish it: `logs/sync.log` (hourly, so it dates the outage precisely),
   `git log`, and `Get-ScheduledTaskInfo`.

**What not to do:** do not go looking for a Task Scheduler setting to fix. They
were checked on 2026-08-24 and are already right (`StartWhenAvailable` True,
`WakeToRun` True, `ExecutionTimeLimit` PT1H, `MultipleInstances` IgnoreNew).
`WakeToRun` does not power on a machine that is off, and `StartWhenAvailable`
catches up once, not six times. There is no config answer.

**Ends when:** never.

### Standing: prefer drafts that do not expire

**Trigger:** any cycle writing something for `drafts/`. From 2026-08-24.

A series preview is worthless after first pitch by construction, so it needs a
live machine *and* a same-day yes from him inside the same day. Those are 2
independent single points of failure and the Royals preview lost to both at
once.

**Sharpened 2026-08-25, after the second decay in 4 days.** "Does not expire" is
too soft to act on. Shelf life is a property of the subject and it is knowable
before you start writing:

| Subject type | Decays | Seen |
|---|---|---|
| Live season aggregate (run totals, ERA, save rate) | every night there is a game | the pythag draft lost its headline in 24 hours, 08-25; the Royals draft lost an ERA, 08-21 |
| Tonight's matchup | completely, at first pitch | the Royals preview died unread, 08-21 |
| Closed historical fact (finished seasons, completed samples) | never | the 2008 Lions backtest, 11 days queued, diffs to zero |

**Sharpened again 2026-08-27, after the same draft produced its 4th headline in
4 days.** "Prefer subjects that do not decay" is not the whole rule, because a
live subject usually contains **both a fragile version and a durable one, and
the fragile one is the one that looks like the headline.** The pythag draft led
3 times on Tampa Bay and Detroit having scored an identical number of runs, a
coincidence that broke every night. Sitting in the same script output the whole
time was Detroit's minus 12.1 Pythagorean residual, the largest in baseball
against a 2nd place of 7.2, which moves about a tenth of a win a night over a
133 game base. Same pull, same subject, one version keeps for hours and the
other for weeks.

So before writing: ask which number in the output has the biggest denominator
under it. Lead on that one. The coincidence can still be a sentence in the body.

**When the queue has room, write the closed historical fact.** Not because it is
more interesting, but because it survives an approval latency nobody controls.

Where there is still a choice inside a live subject, write the version with the
longer shelf life: a league-wide finding over a tonight-only one, a fact that can
be regenerated over one that dies. If a draft does have a decaying element, **write down in the
draft which sentence decays and the command that replaces it**, the way
`drafts/2026-08-24-pythag-extremes.md` does.

**Ends when:** never.

### Standing: render draft images from live pulls, not DATA blocks

**Trigger:** any cycle making a PNG for a draft. From 2026-08-24.

`scripts/make_series_image_kc.py` and its siblings hardcode a DATA block copied
out of a script run, which is exactly how the 08-21 draft ended up carrying an
ERA that had moved. `scripts/make_pythag_image.py` is the replacement pattern:
it pulls the standings, the margin splits and the bullpen lines from the API on
every render and prints every value it drew, so re-running it *is* the diff.

Copy that shape for the next one rather than the old one.

**Ends when:** never.

### Standing: re-pull a draft's numbers if it has waited more than a day

**Trigger:** any cycle that touches a draft in `drafts/` that was written more
than 24 hours ago, and the posting session itself. From 2026-08-21.

`drafts/2026-08-21-royals-tigers-series.md` was written on 08-20 saying Troy
Melton was at **1.71** over 84.1 innings. By the next morning he was at **1.49**
over the same 84.1 innings, without pitching: 2 of the 3 runs charged to him on
August 15 were rescored unearned, 16 earned became 14. A draft awaiting approval
is not a stored file, it is a set of claims drifting away from the data.

I only caught it because that morning's pick needed Melton's line anyway. That
is luck, not process.

**What to do:** every draft must name the command that regenerates its numbers,
near the top. Both current drafts now do. If the draft has waited more than a
day, run that command and diff before it goes up. Historical-season drafts (the
Lions backtest) will diff to zero and the rule still applies, because knowing the
diff is zero costs a minute.

**A published entry gets a correction note, never a silent edit.** The 08-20
series preview keeps its table as published with a dated note underneath.

**Ends when:** never.

### Every new request goes in two files, not one

**Trigger:** any cycle that records a reader request. Standing, from 2026-08-15.

`REQUESTS.md` is the prose record. **`requests.json` is what a reader sees**, via
`/requests.html` on Detroit Sports Reporter. A request that only lands in the
markdown is invisible to everybody outside this repository, which is the exact
failure the file already has a rule about.

`build.py` refuses to build if a row marked `answered` names an entry slug with
no file in `entries/`, so a bad slug fails loudly rather than shipping a link to
a 404. The guard runs before the output directories are wiped; that ordering was
wrong on the first attempt and is tested.

**Ends when:** never.

### A request is closed when it has a URL, not when the answer exists

**Trigger:** every cycle that touches `REQUESTS.md`. Standing.

**2026-08-15: the 2 outstanding requests both have URLs now**, so what remains
here is the standing rule rather than a backlog. See Done below. The only open
row in `REQUESTS.md` is the Cleveland one from 08-10, and the 4th item from the
Lions thread is a research question about preseason starter snap counts whose
data availability has never been checked.

Found 2026-08-14. Two requests from the Lions thread were marked "Delivered same
day" on 08-13. Delivered meant a script ran, a PNG landed in `scripts/`, and the
answer got typed into `REQUESTS.md`. **No reader could reach any of it**, and the
posting rules mean I never reply in the thread either, so from the asker's side
it is identical to being ignored. `MEASURE.md` carried "1 of 2 delivered" for
three days when the true figure was 0 of 4 published.

**Ends when:** never. No row in `REQUESTS.md` says Delivered without a URL.

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

### Any cycle reading analytics: a number without its sampleInterval is a rumour

**Trigger:** every cycle that runs `read_analytics.py` or writes a page-view
figure into `MEASURE.md`. Standing, from 2026-08-16.

Cloudflare's RUM dataset is **adaptive**: it silently picks a coarser, sampled
table based on the query, and at a 1-in-10 sample a day with single-digit views
returns **no row rather than a zero**. Two triggers are measured and both are
live:

1. **Window start older than about 7 days.** Not window length. A 5 day query
   starting 8 days ago is sampled too.
2. **Asking for `requestPath` as a dimension**, which drops a 7 day window to
   1 in 2 on its own. To ask about one page, **filter** on it with `--page` and
   it stays raw. `--page` needs `MSYS_NO_PATHCONV=1` on Git Bash or the leading
   slash becomes a Windows path; the script refuses rather than answering.

The script now chunks the window at the cliff, prints `[sampled, not a count]`
per affected day, and **exits 2** on a partial read. **Read the exit code.** A 2
means some of what you are looking at is scaled, and scaled numbers do not go in
`MEASURE.md` without the word sampled next to them.

**Ends when:** never. This is the analytics equivalent of the artifact check.

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

### The Anderson call has a follow-up worth writing, whichever way Tuesday goes

**Trigger:** after Anderson's next two or three starts, so roughly 2026-08-25.

**2026-08-17: the number moved.** Anderson threw 5 innings on 15 outs against
Chicago on 08-16, 21 batters faced, which beat the 14-out ceiling Pick 8 was
built on and cost that pick both its premises. That is 1 start, not a trend, and
the piece worth writing is still the third-time-through one. Re-run
`scripts/anderson_start.py --refresh` when the next 2 land.

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

### Done 2026-08-21: Pick 12 committed, `824072`

The 2:00am cycle Friday, as the item required. Kansas City had finally named all
3 starters, which is why this waited: Noah Cameron Friday, Wacha Saturday, Lynch
Sunday. `injury_check.py 824072` ran clean at exit 0. Riley Greene is still on
the 10-day and eligible **Saturday**, so he does not touch this game. Call is
Tigers win, Low, on Melton at 1.49 against a Cameron who is 5.17 at Kauffman and
3.33 on the road. Pushed before 8:10pm ET with hours to spare.

### Done 2026-08-21: confirmed nothing was owed a grade

Fetched by `gamePk`, not by name. `823342` was graded on 08-20 and is the most
recent Final Detroit game; `824072`, `824073` and `824071` are all Scheduled.
Detroit was off Thursday. Record unchanged at **7-4**.

### Done 2026-08-20: the Pistons floor, and the headline deflated on contact

**2 rows in this file were asking for the same thing**, one carrying the
Christmas-slight angle from the 08-12 sweep and one carrying the opening-4 angle
from the 08-16 sweep. Both are closed by the same piece.

Published `entries/2026-08-20-pistons-opening-four.md`. The sweep's hook was
real: Detroit's first 4 games of 2026-27 are Boston, at Miami, at Philadelphia,
at New York, and by opponent quality that is the 3rd toughest opening in the
league, in an exact 3 way tie with Philadelphia and Phoenix at .601 because all
3 sets of opponents won 197 games last year.

**And the 30 team correction did what the item warned it would.** Run the same 4
games through Detroit's own 60-22 with a home and road adjustment and it comes
out at 2.47 expected wins, which is the **9th easiest** opening in the NBA. So
the piece leads on the reversal rather than on the complaint: New York has the
hardest opening in the league partly *because* they play Detroit, and there are
Knicks fans posting our thread with our name in it.

The genuinely unfriendly part is travel, not opponents. 3 of the first 4 on the
road, which only 8 teams match and nobody exceeds, then 5 of the first 10 and 9
of the first 14.

New scripts: `scripts/nba_opening_sos.py` and `scripts/nba_opening_chart.py`,
both regenerating from ESPN's public JSON.

**Caught in review before publishing**, and worth recording because it is the
same class of error the item warned about: a first draft said Detroit had the
2nd best record in the league last season. San Antonio went 62-20. It is 3rd.

### Done 2026-08-20: grade Pick 11

`823342` fetched by id, status Final, Pirates 4 Tigers 3. The call was Pirates
win, so **the record is 7-4**. The grade is more interesting than the result:
Detroit chased Skenes in the 5th and led 3-2 into the bottom of the ninth, and
Kenley Jansen gave up 2 solo home runs. The entry's argument, a lineup missing 6
outfielders, did not happen. `entries/2026-08-20-grade-pick-11.md`.

### Done 2026-08-20: Kansas City series preview

Published a day and a half before the 8:10pm Friday opener rather than at the
10:00am cycle it was due. Opened on the finding, not on the previous preview.

The finding: **8 of the 10 Tigers-Royals games this season were decided by 1
run, the most of any of the 391 pairings in baseball**, and no pairing has
finished a full season above 7 since the balanced schedule arrived in 2023. Then
the correction that number needed, because a maximum over 391 pairings sits in
the tail by construction: 20,000 simulated leagues at the league's own one-run
rate produce a leader at 8 in 13 percent of seasons. Tail draw, not a miracle,
and the piece says so.

New script `scripts/tightest_matchup.py` does all 3 checks and emits the chart.
The live angle the item asked about: Riley Greene is still on the 10-day IL,
placed 08-12, **eligible 08-22**, which is Saturday. The Detroit News quote about
him rejoining on this road trip was cut from the piece because the article is
paywalled and it could not be verified from a primary source.
`entries/2026-08-20-royals-series-preview.md`.

### Done 2026-08-19: pick `823342`, Jobe vs Skenes

Committed at the 2:00am cycle on 08-19, roughly 10 hours before the 12:35pm ET
first pitch. `injury_check.py 823342` ran clean at exit 0 and its output is the
piece: 6 Detroit outfielders on the injured list. **The call is Pirates win,
Low**, which is only the 2nd time this board has taken the other side.
`entries/2026-08-19-pick-11-six-outfielders.md`.

The deferral was right. At 10 hours out there was time for a skeptic pass that
caught 6 factual errors and one omission (Ben Malgeri, active, .833 OPS) that
undercut the draft's own headline. At 2 hours out there would not have been.


### 2026-08-18: the Red Wings floor, taken 7 days before it was actually due

Published `entries/2026-08-18-red-wings-depth-scoring.md`, the second Wings piece.
Detroit's top 3 scorers put up 100 goals last season, 9th most in the NHL; the
other 26 skaters managed 139, 4th fewest and about 23 below the league's average
for non-stars. Built off the sub's own "with or without Larkin, Red Wings still
need to address offense" thread, which turned out to be checkable and right.
New tool: `scripts/nhl_depth_scoring.py`, which splits any team's season goals
into top-3 and everybody-else and ranks all 32.

**And the item that produced it was carrying a wrong date.** It said the floor
was overdue as of 2026-08-17. It was not. The Wings are out of season, the
out-of-season floor is 14 days, `CALENDAR.md` says the next Wings floor is
**Aug 25**, and this item had quietly applied the 7-day in-season figure. Two
cycles read "OVERDUE" and correctly deferred it for games, which means the wrong
date cost nothing this time. It could have cost a game cycle. **When this file
and `CALENDAR.md` disagree about a date, `CALENDAR.md` is the schedule.**

### 2026-08-18: the skeptic pass earned its keep, again, and harder than usual

The Wings draft went to the skeptic before publishing and came back with 4 hard
errors and 3 inference problems. The worst: the draft claimed Colorado's top-3
share was bigger than Detroit's, which is backwards (41.6 against 41.8, close to
identical), and that sentence was the load-bearing one in the section arguing
concentration is not the problem. Also caught: the piece said "84 games" for a
season that was 82, overstated the depth gap as "a couple of goals a week" when
it is about 23 goals a season, and never reconciled 241 team goals against 239
skater goals. All fixed before `build.py` ran. **The draft was internally
consistent and confidently wrong**, which is exactly what the pass exists for.

### 2026-08-17: Pick 8 graded 5-3, and the pick's own escape clause half-fired

`824236` Final on the id, White Sox 7 Tigers 5, so the White Sox call was
correct and the record is **5-3**. Published at
`/journal/2026-08-17-grade-pick-08.html`.

**Both of the pick's premises died and it collected anyway.** Drew Anderson
threw 5 innings on 15 outs, beating the 14-out ceiling the entry called his 2026
maximum across 42 appearances, and Sean Burke got 13 outs rather than the 6 or 7
innings his last-11 record implied. The entry's closing sentence was "If Anderson
goes 5 and Detroit's pen holds it, I'm wrong" and Anderson went 5. Detroit's pen
gave up 4 in 4 innings, and that is the only reason the pick won.

**What the grade found that outlives it:** Detroit has now scored 3, 5, 3 and 5
in 4 straight losses and is scoring **5.64 a game across all of August** against
a 4.56 season rate, with 4 outfielders on the injured list. The consensus that
the injuries silenced this offense is wrong on the numbers. The run prevention is
what broke. That finding became the spine of Pick 9.

### 2026-08-17: Pick 9 committed on `823343`, 9 hours early, and it is the first High on the board

`python scripts/injury_check.py 823343` ran clean at exit 0 and was read.
Pittsburgh posted Carmen Mlodzinski on Monday morning, which is what this item
was waiting for, so the pick went up rather than going blind.

**Tigers win, confidence High**, at
`/journal/2026-08-17-pick-09-two-different-pitchers.html`. That agrees with the
series preview's "Detroit takes 2 of 3", so there are no 2 calls contradicting
each other on the board.

**The finding, and it is the cleanest edge any pick has had here:**
Mlodzinski's 3.79 ERA is an average of two jobs. Split by role it is **2.15 in
16 relief outings and 5.47 in 11 starts**, on nearly identical innings, 50.1
against 49.1, with a 1.68 WHIP as a starter. He has cleared 6 innings **once**
in 11 starts, and since returning to the rotation on 08-07 he has thrown 5.1
innings for 9 earned runs. There is no injured-list stint behind the gap in his
starting log; Pittsburgh used him as a swingman all season.

**New tooling:** `scripts/start_lengths.py <playerId>` renders a start-by-start
innings chart plus the role split from the game log, `--table` for the markdown
version, exit 2 if the pitcher has no starts. Generated from the API on every
run, so the figure cannot drift from the prose.

**Two numbers were wrong in the draft and the verify pass caught both.** I had
written Miami as the 4th fewest runs in the NL (it is 6th) and Detroit's team ERA
as 6th in baseball (it is 4th). Both were plausible, neither was checked when
written, and both went into a piece whose entire value is that the numbers hold.
A third was cut rather than fixed: I had quoted AJ Hinch saying Detroit "couldn't
keep them in the ballpark", which I had completed by inference from a **truncated
Reddit headline**. The visible text stopped at "keep them i". That is a fabricated
quote from a real person and it came within one command of publishing.


### 2026-08-16: the page-view reader was one day inside a sampling cliff, and the requests page has never been loaded

Also retires **"Write and test the Cloudflare analytics reader"**, which had been
sitting in the live queue for days after being finished. Its own instruction not
to trust Cloudflare's field names from memory but to introspect the schema first
is what turned up `datetimeHour`, `requestPath` and `refererHost`, none of which
had ever been queried, and then the cliff underneath all of them.

**The defect.** `rumPageloadEventsAdaptiveGroups` is adaptive: Cloudflare picks a
coarser table from the query and does not say so unless asked. Measured minutes
apart on the same credentials, `--days 7` returns 6, 13, 16, 5, 6 across the last
five days and `--days 8` returns **08-12: 10 and nothing else**, exit code 0. The
boundary is sharp to the hour at 7 days back at UTC midnight, and it keys on the
window's **start**, not its length. At the 1-in-10 sample that follows, a day with
single-digit views has no retained event to scale and returns **no row rather
than a zero**. The old `--days 7` default sat one day inside it by luck.

**The fix**, both halves in `scripts/read_analytics.py`:

- **Chunked windows.** Slices cut at the cliff and anchored to the recent end, so
  the raw portion is never dragged onto the sampled table. Verified: `--days 14`
  now returns 08-12 through 08-16 byte-identical to `--days 7`, where before it
  returned a single row.
- **`avg{sampleInterval}` on every query.** Sampled days print `[sampled, not a
  count]`, degraded slices are named with their factor, and the run **exits 2**.

**The guard then caught a case I had not looked for, twenty minutes after it
existed.** Asking for `requestPath` as a *dimension* trips 1-in-2 sampling on a
window that is raw without it, so the cliff is about cardinality too. My first
draft of the finding below was read off that sampled table. Filtering with the
new `--page` instead keeps it raw.

**What it then measured**, all unsampled and with controls:

- **`/requests.html`: 0 views since it went up on 08-15.** Both sites.
  `/picks.html` likewise 0. Control `/about.html` returns 1 and 2, so the query
  works and the pages have no readers. `PLAN.md` has been carrying the requests
  page as the favourite route's first step; the step has an audience of nobody.
- **The 08-13 Lions post's famous 3 page views is an upper bound.** Hourly: the
  3 arrived one per hour at 5pm, 6pm and 7pm ET around a 7:00pm post, then 0 for
  11 hours. No spike. The hours through 10am sum to exactly the 10 that was
  written down at post time, which does confirm the baseline discipline recorded
  what it claimed.
- **The 08-14 preview, recorded as permanently unknowable, is 3 to 5.**
  Reconstructed with no baseline. 10 of that day's 16 landed in the 9:00am ET
  hour, long before the post.

**A human dependency shrank rather than closed.** The `ASK-HUMAN.md` item asking
him to record a baseline at post time every time is now "tell me the day, within
a week," because hourly reconstruction does the rest and the raw table only
reaches back 7 days.

Also new and worth carrying: `--page` needs `MSYS_NO_PATHCONV=1` on Git Bash or
the leading slash is rewritten into a Windows path and the query returns a
truthful zero about a path that does not exist. Caught doing exactly that; the
script now refuses a page argument that does not start with `/` rather than
answering it. Published at
`/journal/2026-08-16-the-instrument-was-sampling.html`.

### 2026-08-16: the Pittsburgh series preview, and it deflated this project's own calling card

`entries/2026-08-16-pirates-series-preview.md`, published Sunday morning, well
inside Monday's 7:05pm first pitch. `PIT` added to `OPPS` in `series_preview.py`,
which it was missing as predicted. Opened on the finding rather than on the
previous preview's grade, per the rule.

What came of it:

- **Detroit is 10.7 wins below its Pythagorean expectation, the largest shortfall
  in baseball. Pittsburgh is 4.8 below, the largest in the National League.** Two
  clubs on 60 wins, 15.5 wins short between them, meeting for the first time this
  season.
- **Then the number died.** 20,000 simulated leagues where every club is by
  construction exactly as good as its run differential says: **a shortfall at
  least as big as Detroit's appears in 55 percent of them**, and 5.7 clubs a
  season land at or below Pittsburgh's 4.8. The minimum of 30 draws sits about 2
  standard deviations out because that is what taking a minimum does.
- **What survives is the shape.** Detroit 12-21 in 1-run games, 2nd worst in
  baseball, and 31-17 at 4-plus, 5th best. Pittsburgh has a *winning* 1-run
  record at 17-14 and is 10-24 in games decided by 2 or 3, the worst in baseball,
  which the same simulation then deflates too at 13 percent. Mirror-image clubs:
  Pittsburgh 3rd in runs scored and 24th in runs allowed, Detroit 12th and 5th.
- **The call: Detroit takes 2 of 3.** Wednesday is Skenes at 12:35pm against a
  lineup missing 4 outfielders.

New tooling: `scripts/underperformers.py` derives every prose number, the ranked
30-club dot plot and both simulations in one run. Two things worth carrying
forward. The `hydrate=record(type=[home,away])` form on `/teams` returns an empty
`splitRecords` for this season, so home and road records are counted off the
schedule feed with the same postponed-game guard as everything else. And the
all-30 margin buckets are cached at `logs/margin-buckets.json` **with no
expiry**, which is a stale-number trap of exactly the kind this repo keeps paying
for; the item above says to delete it to refresh.

**No draft was written for `drafts/`.** The item asked for one, and the reason it
is not there is the 1-post-a-day cap plus the 08-14 Lions follow-up still sitting
queued and unposted. Writing a third unposted draft would have been queueing work
for a human rather than doing any, and the same cycle's process entry argues that
the posts that matter are the ones people argue with, which is a claim the queued
Lions follow-up tests directly. If he posts that one and wants a Pittsburgh
draft after it, it is a `reddit-summarizer` run off a published entry.

### 2026-08-15: both outstanding reader requests published, and the answer embarrassed the question

`entries/2026-08-15-lions-scatter-and-histogram.md`, one entry carrying both
charts, because both came out of the same thread on the same afternoon. The item
said a request is not closed until it has a URL. Both have one now, and
`REQUESTS.md` is restructured so nothing marked published is sitting under Open,
which it was for 3 blocks including the 08-14 one.

What came of it, beyond the URLs:

- **The scatter reran on the corrected cache** (`preseason_cache_2000.json`),
  which moves 2001 from 2.5-13.5 to 2-13 and takes the reader's 20 seasons to
  **25**. Correlation **+0.285**, r squared 8.1%, against +0.20 and 3.9% on the
  old 19-season version and +.106 league wide.
- **That higher number is nothing, and the piece kills it in the paragraph after
  reporting it.** A permutation test, 20,000 shuffles on a fixed seed, produces a
  correlation at least that strong **17.1%** of the time. About 1 in 6.
- **The finding is the leave-one-out.** Without 2008 r goes to **+0.514**;
  without 2011 it falls to +0.222. The thread spent Thursday demanding 2008 be
  included, and 2008 turns out to be the single dot doing the most work to prove
  the thread's own point. The entry says you do not get to drop the inconvenient
  dot, so the answer stands at +0.28.
- **The histogram is 68 teams of 798**, not 39 of 320, and the shape does not
  move: 45.6% of the undefeated group won 9 or more per 17 against 46.9% of
  everybody, raw totals 0 to 14, no cluster.

Two tooling notes worth carrying. `undefeated_preseason_hist.py` grew `--svg` and
`--cache` rather than being forked, and its caveat line ("bars are 1 to 7 teams")
was **stale**: it had been written down when the sample was 39 and never updated
when it became 68. It is derived from the data now. That is the same failure
class as the `MEASURE.md` denominator and the 2015 window, three times in a week:
a sentence describing data, written once, then trusted.

### 2026-08-15: Pick 6 graded 4-2, and Pick 7 committed 11 hours early

`824237` Final on the id, **White Sox 9, Tigers 5**, note at
`/journal/2026-08-15-grade-pick-06.html`. `824239` has its row, Tigers, Low,
committed at 2:00am against a 1:10pm first pitch, which is the margin the item
asked for.

All 3 things the item asked the grade to check came back, and 2 of them cut
against the entry:

- **Jobe and the third time through.** The entry said nobody would let him see a
  lineup a 3rd time. He faced **23 hitters in 3.2 innings**, which is 5 batters
  into a third trip, and it happened in the 4th because Chicago kept hitting.
  The mechanism was backwards: a manager's decision was never involved.
- **Newcomb as an opener.** Right. 1.1 innings, 5 hitters, 25 pitches, and
  Chicago's pen threw 7.2 of the 9.
- **Which pen breaks.** Detroit's threw 5.1 and gave up 3, Chicago's threw 7.2
  and gave up 5, so the entry's closing claim was correct per inning and
  irrelevant, because both arrived after 6-3.
- **The stated fear did not arrive.** The entry named the 12-20 record in 1-run
  games as the danger. Final 9-5. Second straight game where that fear was named
  and the game was not close.

`injury_check.py 824239` ran before the pick, exit 0. New this cycle: Chicago put
**Davis Martin on the 15-day** with a blister and claimed **Jake Rogers** off
waivers from Boston.

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
