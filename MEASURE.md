# The instrument panel

`PLAN.md` milestone M0. Every line carries the date it was read, because a
number without a date is a rumour. Newest at top.

**A blank is not a zero.** If something could not be read, the row says so
rather than being skipped. Silence is what let this project run for 3 days with
no idea whether anyone was reading it.

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
