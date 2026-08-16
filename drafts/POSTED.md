# Reddit posting ledger

Newest at top. **Check this before preparing another post.**

The cap is **one post per day across all four teams combined**, his rule
2026-08-10. Not one per sport, not one per sub. A cycle has no memory of what an
earlier cycle queued, so this file is the only thing standing between three
cycles a day and three posts a day.

A row goes in when something is actually posted, not when a draft is written.
Drafts live beside this file and say plainly at the top that they are unposted.

| Date | Sub | What | Thread | Reception |
|---|---|---|---|---|
| 2026-08-14 | r/motorcitykitties | Series preview: White Sox at Comerica, image post | `1voamk1` | Posted before the 6:40pm opener. He retitled it "Series Preview: The home team has won every game so far" and edited the body; the edits are the newest sample in `VOICE.md`. He cut the opening line that graded the previous preview, which retires that tradition. |
| 2026-08-13 | r/detroitlions | Preseason backtest, 320 team-seasons, image post | `1vne8nx` | Posted before the 7:00pm ET opener at Cincinnati. **He retitled it "Preseason record really doesn't matter." and edited the body.** **5 up, 33 comments, 9K views** at 2h, not removed. The comment-to-upvote ratio is the story: it argued rather than landed. Top comment at 13 up is that the 2008 Lions went 4-0 in the preseason and 0-16, and the sample starts in 2015 so it is missing. See `REQUESTS.md`. First post ever to go up with the traffic counter working; baseline below. |
| 2026-08-11 | r/motorcitykitties | Series preview: Guardians at Comerica, image post | `1vkuuh2` | Posted 2026-08-10 evening, before Tuesday's opener. First of the series-preview tradition. Call on the board: Tigers take 2 of 3. |
| 2026-08-08 | r/motorcitykitties | Tigers xW-L and the schedule concentration, image post | `1viuuv9` | 26 up, 22 comments, not removed. Three objections worth more than the post; see LOG 08-08. |

## The 08-13 baseline, so tomorrow's number means something

Read at post time with `python scripts/read_analytics.py --days 2`. Both
properties only began collecting the evening of 08-12, so these are small and
most of them are ours:

| | 08-12 | 08-13 before the post |
|---|---|---|
| detroitsportsreporter.com | 6 | 10 |
| project-unmuted.com | 12 | 2 |

Nearly all of that is verification loads from setting the beacon up. **The
number that matters is 08-14 against 08-13**, and specifically whether DSR moves
while the journal does not, since only the Lions sub was pointed at anything.
Read it tomorrow morning before doing anything else and write it down even if it
is zero. A zero here is a real answer: it would mean a fan sub post that draws
comments still sends nobody to a profile, which is worth knowing before another
week goes into posts.

Caveat that has to stay attached to whatever the number is: the post does not
link the site, by rule. Anyone who arrives went post to profile to site, so this
measures that whole chain, not the post.

### Revised 2026-08-16: the 3 is an upper bound, and the 08-14 post is measurable after all

Hourly buckets (`read_analytics.py --hourly`, added this morning) reconstruct both
posts without a baseline. All times Eastern.

**08-13 Lions post**, before a 7:00pm opener. The hours through 10:00am sum to
exactly the 10 written down below, which confirms the baseline recorded what it
claimed. The 3 that follow arrived **one per hour at 5pm, 6pm and 7pm**, and then
DSR recorded **nothing for the next 11 hours**, straight through the evening. If
the post went up at 5pm all 3 count; if it went up near first pitch, 1 or 2 of
them precede it. Either way there is no spike in the data, so 3 is the most
generous reading rather than a measurement.

**08-14 White Sox preview**, written off below as unknowable. It is worth **3 to
5** depending on the post minute, before a 6:40pm first pitch. The day's 16 views,
Detroit Sports Reporter's best ever, are mostly a **10-view spike in the 9:00am
hour** hours before the post, from a source I cannot identify.

So both measured posts land in the same low single digits, and the "1 visit per
3,000 impressions" figure is the ceiling of that range, not the middle.

### The answer, read 2026-08-14 2:00am: 3

DSR ended 08-13 on **13**, from the 10 above. The journal ended on **2**, from
2. So the post is worth **3 page views on DSR and 0 on the journal**, against
**9,000 impressions and 33 comments**. About 1 visit per 3,000 people who saw it.

No cycle ran between the 7:00pm ET post and midnight, so the 3 aren't build or
`check_live` loads, though they could be his.

**This table is the reason the number is 3 and not 7.** The first draft of the
`MEASURE.md` row compared 13 against the *10:00am* reading of 6 and reported a
modest success. 4 of those 7 arrived before the post existed. Keeping the
post-time baseline, written down when it couldn't be chosen to suit a
conclusion, is what caught it. **Keep doing this for every post.**

What it means for the next one: a fan-sub post that argues rather than lands
sends almost nobody to a profile. That's worth knowing before another week goes
into posts, which is exactly what this measurement was set up to find out.

## Queued, not yet posted

- **2026-08-14, r/detroitlions:** `drafts/2026-08-14-lions-2008-followup.md`.
  Direct follow-up to `1vne8nx`, conceding the 2008 objection and reporting the
  rerun on 798 team-seasons. Needs his approval like every post. **It carries a
  baseline table to fill in at post time**, and the thing it actually tests is
  whether a post that agrees with the sub converts differently from one that
  argues with it. Today's slot is open.
- **Nothing for 2026-08-13.** The Lions backtest used that day's single slot.
