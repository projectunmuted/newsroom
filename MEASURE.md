# The instrument panel

`PLAN.md` milestone M0. Every line carries the date it was read, because a
number without a date is a rumour. Newest at top.

**A blank is not a zero.** If something could not be read, the row says so
rather than being skipped. Silence is what let this project run for 3 days with
no idea whether anyone was reading it.

---

## 2026-08-27, 10:00am — baseline for the findings repo, taken the hour it shipped

Traffic read unsampled, single slice, exit 0. This row exists so the 2026-09-24
check has something to compare against: `github.com/projectunmuted/api-gotchas`
went public this morning and the test set for it is **one inbound visit that did
not come from Reddit.**

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **21 over 8 days**: 2, 4, 3, 2, 2, 2, 3, 3 (08-20 to 08-27) | `read_analytics.py --days 7`, unsampled, exit 0 |
| Page views, project-unmuted.com | **2**, both on 08-26, 1 visit | same |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since 08-08 |
| Emails to `projectunmuted@proton.me` | **0 ever**, and unreadable from here | `ASK-HUMAN.md` |
| Prediction record | **8-7**, Pick 16 pending | `PICKS.md` |
| Days since anything was posted to Reddit | **13** (last post 2026-08-14) | `drafts/POSTED.md` |
| Finished drafts waiting on approval | **2** | `ASK-HUMAN.md` |
| Non-Reddit inbound visits, ever | **0** | no referral has ever been recorded from anywhere else |
| Pages of ours in a search index | **not re-measured today** | last read 08-19, 0 of 6 queries |
| Public artifacts on a domain we do not own | **1**, new today: 4 findings, 5 files, all 5 verified 200 over the network | `curl` against `raw.githubusercontent.com` |

**The number that matters here is the last one, and it is a 1 rather than a
reader.** Nothing about this row says anybody read anything. It says the surface
exists, which was not true yesterday.

---

## 2026-08-25, 10:00am — the journal recorded 0 page views over 5 days

Traffic read unsampled, exit 0, single slice, 5 day window so it stays off the
sampling cliff.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **15 over 6 days**: 2, 4, 3, 2, 2, 2 (08-20 to 08-25) | `read_analytics.py`, unsampled, exit 0 |
| Page views, project-unmuted.com | **0.** Not a gap, a zero | same |
| Visits (sessions), both sites | **15 and 0** | same |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since 08-08 |
| Prediction record | **8-5**, Picks 14 and 15 pending | `PICKS.md` |
| Reddit sweep | **4 of 4 subs, exit 0** | `reddit_rss.py` |
| Days since anything was posted to Reddit | **11** (last post 2026-08-14) | `drafts/POSTED.md` |
| Finished drafts waiting on approval | **2** | `ASK-HUMAN.md` |
| Pages of ours in a search index | **not re-measured today** | last read 08-19, 0 of 6 queries |

**The journal's zero is the new fact and it is worth stating carefully.** On
08-20 project-unmuted.com read 9 views over 5 days with 2 of those days empty.
Today the whole 5 day window is empty. The window is raw rather than sampled,
exit 0, and detroitsportsreporter.com recorded on every one of the same days
through the same beacon, so the instrument is working and the number is real.

The journal is the money log. Nobody is reading it. That does not change what it
is for, because it is also the public record and the thing a reader who follows
the repository link ends up in, but it does mean **no argument about the dollar
made only on that site reaches anybody today.**

Both properties are flat while nothing is being posted, which is consistent with
the one channel being the only source of readers this project has ever measured.

## 2026-08-20, 10:00am — 5 routes tried at Reddit's rules pages, 5 closed

Traffic read unsampled, exit 0, single slice, 5 day window so it stays off the
sampling cliff.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **33 over 5 days**: 5, 9, 9, 4, 6, no row yet for 08-20 | `read_analytics.py`, unsampled, exit 0 |
| Page views, project-unmuted.com | **9 over 5 days**: 1, 3, 2, 3, no row for 08-19 or 08-20 | same |
| Visits (sessions), both sites | **30 and 5** | same |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since 08-08 |
| Prediction record | **7-4** | `PICKS.md`. Nothing pending; Detroit is off today |
| Reddit sweep | **4 of 4 subs, exit 0** | `reddit_rss.py` |
| Days since anything was posted to Reddit | **6** (last post 2026-08-14) | `drafts/POSTED.md` |
| Finished drafts waiting on approval | **2** | `ASK-HUMAN.md` |
| Pages of ours in a search index | **not re-measured today** | last read 08-19, 0 of 6 queries |

**Journal traffic has gone quiet in a way worth naming.** project-unmuted.com
recorded no row at all for 08-19 or 08-20 as of this reading. At this resolution
no row means no views rather than a gap in the instrument, because the window is
raw and the other property recorded on the same days. 5 days, 9 views, and 2 of
those days are zeroes.

**New negative result: the subreddit rules question cannot be answered from
here, and I tried harder than last time.** 5 routes, in order:

| Route | Result |
|---|---|
| `old.reddit.com/r/X/about/rules` | 200, but it serves the JavaScript shell with a "Welcome to Reddit" title and no rule text in the bytes |
| `www.reddit.com/r/X/about/rules/.json` | 403 Blocked, same as 08-18 and 08-19 |
| Wayback Machine, direct `id_` fetch | 404, no snapshot; the availability API returned 429 |
| Public Reddit mirrors, 9 instances | 6 dead or 403. The 1 that served bytes sits behind a proof of work challenge |
| Web search for the rules text | Returns research papers about subreddit AI policies, not the policies |

**The 4th row is a decision, not a wall, and it should be recorded as one.** The
working mirror answers with an Anubis challenge whose own page text says it
exists because "AI companies have changed the social contract around how website
hosting works." Its challenge is weak enough to solve in a few lines. I did not
solve it and will not. A project whose product is a reader being able to check
everything does not get to quietly defeat an anti-bot gate aimed at exactly this,
and rule 3 of the mission covers it: getting the answer and breaking a platform's
terms is a loss. The ask stays with the human.

---

## 2026-08-19, 10:00am — the first reading of whether search has us at all

Traffic read unsampled, exit 0, single slice. The new row is the last one and it
is the first time this project has ever asked it.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **64 over 7 days**: 6, 13, 16, 5, 9, 9, 4, and 2 so far on 08-19 | `read_analytics.py`, unsampled, exit 0 |
| Page views, project-unmuted.com | **27 over 7 days**: 12, 2, 4, 1, 3, 2, 3, no row yet for 08-19 | same |
| Visits (sessions), both sites | **48 and 16** | same |
| `/requests.html` views since 08-15 | **0, both sites, sixth reading in a row** | same, `--page /requests.html`, exit 0 |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since 08-08 |
| Prediction record | **6-4** | `PICKS.md`. Pick 11 pending, first pitch 12:35pm ET today |
| Reddit sweep | **4 of 4 subs, exit 0** | `reddit_rss.py` |
| Days since anything was posted to Reddit | **5** (last post 2026-08-14) | `drafts/POSTED.md` |
| **Pages of ours in a search index** | **0**, on 6 queries including 2 verbatim entry titles, with a control query that passed | in-session web search; method in `scripts/search_index_check.py` |
| **Indexed pages anywhere mentioning either domain** | **0** | searching the bare domain strings |

**A blank is not a zero and this one is not a blank.** The control matters more
than the result: the same tool, asked for an obscure Substack title in quotes,
returned the right URL. So the engine was answering and had nothing of ours.

**What cannot be measured from here, and it is worth recording as a limit rather
than a gap.** All 4 scriptable engines refuse this machine: Bing serves a results
page with no control hit, DuckDuckGo's HTML endpoint returns 202, Mojeek returns
a page titled `Captcha`, Marginalia returns 1,077 bytes. `search_index_check.py`
therefore exits **2** rather than reporting a zero it cannot stand behind. This
row has to be refreshed by hand, or from a session with a search tool.

Also unmeasurable and now known to be so: **Reddit's anonymous JSON and
`/about/rules` surfaces are blocked account-wide**, not just for this IP. A
proxy fetch returned Reddit's own text: "You've been blocked by network
security. To continue, log in to your Reddit account or use your developer
token." The RSS listing feeds still work, 4 of 4 subs today.


## 2026-08-18, 10:00am, and this is the reading that reorders the plan

Read unsampled, exit 0, single slice. **Every figure below is identical to the
2:00am reading 8 hours earlier**, including the partial 1 for 08-18, so nothing
arrived overnight and nothing here is a new measurement. That is the number.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **59 over 7 days**, unchanged from 8 hours ago: 6, 13, 16, 5, 9, 9, 1 so far on 08-18 | `read_analytics.py`, unsampled, exit 0 |
| Page views, project-unmuted.com | **24 over 7 days**, unchanged: 12, 2, 4, 1, 3, 2, still no row for 08-18 | same |
| Visits (sessions), both sites | **43 and 15**, both unchanged | same |
| `/requests.html` views since 08-15 | **0, both sites, fifth reading in a row** | same, `--page /requests.html` |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since 08-08 |
| Prediction record | **6-3** | `PICKS.md`. Pick 10 pending, first pitch 6:40pm tonight |
| Reddit sweep | **4 of 4 subs, exit 0, all live** | `reddit_rss.py` |
| **Analysis pieces by team** | **Tigers 26, Lions 3, Red Wings 2, Pistons 1** | `grep "^team:" entries/*.md`, counted for the first time today |
| **Subreddit rules, Wings and Pistons** | **unknown, and unreadable from here** | reddit `/about/rules` and `about/rules.json` both 403 as of today. Queued in `ASK-HUMAN.md` |

**The new row is the last one but the one that matters is the one above it.**
26 of 32 pieces are aimed at r/motorcitykitties, which bans this by Rule 5. The
only traffic event ever measured, 08-14 at 16 views, came from r/detroitlions,
which does not. Nobody had counted the split before this morning, and it is the
first thing in this file that says something about the *route* rather than about
the volume. Written up at
`/journal/2026-08-18-inventory-pointed-at-a-closed-door.html`.

**Flat line, day 5.** 5, 9, 9 and a partial 1 since the post day, on days that
mostly published 2 pieces each.

---

## 2026-08-18, 2:00am — 08-17 finished at 9, and `/requests.html` is at zero for the fourth reading

Read unsampled, exit 0, single slice, so nothing below needs a caveat.

**Yesterday's row for 08-17 said 2 and it was a partial day.** The day closed at
**9**. That is worth noting because a cycle reading a same-day figure at 10am is
reading a third of a day and will under-report it every time. The 08-18 figure
below is the same trap and is labelled as such.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **59 over 7 days**: 6 on 08-12, 13 on 08-13, 16 on 08-14, 5 on 08-15, 9 on 08-16, 9 on 08-17, 1 so far on 08-18 (partial, 4 hours in) | `read_analytics.py --days 7`, unsampled, exit 0 |
| Page views, project-unmuted.com | **24 over 7 days**: 12, 2, 4, 1, 3, 2, and no row yet for 08-18 | same |
| Visits (sessions), both sites | **43 and 15** | same |
| **`/requests.html` views since it went up 08-15** | **0, both sites, fourth reading in a row** | `MSYS_NO_PATHCONV=1 read_analytics.py --days 7 --page /requests.html`, filtered so it stays raw, exit 0 |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Emails to `projectunmuted@proton.me` | **unknown, needs his login** | `ASK-HUMAN.md`, no schedule |
| Prediction record | **6-3** | `PICKS.md`. Pick 9 graded correct, Pick 10 committed, first pitch 6:40pm today |
| Reddit sweep | **4 of 4 subs, exit 0, all live** | `reddit_rss.py`, 3 of the 4 needed a 429 backoff |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |

**The flat line is now 4 days long.** 08-14 was 16 and it was the day of a Reddit
post. The 4 days since are 5, 9, 9 and a partial 1. Two of those days published
2 pieces each. The publishing rate and the readership are not connected, which
is the same finding this file has recorded every day since 08-15, and it keeps
pointing at the same conclusion: the only thing that has ever moved this number
is a post on somebody else's front page, and the Lions draft that would be one
is still sitting in `drafts/` waiting on his approval.

---

## 2026-08-17, 10:00am — three straight days under 10 views, and the requests page is still at zero

Read unsampled, exit 0, single slice. Nothing here needed a caveat, which is the
first time that sentence has been true since the cliff was found.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **51 over 7 days**: 6 on 08-12, 13 on 08-13, 16 on 08-14, 5 on 08-15, 9 on 08-16, 2 so far on 08-17 | `read_analytics.py --days 7`, unsampled, exit 0 |
| Page views, project-unmuted.com | **24 over 7 days**: 12, 2, 4, 1, 3, 2 | same |
| Visits (sessions), both sites | **37 and 15** | same |
| **`/requests.html` views since it went up 08-15** | **0, both sites, third reading in a row** | `MSYS_NO_PATHCONV=1 read_analytics.py --page /requests.html`, filtered so it stays raw |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Emails to `projectunmuted@proton.me` | **unknown, needs his login** | `ASK-HUMAN.md`, no schedule |
| Prediction record | **5-3** | `PICKS.md`. Pick 8 graded correct, Pick 9 pending, first pitch 7:05pm today |
| Reddit sweep | **4 of 4 subs, exit 0, all live** | `reddit_rss.py`, 3 of the 4 needed a 429 backoff |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |

**The trend is the story and it is flat to down.** 08-14 was 16 and it was the
day of a Reddit post. The 3 days since, with no post, are 5, 9 and 2. Nothing
this project publishes on its own reaches anybody; the only movement this file
has ever recorded came from somebody else's front page. That is the argument for
why the queued Lions draft sitting in `drafts/` is worth more than another entry.

---

## 2026-08-16, 10:00am (second cycle) — every number below this line was read one day inside a sampling cliff

**Read this before trusting any older row in this file.** Cloudflare's RUM API
switches to a **1-in-10 sample** when a query's start crosses about 7 days back,
and at that resolution a day with single-digit views returns **no row at all**
rather than a zero. `read_analytics.py` defaulted to `--days 7`, one day inside
the boundary, which is why every figure in this file is correct. It was correct
by accident, not by design.

Measured minutes apart, same credentials: `--days 7` gives 08-12: 6, 08-13: 13,
08-14: 16, 08-15: 5, 08-16: 6. `--days 8` gives 08-12: 10 and nothing else, exit
code 0. Fixed by chunking the window at the cliff and reading `sampleInterval` on
every query; a partial read now exits 2. Written up at
`/journal/2026-08-16-the-instrument-was-sampling.html`.

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **46 over 7 days**: 6 on 08-12, 13 on 08-13, 16 on 08-14, 5 on 08-15, 6 so far on 08-16 | `read_analytics.py --days 7`, unsampled, exit 0 |
| Page views, project-unmuted.com | **19 over 7 days**: 12, 2, 4, 1, 0 | same |
| **Visits (sessions), both sites** | **33 and 12** | same. **New row.** `count` is pageloads and `visits` is sessions; on 08-14 they were 16 and 6, so quoting the wrong one is a factor of nearly 3 |
| **`/requests.html` views since it went up 08-15** | **0, both sites** | `read_analytics.py --page /requests.html`, filtered so it stays unsampled. Control: `/about.html` returns 1 and 2, so the query works and the page has no readers |
| **`/picks.html` views** | **0** | same method. The record also renders on the DSR homepage, which has 31 of the site's 46 views, so the board is being seen and its own page is not |
| **08-13 Lions post, revised** | **at most 3, and the shape argues for less** | `--hourly`. The 3 arrived one per hour at 5pm, 6pm and 7pm ET around a 7:00pm post, then **0 for the next 11 hours**. Upper bound, not a measurement |
| **08-14 White Sox preview, previously "unknowable"** | **3 to 5** | `--hourly`. Reconstructed without a baseline. 10 of that day's 16 landed in the 9:00am ET hour, long before the post |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Emails to `projectunmuted@proton.me` | **unknown, needs his login** | `ASK-HUMAN.md`, no schedule |
| Prediction record | **4-3** | `PICKS.md`, Pick 8 pending, first pitch 1:40pm today |
| Reddit sweep | **4 of 4 subs, exit 0, all live** | `reddit_rss.py` |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |

**What moved and what did not.** No new readers, no dollar. What changed is that
the two numbers this project's plan leans on both got softer: the conversion
figure behind "1 visit per 3,000 impressions" is an upper bound off a post with
no spike in it, and the favourite route's first step has a measured audience of
zero. Both are better information than yesterday and neither is good news.

---

## 2026-08-16, 10:00am — a new row, because the number I was implicitly optimising was the wrong one

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **5 on 08-15, 16 on 08-14, 13 on 08-13, 6 so far on 08-16** | `read_analytics.py --days 3` |
| Page views, project-unmuted.com | **1 on 08-15, 4 on 08-14, 2 on 08-13, 0 so far on 08-16** | same |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **27 analysis, 13 process** | counted off `entries/*.md` frontmatter |
| **Requests generated per Reddit post** | **0, 2, 4, unread** across the 4 posts, oldest first | `requests.json` rows attributed to their source thread. **New row this cycle** |
| Reader requests **published** | **4 of 6** | `requests.json`, unchanged this cycle. The 2 open ones are the Cleveland question from 08-10 and the preseason snap-count question |
| Emails to `projectunmuted@proton.me` | **unknown, needs his login** | `ASK-HUMAN.md`, no schedule |
| Prediction record | **4-3** | `PICKS.md`, Pick 7 graded this cycle |
| Reddit sweep | **4 of 4 subs, exit 0, all live** | `reddit_rss.py`, JSON parses |
| Live site health, both sites | **6 of 6 green on `--built`** | `check_live.py --built`, network run after Pages deploys |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |

**The new row is the point of this one.** Page views have been the headline number
here since 08-14, and page views feed the tips route, which `PLAN.md` already
prices as a coin flip needing 178 consecutive good posts. The route this project
calls the favourite needs **one person who asked for something specific**, so the
per-post number that matters is requests generated, and nobody had ever counted
it.

Counted, by thread: the 08-08 Pythagorean post at 26 upvotes and 22 comments
produced **0** requests. The 08-11 series preview produced **2**. The 08-13 Lions
backtest, 5 upvotes against 33 comments and the worst-received post of the 4,
produced **4**. All 6 requests in `requests.json` came from the 2 posts people
argued with. The 08-14 White Sox preview has never had its comments read, so 1 of
4 cells is genuinely unknown rather than zero, and it stays labelled unread.

Four posts is a direction, not a rate, and the 2 request-producing posts were also
the 2 most specific ones, so specificity and disagreement cannot be separated at
this sample size. Written up at
`/journal/2026-08-16-the-post-that-worked-was-a-coin-flip.html`.

**A miscount caught before it shipped, recorded rather than quietly fixed.** The
first draft of this row said 3 requests from the 08-11 preview and 7 in total,
read off the section headings in `REQUESTS.md`. Counted properly off
`requests.json`, which is the file the site actually renders, it is 2 and 6: both
08-10 requests came from thread `1vkuuh2`, and one `REQUESTS.md` heading covers a
question asked by 2 separate commenters. Same failure class as the stale
histogram caption. The count now comes from the machine-readable file.

---

## 2026-08-15, 10:00am — the favourite route had no front door, and a count in this file was off by one

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **16 on 08-14, 13 on 08-13, 6 on 08-12, 2 so far on 08-15** | `read_analytics.py --days 3` |
| Page views, project-unmuted.com | **4 on 08-14, 2 on 08-13, 12 on 08-12, 0 so far on 08-15** | same |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **25 analysis, 12 process** | counted off `entries/*.md` frontmatter, up 1 each this cycle |
| Reader requests **published** | **4 of 6** | New denominator; see below |
| Ways for a reader to ask for anything | **1, as of this morning. It was 0** | `/requests.html` and `projectunmuted@proton.me` |
| Reddit sweep | **4 of 4 subs, exit 0, all live** | `reddit_rss.py`, and the JSON parses with `json.load` |
| Live site health, both sites | **6 of 6 green on `--built`** | `check_live.py --built`; network run after Pages deploys |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |

**The row that matters is the one that reads 0.** `MONEY.md` and `PLAN.md` have
called "somebody pays for a specific breakdown" the likeliest first dollar since
08-14, on the grounds that it needs 1 person rather than 530 visits. Its first
step is a reader asking a question, and there was no address on either site.
There never had been. Every page carried a tip button. Fixed this cycle;
`/journal/2026-08-15-no-way-to-ask.html`.

**A count in this file was wrong, so it gets corrected rather than quietly
restated.** The 2:00am row said 24 analysis and **10** process. The analysis
figure was right; the process figure was 11. Both are now counted directly off
the frontmatter in `entries/` rather than read from the previous row, which is
how the wrong number survived. Same failure class as the stale histogram caption
and the 2015 window: a number written down once and then trusted.

**Requests move to 4 of 6, and the denominator grew on purpose.** The 4 published
answers are unchanged. The 2 open ones, the Cleveland question from 08-10 and the
preseason snap-count question from 08-13, are now *listed publicly as open*
rather than only existing in `REQUESTS.md`. A request nobody can see is not
outstanding, it is invisible.

**No page-view baseline needed this cycle**: nothing was posted to Reddit.

---

## 2026-08-15, 2:00am — the second measured post has no baseline, because nobody wrote one down

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **16 on 08-14, 13 on 08-13, 6 on 08-12** | `read_analytics.py --days 3` |
| Page views, project-unmuted.com | **4 on 08-14, 2 on 08-13, 12 on 08-12** | same |
| The 08-14 r/motorcitykitties post | **3 DSR views at most, and the ceiling is soft** | 13 at the 10:00am cycle, 16 at end of day. The 10:00am cycle itself did a network `check_live` and fetched 3 new pages, so some of the 16 is mine |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **24 analysis, 10 process** | `build.py`, up 3 analysis this cycle |
| Live site health, both sites | **6 of 6 green on `--built`** | `check_live.py --built`; network run after Pages deploys |
| Reader requests **published** | **3 of 4** | Up from 1 of 4. The scatter and the histogram both have URLs now |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |

**The measurement failure this cycle is that the second Reddit post was not
pre-registered.** On 08-13 a cycle wrote the post-time baseline into
`drafts/POSTED.md` before the Lions post went up, and that single act is the only
reason the answer came back as 3 views rather than a flattering 7. On 08-14 the
White Sox series preview went to r/motorcitykitties, was retitled and edited by
him, and **no post-time baseline was recorded and no impression count was ever
read.**

So the honest reading of the 2nd distribution event this project has measured is
"somewhere between 0 and 3 page views, and I cannot separate the post from my own
build traffic." The discipline that worked on its first outing was not repeated
on its second, one day later, and the cost is that a data point is gone.

**What that means for the plan:** the 1-visit-per-3,000-impressions figure from
08-13 is still a sample of one. Nothing this cycle either confirmed or moved it.

**Requests are at 3 of 4 published**, which is the row that actually advanced.
The 4th is the snap-count mechanism a commenter raised, which is a research
question rather than a request and needs preseason starter snap data that has not
been checked for availability.

---

## 2026-08-14, 10:00am — the 33 commenters matter more than the 9,000 viewers

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **32 over 7 days: 6 on 08-12, 13 on 08-13, 13 so far on 08-14** | `read_analytics.py --days 7` |
| Page views, project-unmuted.com | **17 over 7 days: 12 on 08-12, 2 on 08-13, 3 so far on 08-14** | same |
| Today's 13 on DSR | **almost certainly mine** | The 2:00am cycle ran `check_live.py` over the network plus fetched 3 new pages individually. That is most of 13 on its own. Not counted as readers |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **21 analysis, 10 process** | `build.py` output, up 1 each this cycle |
| Live site health, both sites | **all checks green on `--built`** | `check_live.py --built`; network run after Pages deploys |
| Reddit sweep | **4 of 4 subs, exit 0** | `reddit_rss.py`, all 4 from cache |
| Reader requests **published** | **1 of 4** | New denominator, and it is the point. See below |
| Reader requests worked but unpublished | **2 of 4** | `REQUESTS.md` |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |

**The row that changed today is the requests row, and it changed because the
denominator was wrong.** This file has carried "reader requests delivered: 1 of
2" for three days. The real position is that the 08-13 Lions thread produced
**4** requests, 2 were answered into `REQUESTS.md` and `scripts/*.png` on 08-13,
and **neither was ever published anywhere a reader could reach.** The rule
against replying in-thread is right and is not the problem: nothing stopped an
entry going up. "Delivered" had been defined as "the answer exists."

So the honest count until this morning was **0 of 4 published**, and this cycle
takes it to 1 of 4.

**The forward arithmetic, written down so it can be checked later.** At the
measured 1 visit per 3,000 impressions, 178 days to the deadline at 1 post a day
and 9,000 impressions each gives about **530 site visits**. At a 1-in-200 tip
rate that is 2.7 tips; at 1-in-1,000 it is 0.53. The visit-to-tip rate has never
been observed and cannot be at this traffic, which makes it the most load-bearing
unmeasured number in the plan.

---

## 2026-08-14, 2:00am — the first distribution event ever measured, and the answer is 3

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **19 over 7 days: 6 on 08-12, 13 on 08-13, 0 so far on 08-14** | `read_analytics.py --days 7` |
| Page views, project-unmuted.com | **14 over 7 days: 12 on 08-12, 2 on 08-13, 0 so far on 08-14** | same |
| **Views after the Lions post went up** | **3 on DSR. 0 on the journal.** | `drafts/POSTED.md` recorded the baseline **at post time**: DSR 10, journal 2. The day ended at 13 and 2 |
| Was it the post | **Probably, and it barely matters at this size** | No cycle ran between the 7:00pm ET post and midnight, so those 3 are not build or `check_live` loads. They could be the human. 3 is inside the range where one person explains all of it |
| The 9K views the post itself got | **9,000 impressions, 33 comments, 3 site visits** | Post metrics from the thread, site views from Cloudflare |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **20 analysis, 9 process** | `build.py` output, up 2 analysis and 1 process this cycle |
| Live site health, both sites | **all checks green on `--built`** | `check_live.py --built`; network run after Pages deploys |
| Reddit sweep | **4 of 4 subs, exit 0** | `reddit_rss.py`, and it changed the pick. See `LOG.md` |
| Search impressions and clicks | **still not read** | no unauthenticated Search Console API, still an `ASK-HUMAN.md` item |
| Reader requests delivered | **1 of 2** | `REQUESTS.md`, unchanged |
| The `ledger.project-unmuted.com` hostname | **14 views, still unexplained, still not chased** | Nothing in this project serves that host |

**Read the third row against the fifth one, because that is the finding.** A post
that reached about 9,000 people and drew 33 comments sent **3** page views to the
site. That is the number, and it is close enough to zero that the honest summary
is "a fan-sub post that argues does not send people to a profile."

`drafts/POSTED.md` predicted this outcome as a live possibility and said in
advance that a zero would be a real answer worth having before another week goes
into posts. It nearly is a zero.

**A correction on this row, made before it was committed.** The first draft of
this table compared 08-13's final 13 against the **10:00am** reading of 6 and
concluded that 7 views arrived after 10am, which read as a modest success. That
is wrong: the baseline that matters was taken **at post time in the evening** and
it was already 10. 4 of those 7 arrived during ordinary cycle activity before
the post existed. The pre-registered baseline in `POSTED.md` is the only reason
the flattering version did not get published, which is exactly the job it was
written to do.

**What it does still settle, narrowly:** the chain is not mechanically broken.
Somebody went post to profile to site, which the rule against linking makes 3
deliberate steps, and before this morning it was unknown whether anyone ever
would. The rate at which they do it is roughly 1 in 3,000.

---

## 2026-08-13, 10:00am

| What | Number | Read from |
|---|---|---|
| Page views, detroitsportsreporter.com | **12 over 7 days** (6 on 08-12, 6 on 08-13) | `read_analytics.py --days 7` |
| Page views, project-unmuted.com | **14 over 7 days** (12 on 08-12, 2 on 08-13) | same |
| Whose views are they | **still mine, as far as I can tell** | The 08-12 counts are the evening the beacon was fixed, which was a lot of verification loads. The 6 on DSR today are consistent with 2 `check_live.py` runs plus builds. No distribution event has happened since the counter came alive |
| Ko-fi | **$0.00** | `MONEY.md`, unchanged since the rail opened 08-08 |
| Entries published | **18 analysis, 8 process** | `build.py` output, up 1 analysis this cycle |
| Live site health, both sites | **all 12 checks green** | `check_live.py` against production after Pages deployed, not just `--built` |
| New entry serves | **200, 30,150 bytes, beacon and chart present** | `/journal/2026-08-13-tigers-outfield-injuries.html`, fetched over the network |
| IndexNow | **200 for 18 journal urls, 27 DSR urls** | `scripts/indexnow.py`, run this cycle |
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
