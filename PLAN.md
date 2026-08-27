# The road to a dollar

Written 2026-08-10, because he asked whether one existed and the honest answer
was "not really." `BETS.md` had a hypothesis and a kill date; `MONEY.md` had a
target. Nothing described the ground between publishing a piece and a stranger
tipping.

**This file is the ladder. `BETS.md` is why we think the ladder leans against
the right wall.** If a rung fails, the failure is recorded here and the bet gets
re-examined there.

---

## The one thing that was missing: a number

Before today, **nobody knew how many people had read either site.** Not "a small
number" — no number at all. Search Console has been verified since 2026-08-08
and has never been read. Ko-fi shows tips. Reddit shows upvotes.

That gap makes the whole bet unfalsifiable. If no dollar arrives by November, the
diagnosis splits three ways and they need completely different responses:

- **Nobody saw it.** Distribution problem. The work might be fine.
- **People saw it and did not come back.** Product problem.
- **People came back and did not tip.** Monetisation problem, and the cheapest
  fix is asking better rather than writing more.

Measuring first is not bureaucracy. It is the difference between a project that
learns and a project that guesses.

---

## Milestones

Each one has a date, a test that can fail, and what it changes if it does.

### M0 — Know the number  ·  by 2026-08-17

**Test:** a `MEASURE.md` in this repo, updated by the 10:00am cycle, carrying
search impressions and clicks, Reddit post performance, and Ko-fi state, each
with the date it was read.

**Why first:** everything below is unreadable without it.

**Status 2026-08-12:** `MEASURE.md` exists and is updated every morning cycle,
so the *file* half is done. The *numbers* half restarted from zero this morning,
and the reason is worth recording here rather than only in the journal.

**Page views were recorded as collecting for two days while collecting nothing.**
The human turned Cloudflare Web Analytics on the evening of 08-10 and pasted both
beacon tokens. `.analytics.json` is gitignored; cycles build inside
`.claude/worktrees/`; a gitignored file does not exist in a worktree. `build.py`
found no tokens, emitted no beacon, exited 0, and shipped. Three cycles then read
the previous cycle's note and wrote "beacon live" again with a larger hour count.
Caught 08-12 by fetching the live homepages. Fixed in `build.py`, guarded by
`scripts/check_live.py`, written up at
`/journal/2026-08-12-the-beacon-that-was-never-there.html`.

**So this rung was not blocked on him. It was broken here.** That matters for how
the ladder gets read: a milestone sitting still is not evidence of a human
dependency until the machine half has been checked against the artifact.

**Blocked on, honestly:** Search Console has no unauthenticated API, so either he
pastes the numbers weekly or he creates a service account. Cloudflare page views
are now collecting and readable in his dashboard; the queued ask is a read-scoped
API token so a cycle reads them unattended. Both in `ASK-HUMAN.md`.

**Fails if:** a week passes and the number is still unknown. Then the honest
move is to say so on the journal rather than pretend the project is progressing.
Two of the nine days were spent on the failure above, which is the project's own
fault and should be counted against it rather than against him.

**Status 2026-08-14, 10:00am: M0 is effectively met, and the first thing it
measured reorders the rungs below it.** Page views are read by a script into
`MEASURE.md` every morning cycle. The first distribution event ever measured
converts at **1 site visit per 3,000 Reddit impressions**.

Run that forward, which nobody had: **178 days** to the deadline, 1 post a day at
the cap, all of them landing like the best one so far, is 1.6 million impressions
and about **530 visits**. At a 1-in-200 tip rate that is 2.7 tips; at 1-in-1,000
it is 0.53. **The visit-to-tip rate has never been observed and cannot be at this
traffic**, so the tips route is a coin flip on an unmeasured number, requiring 178
consecutive good posts, with nothing about it compounding.

What that does to this ladder: **M1 is a means, not the goal, and the "paid work"
route in `MONEY.md` moves from dark horse to favourite.** It needs one person
rather than 530 visits, and its input is somebody who has already asked for
something specific. On 08-13 there were **4 of those in a single thread**, and as
of this morning **0 of the 4 had been published anywhere a reader could reach**.
That is a bigger miss than any traffic number in this file.

**Status 2026-08-15, 10:00am: the favourite route's first step existed only in
this file.** M0 promoted "somebody pays for a specific breakdown" over tips,
because it needs 1 person rather than 530 visits and its input is a reader
asking a question. Neither site had anywhere for a reader to ask. No address, no
form, no invitation, while every page carried a Ko-fi button for the route this
file calls a coin flip.

`/requests.html` closes it: the ask, the 4 already-answered questions with links
to where the answers went, and the open ones listed as open, all generated from
`requests.json` with a build guard that refuses an answered row whose entry does
not exist. Written up at `/journal/2026-08-15-no-way-to-ask.html`.

**What it does not do**, recorded so a later cycle does not read this as a win:
it creates no readers, it does not reach the 4 people who already asked, and it
adds a human dependency, because the inbox needs a login I do not have. The
claim is one step of three, not the route.

**Status 2026-08-16, second cycle: M0's instrument was degrading silently, and
fixing it made two of this ladder's load-bearing numbers softer.**

M0 says a milestone marked done without a number beside it is not done. The
corollary nobody wrote down is that a number is only as good as the instrument,
and this one had a cliff in it. Cloudflare's RUM API drops to a **1-in-10
sample** when a query starts more than about 7 days back, and at that resolution
a quiet day returns **no row rather than a zero**. `read_analytics.py` defaulted
to `--days 7`, one day inside the boundary. Every figure in `MEASURE.md` is
right by accident. Fixed by chunking and by reading `sampleInterval`; a partial
read now exits 2. `/journal/2026-08-16-the-instrument-was-sampling.html`.

Two things on this ladder move as a result, both downward:

- **The conversion figure under the 08-14 re-rank is an upper bound.** Hourly
  buckets show the 08-13 post's 3 page views arriving one an hour at 5pm, 6pm and
  7pm ET around a 7:00pm post, then nothing for 11 hours. There is no spike in
  the data. "1 visit per 3,000 impressions" is the most generous reading
  consistent with it, and the arithmetic above that already made tips a coin
  flip gets worse, not better. The 08-14 preview, previously unmeasurable, comes
  in at 3 to 5 by the same method, so the two agree and neither is encouraging.
- **The 08-15 claim above needs correcting.** It says `/requests.html` closes the
  favourite route's first step. The page has been loaded **zero times** since it
  was published, verified unsampled against a working control. Publishing the ask
  is not the same as opening the route: the route needs a reader to arrive,
  notice, and ask, and only the first of those is even attempted today.

**What does not change:** the direction. The re-rank put paid work above tips
because tips need traffic that does not exist, and everything here makes the
traffic thinner. The re-rank was right and is now better evidenced.

**Status 2026-08-26: the 08-16 correction above was still true 10 days later,
and the reason was structural.** That note says publishing `/requests.html` is
not the same as opening the route, because the route needs a reader to arrive,
notice, and ask. Checked this morning, the "notice" step was not attempted
anywhere a reader actually goes: **the Ko-fi button was on 52 of 52 pages and
the request ask was on 1**, the homepage. `/requests.html` has taken **0 loads
in the last 7 days**, scoped to the path on the raw table at exit 0, against 22
page views for the site as a whole.

So for 12 days after the re-rank made paid work the favourite, the site asked
every single reader for the coin flip and none of them for the favourite. The
plan changed and nothing downstream of it did. **A re-ranked plan is not
implemented until you can point at the artifact that changed**, which is the
08-12 beacon lesson arriving from a different direction.

Shipped the same cycle: the ask, address inline, at the end of all **44**
analysis entries. What that is worth is small and should be recorded as small.
It creates no readers, and 22 page views a week times any conversion rate is
still about zero emails. It moves the first step of the favourite route from
structurally impossible to merely unlikely.

### M1 — One hundred humans  ·  by 2026-09-07

**Test:** a single piece drawing 100+ real readers, from any source, evidenced
by a number rather than a feeling.

**How, based on what actually worked:** the Tigers post drew 26 upvotes and 22
comments on a fan sub. That is the channel. One post a day maximum across all
four teams, best piece only, posted when he can answer comments.

**Fails if:** four weeks of posts and no piece clears 100. Then the writing is
not landing with fans and the next move is reading the comments on what did
land, not writing more of what did not.

### M2 — A reason to come back  ·  by 2026-09-21

**Test:** a named recurring column at a fixed time, plus evidence somebody
returned for it: a repeat commenter, an RSS subscriber, a "looking forward to
this week's" reply.

**Why this shape:** the research pass found that the single strongest
free return mechanism at small scale is a named column on a known day.
Readers bookmark "The Weekly Ledger", not a site.

**Candidate, replaced 2026-08-25.** It used to read "the weekly ledger of what
the calls got right and wrong, Monday morning." That column is forbidden by his
standing rule of 2026-08-09: never write about the record, the grading
discipline, or how honest the site is. The plan had a milestone in it that broke
a rule, unnoticed since it was written.

The mechanism M2 needs is the **fixed day and the name**. The subject was never
the point. So: a Monday column carrying **one number for each of the four
teams**, whatever the most interesting one is that week. Same return mechanism,
no self-congratulation, and it forces coverage across all 4 teams in a project
where 33 of 40 analysis pieces are Tigers pieces while the Lions sub is the only
channel ever measured to send a reader.

**Instrument built 2026-08-25, 10:00am cycle.** `scripts/four_numbers.py`
pulls every candidate number for all 4 clubs from primary sources in one run
(MLB Stats API for the Tigers, ESPN public JSON for the other 3), prints the
arithmetic beside each value, and labels how fast each one decays, because a
column published Monday carrying a number that moved Sunday night is the
drafts-folder failure with a schedule attached. Exit 2 on a partial read, same
contract as `injury_check.py`.

The first run found a defect worth having: **ESPN's team endpoint `nextEvent`
was stale**, still pointing at a Lions game that had finished 3 days earlier.
The script now walks the schedule endpoint instead and warns when the two
disagree.

It also priced the real difficulty. Today it produces **5 live candidates for
the Tigers and 2 each for the Pistons and Red Wings**, and both of those are
last season's closed numbers. Two of the four teams are dark until October, so
the column's hard part is not the Tigers number, it is finding something worth
reading about a club that has not played since spring.

**Still to do:** the column itself, its name, and the first edition. Nothing is
published yet, so this rung is not climbed. First edition Monday 2026-08-31.

**Fails if:** the column runs four times and nothing indicates a returning
reader. Then the return mechanism is wrong and comments or email are next.

### M3 — Findable without being shared  ·  by 2026-10-12

**Reordered 2026-08-19: M3 is downstream of M4, not parallel to it.** The first
check of whether either site is actually in a search index, 11 days after
IndexNow started returning 200, found **zero pages from either domain** on 6
queries with a passing control, including verbatim entry titles. The mechanism
is not the content and not the markup: `robots.txt` allows everything, both
sitemaps serve, there is no stray `noindex`. It is that **nothing on the open
web links here**, by rule, since Reddit posts never link the site. Submission
without a citation is a request to be crawled with no reason to be trusted.

So this rung cannot be climbed before M4 below, which is dated four weeks
later. Do not spend a cycle on search until something points here. Method and
evidence: `scripts/search_index_check.py`,
`/journal/2026-08-19-nobody-links-here.html`.

**Test:** non-zero clicks from search on a query that is not the site's name.

**Where it is winnable:** methodology questions nobody owns. "Does preseason
record predict the regular season." "How much of a close-game record is luck."
Low volume, evergreen, and the SERPs have no incumbent. Game-prediction queries
are 100% sportsbook inventory and are not worth attempting.

**Fails if:** October ends with zero non-brand search clicks. That is not a
crisis; organic search on a two-month-old domain is expected to be slow. It
just means search is not the path to the dollar and effort belongs elsewhere.

### M4 — Somebody else points at it  ·  by 2026-11-08

**Test:** one inbound link or citation from anywhere with its own audience: a
newsletter, a beat writer, another blog, a Reddit thread started by someone else.

**Why it matters more than rankings:** authority is the thing a new domain
cannot manufacture, and one citation is worth more than a month of publishing.
**As of 2026-08-19 this is also the gate on M3**, so it is the earlier
milestone in practice whatever the dates say.

Does not count: the GitHub repository homepage fields, set 2026-08-19 on both
repos because they were the only inbound link surface reachable without his
login. Verified rendered, and GitHub marks them `rel="nofollow"`. That is a
crawl path, not an audience pointing at anything.

**Also does not count, recorded 2026-08-27 the day it shipped so nobody reads it
as progress on this rung:** `github.com/projectunmuted/api-gotchas`, 4 verified
technical findings published as their own public repository. Its README links
home and those links are `rel="nofollow"` too, checked in the rendered bytes. It
is the first artifact this project has built that needs nobody's account and
nobody's attention, which is why it exists, but it is a second crawl path on a
high-authority domain and not a citation. This rung still wants somebody with an
audience choosing to point here.

**Fails if:** nothing by the `BETS.md` kill date. Combined with M1 through M3,
that is the evidence to kill or reshape Bet 1 rather than let it drift.

### M5 — The dollar  ·  by 2027-02-08

**Test:** $1.00 earned, by any honest route (his call 2026-08-11). Ko-fi is the
open rail, but ad revenue, a sponsorship or somebody paying for work all count.
See `MONEY.md` for the routes and what each would need.

**The unglamorous part nobody plans:** the tip has to be *asked for*, in the
right place, at the moment something was worth it. Right now the ask is a block
at the bottom of a page. If M1 and M2 land and no tip follows, the experiment
to run is the ask itself, not more writing.

---

## Where visitors actually come from

His question, and the right one: milestones are worthless without a mechanism.
Static pages on GitHub Pages produce **no server logs at all**, so both halves
need solving: counting visits, and causing them.

### Counting them

- **Cloudflare Web Analytics**, free, no cookie, one script tag. It works on any
  host including GitHub Pages, and his Cloudflare account already exists because
  project-unmuted.com's DNS lives there. This is the only piece that gives real
  page views. Needs a token from the dashboard: two minutes, queued for him.
- **Search Console** for impressions and clicks, already verified, unread.
- **Reddit** post score and comment count, readable by any cycle once the API
  credentials land.
- **Ko-fi** for the only number that ends the experiment.

### Causing them, in order of what is actually proven

**1. Reddit, the fan subs. Proven, and currently the whole game.**
The one post so far drew 26 upvotes and 22 comments in six hours. Nothing else
has produced a single reader. One post a day maximum across all four teams,
posted when he can answer comments, best piece only. Expected order of
magnitude per good post: tens to low hundreds of readers, not thousands.

**2. Comments, not posts.** Underrated and unused so far. A specific number
dropped into somebody else's thread ("they are 11-18 inside the division, which
is the part that worries me") earns more credibility per unit of effort than a
post, cannot be read as self-promotion, and drives profile visits, which is
where the site link lives. This is the cheapest untapped channel and it is his
hands, since it is his account.

**3. Being cited by someone with an audience.** One link from a newsletter or a
beat writer outweighs a month of publishing, because authority is the thing a
new domain cannot manufacture. The realistic version: reply to a beat writer's
post with an original number, repeatedly, until the number gets quoted.

**4. Search. Measured 2026-08-19 and currently carrying nothing.** Not slow,
*stalled*: zero pages from either domain in any index reachable from here, 11
days after IndexNow accepted every URL, on 6 queries with a passing control. The
cause is a link profile of zero, which is a direct consequence of item 3 not
having happened yet. Still real, still a compounding asset for next spring, but
it is **downstream of item 3 rather than an alternative to it**, and no cycle
should spend itself on search until something points here.

**5. Sharing.** Every link now renders a proper share card, which was broken
until today. This does not create readers on its own; it stops the ones you
have from bouncing off a grey box.

### The weekly rhythm this implies

- Every day: publish what the calendar demands, grade what finished.
- **One** Reddit post on the best thing that week, timed to a game, when he is
  around.
- Several comments on other people's threads, carrying a real number.
- One evergreen methodology piece a week, for the slow search compounding.
- Read what came back. Reader objections outrank anything picked unprompted.

### The honest expectation

At this size the arithmetic is unforgiving: a good Reddit post is tens of
readers, a great one is a few hundred, and tips convert at a fraction of a
percent. **The dollar most likely arrives from one reader who felt something,
not from traffic volume.** That argues for depth and for the ask being in the
right place, not for publishing more.

## What gets published, and when

`CALENDAR.md` holds the posting plan the milestones above assume: games decide
priority, a floor keeps every team present, and dormant teams get offseason
shapes rather than silence. Written 2026-08-11 after 12 pieces produced nothing
at all about the Red Wings.

## What is deliberately not on this ladder

- **Paid subscriptions and memberships.** Recurring value from a site this
  young is a different project. **Ads are no longer excluded** (his correction
  2026-08-11), they are just worth close to nothing until there is traffic, so
  they sit behind M1 rather than being a route to it.
- **Covering all four teams evenly.** Coverage is not an obligation. Depth on
  whichever team is live beats breadth nobody asked for.
- **Volume.** Publishing more was tried on 2026-08-09: three Tigers pieces in a
  day, and the extra two did nothing. Two cycles a day now, one post a day
  maximum.
- **An email list, for now.** Effective, per the research, but it needs a
  service and therefore a spend decision that is his and has not been made.

---

## How this file gets used

Read it at the start of any cycle choosing what to build. Update the milestone
you moved, with the evidence and the date. **A milestone marked done without a
number beside it is not done.** If one fails, write why here and open the
question in `BETS.md`, because a failed rung is information about the bet.
