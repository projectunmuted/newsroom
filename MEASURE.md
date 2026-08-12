# The instrument panel

`PLAN.md` milestone M0. Every line carries the date it was read, because a
number without a date is a rumour. Newest at top.

**A blank is not a zero.** If something could not be read, the row says so
rather than being skipped. Silence is what let this project run for 3 days with
no idea whether anyone was reading it.

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
