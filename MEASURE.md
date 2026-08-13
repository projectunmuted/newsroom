# The instrument panel

`PLAN.md` milestone M0. Every line carries the date it was read, because a
number without a date is a rumour. Newest at top.

**A blank is not a zero.** If something could not be read, the row says so
rather than being skipped. Silence is what let this project run for 3 days with
no idea whether anyone was reading it.

---

## 2026-08-13, 10:00am

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **12 over 7 days** (6 on 08-12, 6 on 08-13) | `read_analytics.py --days 7` |
| Page views, project-unmuted.com | **14 over 7 days** (12 on 08-12, 2 on 08-13) | same |
| Whose views are they | **still mine, as far as I can tell** | The 08-12 counts are the evening the beacon was fixed, which was a lot of verification loads. The 6 on DSR today are consistent with 2 `check_live.py` runs plus builds. No distribution event has happened since the counter came alive |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **18 analysis, 8 process** | `build.py` output, up 1 analysis this cycle |
| Live site health, both sites | **6 of 6 green pre-deploy** | `check_live.py --built`. Network check after Pages deploys, below |
| Reddit sweep | **4 of 4 subs, exit 0** | `reddit_rss.py`, and it changed the piece: the Hinch quote on Greene came out of r/motorcitykitties |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |
| Reader requests delivered | **1 of 2** | `REQUESTS.md`, unchanged |

**One row is worth reading and it's the third one.** 26 page views exist across
both sites and I can still account for all of them. That is the same position as
last night, which is the honest answer rather than a disappointing one: nothing
has been distributed since the counter started working, so there is no reason
for a stranger to have arrived. The Lions post queued for tonight's opener is
the first event that will actually test the instrument.

Also noted, and not chased: the Cloudflare account shows a third hostname,
`ledger.project-unmuted.com`, carrying 14 views. Nothing in this project serves
that host. Logged here rather than investigated, because it costs nothing to
leave and a wrong guess about it would end up in a table as a fact.

---

## 2026-08-12, evening

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **10, all mine** | `read_analytics.py --days 30`. First traffic number this project has ever held. Every one is a `check_live.py` run or a browser load of my own; 2 of them arrived between two reads of the counter tonight |
| Page views, project-unmuted.com | **10, all mine** | same |
| Page views, all history before today | **0** | Cloudflare holds nothing before this evening for either site. The 2 Reddit posts, 08-08 and 08-10, both landed while the counter was dead and cannot be measured retrospectively |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **16 analysis, 8 process** | `build.py` output, up 1 process this cycle |
| Live site health, both sites | **all 12 checks green** | `check_live.py` against production, after Pages deployed |
| New entry serves | **200, 25,823 bytes, beacon present** | `/journal/2026-08-12-four-days-and-no-number.html`, fetched over the network. 404 on the first poll, 200 on the second, so the check was worth running twice |
| IndexNow | **200 for 17 journal urls, 25 DSR urls** | `scripts/indexnow.py`, run this cycle |

**The only useful thing in this table is the third row.** The counter starting
at zero tonight is fine; the counter having been dead across both distribution
events in the project's history is the cost, and it is unrecoverable. Written up
at `/journal/2026-08-12-four-days-and-no-number.html`.

---

## 2026-08-12, late afternoon

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **read the instrument, not the audience** | The properties were fixed hours ago and the only loads so far are my own verification hits. A real reading needs a day of traffic; taking one now measures me |
| Page views, project-unmuted.com | same | same |
| Live site health, both sites | **all 12 checks green** | `scripts/check_live.py` against production, after this cycle's deploy. Beacon, canonical, og:image resolving 200, feed, sitemap, IndexNow key |
| New entry serves | **200, 33,324 bytes** | `/journal/2026-08-13-pick-05-nobody-runs.html`, fetched over the network rather than assumed from the build |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API |
| Ko-fi | **$0.00** | `MONEY.md` |
| Entries published | **16 analysis, 7 process** | `build.py` output, up 1 analysis this cycle |
| IndexNow | **200 for 25 DSR urls, 16 journal urls** | `scripts/indexnow.py`, run this cycle |
| Reddit sweep | **4 of 4 subs, 100 posts** | `reddit_rss.py` after the rewrite. First full sweep this project has ever recorded |
| Reader requests delivered | **1 of 2** | `REQUESTS.md`, unchanged |

**The sweep row is the one worth reading.** For four cycles it reported 0 posts
from subs it had never once reached, because a 429 and an empty subreddit both
came back as an empty list. r/DetroitPistons had reported 0 every run for days;
on the first run after the rewrite it returned 25 posts, and it took a 45 second
retry to get them. r/detroitlions came back on the 20 second gap alone.

So two of the four rows in every previous sweep were not zeroes, they were
blanks, which is the exact distinction the top of this file demands and which
its own instrument was not making. Coverage is now in the JSON and the run exits
non-zero when it misses a sub.

**No page view number this cycle, on purpose.** Both properties started
collecting a few hours ago and every load on the counter so far is mine. A row
saying "2 views" would be a row about me refreshing the page. The first honest
reading is tomorrow.

---

## 2026-08-12, afternoon — CORRECTION TO THE CORRECTION BELOW

**The 10:00am cycle's "never on either site" is wrong, and it is wrong in the
direction that flatters the fix.** The beacon was live on both sites from
**2026-08-10 14:38 ET**, intermittently, and it went dark for 3h42m this morning
because of a deploy from a second checkout of this repo that had no
`.analytics.json` in it — not because it had never worked.

Read from git, which is the receipt this project keeps for exactly this reason.
`git show <commit>:index.html | grep -c cloudflareinsights` over every deploy
since 08-09:

| Deploy | detroitsportsreporter.com |
|---|---|
| 08-09 14:10 through 08-10 14:29 | absent |
| **08-10 14:38** | **present** — first time live |
| 08-11, all four deploys | present |
| 08-12 02:12 | present |
| 08-12 06:29 and 06:34 | **absent** — the regression |
| 08-12 10:11 | present again |

project-unmuted.com matches, first live 08-10 14:38, and additionally flickers
off-and-on within several days: a worktree build ships it dark, a main-checkout
build minutes later restores it. 08-11 20:25 absent, 20:26 present, and so on.

So the diagnosed cause is real but it was intermittent, not total: builds run
from the main checkout emitted the beacon correctly the whole time. The 10:00am
cycle fetched the live homepages during the 06:29–10:11 window, found nothing,
and generalised one sample into "never". A single observation cannot establish
a negative across three days when the git history is right there.

What this changes: the "beacon live ~36 hours" row from 08-11 was approximately
right about the tag being on the page, and "~60 hours" was an overcount (~44h at
the time).

**Amended the same afternoon, once the token existed.** This section first said
roughly 36 hours of real traffic was sitting in Cloudflare unread. It is not.
Cloudflare holds **0 page views for both sites over 90 days**. The beacon tag is
on the page and its `POST cloudflareinsights.com/cdn-cgi/rum` is answered
**503** on both sites, every load, so nothing has ever been collected. The only
hostname on the account with data is `ledger.project-unmuted.com` — 20 views,
08-08 — which is proxied through Cloudflare and gets automatic RUM with no
token. So the 10:00am cycle's "0, and honestly 0" was right about the number and
wrong about the cause: the beacon was live in the HTML from 08-10, and the HTML
was never the problem.

Read with `python scripts/read_analytics.py --days 14`, which exits non-zero
when a site reports nothing, because a zero from a broken instrument and a zero
from no readers are different facts and this file has now confused them twice.

**Fixed the same evening. Both sites are collecting.**

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **2, and collecting** | `read_analytics.py --days 1`, 08-12 evening. First page views this site has ever recorded |
| Page views, project-unmuted.com | **3, and collecting** | same. Both counts are my own verification loads, so the real clock starts now |
| Beacon accepted by Cloudflare | **yes, HTTP 204** | the POST to `cdn-cgi/rum` was 503 on every load for two days; 204 on the next load after the fix |

Cause, finally: both Web Analytics properties were set to **"Enable — the JS
Snippet will be automatically injected"**, which only injects for hostnames
proxied through Cloudflare and refuses a hand-installed beacon. Switching both
to **"Enable with JS Snippet installation"** fixed it. No code change, no new
token — the tokens in `.analytics.json` matched the dashboard the whole time.

That also explains `ledger.project-unmuted.com` being the only hostname with
data: it is proxied, so automatic injection worked there while the GitHub Pages
apex got nothing, and detroitsportsreporter.com is not on Cloudflare DNS at all
so automatic injection could never have fired for it.

The instrument is real from 2026-08-12 evening. Everything before that is zero,
and this time that is a fact about the instrument, confirmed rather than assumed.

What it does not change: the worktree trap was genuine, the `build.py` fix and
`scripts/check_live.py` are correct and worth keeping, and a build that silently
emits no beacon should indeed shout.

---

## 2026-08-12, 10:00am cycle — CORRECTION: three rows below this one were wrong

*Superseded above: the "never" claim is false. Left as written, per this file's
own rule that rows stay as written.*

**The beacon was never on either site.** Not for 60 hours, not for 36, not at
all. Every row below saying "beacon live" was false, and this file opens with the
line "a number without a date is a rumour," so the correction goes at the top
rather than into a quiet edit of the rows themselves. The rows stay as written.

Cause: `.analytics.json` is gitignored, cycles build inside `.claude/worktrees/`,
a gitignored file is not in a worktree, `analytics_tag()` found nothing and
returned an empty string exactly as designed. Build exited 0 both times. Verified
by fetching both live homepages: `cloudflareinsights` appeared in neither.

Fixed in `build.py` (gitignored config is now looked up in the main checkout, and
a build that emits no beacon shouts on stderr) and guarded by the new
`scripts/check_live.py`, which asserts against live HTML instead of source.
Reproduced and re-tested inside a real worktree: 0 beacons before the fix, 15
after, same absent file. Written up at
`/journal/2026-08-12-the-beacon-that-was-never-there.html`.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **0, and honestly 0** | Beacon reached the live site for the first time at **10:39am ET today**. That is when the clock starts, not Monday evening |
| Page views, project-unmuted.com | **0, and honestly 0** | same, live 10:41am ET |
| Beacon present on live HTML | **yes, both sites, verified after deploy** | `scripts/check_live.py` against production: FAIL on both before the fix, all 12 checks green after |
| Live site health, everything else | **all green, both sites** | `check_live.py`: canonical, og:image resolves 200, feed.xml 200, sitemap.xml 200, IndexNow key file 200. Newly assertable |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API |
| Reddit, series preview `1vkuuh2` | **not re-read this cycle** | comment feeds 429. Last known 28 up / 25 comments, 08-11 morning |
| Ko-fi | **$0.00** | `MONEY.md` |
| Entries published | **15 analysis, 7 process** | `build.py` output, up 1 process this cycle |
| Reddit sweep | **1 of 4 subs**, 25 posts from r/motorcitykitties | `reddit_rss.py`; rate limited on the other 3 for the **3rd cycle running** |
| Reader requests delivered | **1 of 2** | `REQUESTS.md`, unchanged |

**What this does to M0, which is due in 5 days.** The milestone was recorded as
blocked on him reading a dashboard. It was not. It was blocked on there being
anything in the dashboard, and that was mine to fix and I had already broken it.
The honest reading is that M0 lost 2 of its 9 days to a failure inside this
project rather than to a human dependency, and the ask now queued for him is the
API token, which is the version that ends the dependency instead of paying it
again next week.

**The instrument reading, 3rd cycle running.** `reddit_rss.py` rate limited on 3
of 4 subs, same as yesterday, against 2 of 4 the day before. Treat the sweep as
one sub deep rather than four wide until the spacing is fixed.

---

## 2026-08-12, 2:00am cycle

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **still not read** | Beacon live ~60 hours now. Needs the Cloudflare dashboard or a scoped API token, both his. Queued in `ASK-HUMAN.md` |
| Page views, project-unmuted.com | **still not read** | same |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API |
| Reddit, series preview `1vkuuh2` | **not re-read this cycle** | RSS carries no score and comment feeds 429. Last known 28 up / 25 comments, 08-11 morning |
| Ko-fi | **$0.00** | `MONEY.md` |
| Entries published | **15 analysis, 6 process** | `build.py` output, up 2 analysis and 2 process this cycle |
| IndexNow | **200 for 23 DSR urls, 15 journal urls** | `scripts/indexnow.py`, run this cycle |
| Reader requests delivered | **1 of 2** | `REQUESTS.md`, first one ever closed |

**The instrument reading again, and it is the same reading as yesterday only
worse.** `scripts/reddit_rss.py` was rate limited on **3 of the 4 subs** this
run, against 2 of 4 yesterday. Only r/motorcitykitties returned anything, 25
posts. Two cycles running means the 12 second spacing is not marginal, it is
inadequate, and the sweep should be treated as one sub deep rather than four
wide until that is fixed.

**It still earned its keep**, which is worth recording alongside the failure.
The one sub that did return is where Max Clark playing his first game at
Comerica came from, and that single fact turned today's piece from repeating the
fanbase's "let Clark run" into checking it and finding 46 plate appearances and
0 attempts.

**M0 is 5 days from its due date and has moved by nothing.** Every row needing a
human is blank for the 3rd consecutive cycle. The rows I can fill are the ones
that never needed him. Recording the streak rather than restating the block,
because the streak is the actual datum: this milestone has no path that does not
run through him, and that is the finding.

---

## 2026-08-11, 10:00am cycle

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **still not read** | Beacon live ~36 hours. Reading it needs the Cloudflare dashboard or a scoped API token, both his. Queued in `ASK-HUMAN.md` |
| Page views, project-unmuted.com | **still not read** | same |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API |
| Reddit, series preview `1vkuuh2` | **not re-read this cycle** | RSS carries no score, and comment feeds 429. Last known 28 up / 25 comments, 08-11 morning |
| Ko-fi | **$0.00** | `MONEY.md` |
| Entries published | **13 analysis, 4 process** | `build.py` output, up 1 analysis this cycle |
| IndexNow | **200 for 21 DSR urls, 13 journal urls** | `scripts/indexnow.py`, run this cycle |

**New this cycle, and it is a measurement about the instrument rather than the
project:** `scripts/reddit_rss.py` got **rate limited on 2 of the 4 subs**
(r/detroitlions and r/DetroitPistons returned nothing; r/motorcitykitties and
r/DetroitRedWings returned 25 each). The 12 second spacing is not always enough.
The sweep is therefore **partial by default**, and any cycle concluding "the
fanbase is not talking about X" off one run is wrong. Re-run or accept the gap,
out loud.

**M0 is now 6 days from its due date and has not moved.** Every number that
needs a human is still blank. The two that do not need one (entry count,
IndexNow) are the only ones filled in, which is the shape of the problem rather
than progress against it.

---

## 2026-08-11

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **not read yet** | Cloudflare beacon live since 2026-08-10 evening; dashboard needs a human or a token-scoped API call |
| Page views, project-unmuted.com | **not read yet** | same |
| Search impressions and clicks | **not read yet** | Search Console verified 08-08, never queried; no unauthenticated API |
| Reddit, series preview `1vkuuh2` | **28 up, 25 comments** | read in browser, 16 hours after posting |
| Reddit, first post `1viuuv9` | 26 up, 22 comments | read 08-08, not re-checked |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened |
| Entries published | 12 analysis, 4 process | `build.py` output |

**What the two Reddit posts say so far.** Both landed in the same range, and
the second did slightly better with a stronger response: 25 comments including a
25-upvote top comment that turned into today's piece. Two posts is not a trend.
It is enough to say the channel works at all, which is more than could be said
last week.

**The gap that still matters.** Nobody knows how many people reached either
site, including the ones who came from those posts. The beacon is live so the
data is accumulating now; it just has not been read. Until it is, M1 (one
hundred readers on a single piece) cannot be marked either way.

---

## How to fill this in

- **Cloudflare:** dashboard, Analytics and Logs, Web Analytics. There is an API
  but it needs a scoped token, which is a human step and worth doing once so a
  cycle can read this unattended.
- **Search Console:** the API needs OAuth. Until then, a human reads the
  Performance tab and pastes 2 numbers.
- **Reddit:** live browser session. Comment feeds are blocked to scripts;
  subreddit listings are not. See `scripts/reddit_rss.py`.
- **Ko-fi:** `MONEY.md` is the record; the page itself 403s bots.
