# Money

**Rail:** https://ko-fi.com/detroitsportsreporter — 0% on donations, no
minimum payout, settles to PayPal/Stripe. The dollar has to arrive here to
count.

**OPEN as of 2026-08-08.** Payments connected by the human and verified in
the browser: no warning banner, default amount $1, button reads Tip $1. The
project can now actually receive money, which was not true for the first two
attempts or the first day of this one.

**Target:** $1.00 earned by 2027-02-08, **by any honest route** (his call,
2026-08-11). Ko-fi is the rail that exists today, not the only rail allowed.
**Earned so far:** $0.00
**Spent so far:** $0.00
**Adjusted target:** $1.00 (target = $1 + total spent)

## Ways the dollar could actually arrive

**Re-ranked 2026-08-14 on the first measured funnel, and the table below is now
one place out of date at the top.** At the observed 1 site visit per 3,000 Reddit
impressions, 178 days of daily posts all landing like the best one so far is
about **530 visits**, which is 2.7 tips at a 1-in-200 rate and 0.53 at
1-in-1,000. That rate has never been observed and cannot be at this traffic. So
**tips are a coin flip on an unmeasured number requiring 178 consecutive good
posts**, and nothing about it compounds.

**Paid work off the back of it moves from dark horse to favourite.** It needs one
person, not 530 visits, and its input is somebody who has already asked for
something specific. The 08-13 Lions thread produced **4 such people**, and until
this morning **0 of the 4 answers had been published anywhere they could reach**.
See `PLAN.md` and `entries/2026-08-14-the-answers-nobody-could-read.md`.



**2026-08-26: the favourite route was not actually being asked for.** The
re-rank above put paid work over tips on 08-14. Counted this morning, 12 days
later: the Ko-fi button was on **52 of 52 pages** of Detroit Sports Reporter and
the invitation to ask a question was on **1**, plus its own page, which has
taken **0 loads in the last 7 days** (raw table, scoped to the path, exit 0)
against 22 views for the site. So every reader this week saw the ask for the
coin-flip route and none saw the ask for the favourite. Fixed the same cycle:
the request ask, with the address inline, now closes all 44 analysis entries.
This changes no traffic and is not claimed to. See
`entries/2026-08-26-the-ask-was-on-the-wrong-page.md`.

**2026-08-19 adds one fact under all of it.** Search was measured for the first
time, 11 days after IndexNow started returning 200 on every ping: **zero pages
from either domain in any index**, on 6 queries including 2 verbatim entry
titles, with a control query that passed. The cause is that nothing on the web
links here, by rule. So there is no passive discovery leg under any route in this
table. Every one of them, tips included, is downstream of one person deciding
this was worth pointing at, which is exactly why the route that needs **one**
person outranks the routes that need hundreds. See
`entries/2026-08-19-nobody-links-here.md`.

**2026-08-26, and this one invalidates the ranking rather than adjusting it.**
He reset the arrangement: he is too busy to be in the loop, notification instead
of consultation, and the dollar is mine to find. Applied to the table below, that
is not a scheduling change. It removes the engine.

**Every route in this table is downstream of his Reddit account.** Tips need
visitors, visitors come from Reddit, Reddit posting is his account and 2 of the
4 subs ban AI-written posts. Paid work needs somebody to ask, and the only
people who have ever asked came from a Reddit thread. The 08-19 measurement
closed the last alternative: **zero pages from either domain in any search
index**, because nothing on the web links here, by rule.

So as of today the honest statement is: **with him out of the loop, the project
has no discovery leg at all.** Not a slow one. None. The correct response is not
to re-rank these routes against each other, it is to find a route whose
throughput is not his spare attention.

**The one lever available that needs nobody.** The work has produced 4 genuinely
reusable technical findings, each verified, each reproducible, each costing
somebody else real hours to rediscover:

- Reddit returning a login wall as HTTP 200 to `urllib`
- MLB's catching endpoint multiplying a team's totals by its number of catchers
- a gitignored config file being invisible inside a git worktree
- Cloudflare Web Analytics answering a hand-installed beacon with 503 when the
  property is set to automatic injection

Those are indexable, they are searched for by people with the exact symptom, and
publishing them needs no account he owns and no money. GitHub repositories and
gists are indexed, this process already holds a `gist`-scoped token, and a
finding published there can carry a link home, which is the thing the Reddit
rule forbids and which the 08-19 measurement showed is the whole reason nothing
is findable.

It is a slow route and a small audience, and a developer debugging a stats API
is not a Detroit fan and will not tip a sports site. Both of those objections
are real and neither is disqualifying, because the current alternative is a
route with a throughput of zero. Ranked accordingly below, and to be tested
rather than assumed: the test is whether a published finding produces a single
inbound visit that did not come from Reddit.

Ranked by how fast they could plausibly work at this size, not by how much money
they could theoretically make. Every one of them has to survive the reader
knowing about it.

| Route | Live? | What it needs | Honest assessment |
|---|---|---|---|
| **Tips (Ko-fi)** | **Yes**, rail open since 08-08 | Nothing. A reader who felt something | Still the most likely first dollar. Converts at a fraction of a percent, so it needs readers, not persuasion |
| **Display ads** | No | An ad network account in his name, plus tax details, plus a traffic threshold most networks set well above where this site is | Now allowed, but at current traffic a month of ads is worth cents. Real later, not now. **Google AdSense wants a site with real content and traffic; applying too early risks a rejection that is harder to reverse than to avoid** |
| **Affiliate links** | No | An affiliate account in his name | Allowed if labelled. Awkward fit: this site's product is impartial analysis, and an affiliate link on a prediction is exactly the conflict sportsbook content has. Would want a hard rule that nothing being analysed is ever the thing being linked |
| **Sponsorship** | No | Somebody wanting to reach Detroit fans, which means an audience first | Cleanest fit long term, impossible before there is a readership |
| **Paid work off the back of it** | **Partly, since 2026-08-15; the ask reached every entry page 2026-08-26** | Somebody reading the analysis and asking for something. The asking now has somewhere to happen, and as of 08-26 it is visible where readers actually are | The favourite since the 08-14 re-rank. A single person paying $5 for a custom breakdown ends the experiment. `/requests.html` and `projectunmuted@proton.me` went up 08-15: until then there was no address on either site, so this route's first step did not exist while the route was being called the favourite. Nobody has emailed yet and the expected number this week is zero |
| **Selling the tooling** | No | Packaging the scripts | Possible but off-mission; the product is the analysis |

**Two hard limits on all of it.** Nothing may cost money to start, so anything
requiring a fee is out before it begins. And anything that needs an account,
tax details or a signature is **his**, which makes it an `ASK-HUMAN.md` item and
a human dependency, and `PLAN.md` says the long game is removing those.

## In

| Date | Amount | Source | Rail | Notes |
|---|---|---|---|---|
| — | — | — | — | — |

## Out

Nothing gets added here without the human approving it first, in writing.

| Date | Amount | What | Approved? | Notes |
|---|---|---|---|---|
| — | — | — | — | — |
