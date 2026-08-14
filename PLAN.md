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

**Candidate:** the weekly ledger of what the calls got right and wrong, Monday
morning. It is the product's own argument, restated on a schedule.

**Fails if:** the column runs four times and nothing indicates a returning
reader. Then the return mechanism is wrong and comments or email are next.

### M3 — Findable without being shared  ·  by 2026-10-12

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

**4. Search.** Real but slow. Six to twelve months on a domain this age, and
only on methodology queries with no incumbent. Not a plan for this autumn; a
compounding asset for next spring.

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
