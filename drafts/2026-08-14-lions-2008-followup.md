# UNPOSTED DRAFT — needs his approval before it goes anywhere

**Sub:** r/detroitlions
**Type:** text post (no image needed; the tables are short enough to read inline)
**Date drafted:** 2026-08-14
**Slot:** 2026-08-14 is open per `drafts/POSTED.md`. One post per day across all
four teams.

**Rules check, as of the last verified read (2026-08-09, in a browser):**
r/detroitlions bans AI-generated **art** only. It has no rule against AI-written
text. **Re-read the rules in the browser at post time anyway** — that check
happens in the session that posts, not from memory.

**What this is:** a direct follow-up to `1vne8nx`, the preseason backtest posted
2026-08-13. The top comment at 13 upvotes was that the 2008 Lions went 4-0 in
the preseason and 0-16 and were excluded from the sample. They were right. This
post concedes that, and reports what happened when the missing seasons went in.

**Why it is worth posting:** it is the first post that answers the sub rather
than telling it something. Every previous post argued. This one starts by
agreeing with the top comment. Whether that changes how a post performs is
completely untested and is the reason to run it.

**Never link the site.** The site lives in the profile. **No em dashes. No
percentages as confidence. Never reply to a comment.**

---

## Title

You were right about 2008, so I went and got the missing 15 seasons

## Body

Posted the preseason thing on Thursday. Top comment, and a couple of others,
said the same thing: the 2008 Lions went 4-0 in August and 0-16, and the sample
started in 2015 so it wasn't in there.

That's correct, and the reason I gave for the window was wrong. I said 2015 was
where the data started. It isn't. It goes back to 2000. So here's all of it, 798
team-seasons instead of 320.

**Your case was stronger than you made it.** Sorted by regular season winning
percentage, these are the 3 worst seasons in the whole 25 years:

- Detroit 2008: preseason 4-0, regular season 0-16
- Cleveland 2017: preseason 4-0, regular season 0-16
- San Diego 2000: preseason 4-0, regular season 1-15

Both 0-16 seasons in NFL history came out of an undefeated preseason. So did the
1-15. Add St. Louis going 4-0 in 2011 and then 2-14, and Washington 4-0 in 2013
and then 3-13.

**And then 2011.** Also 4-0 in August. 10-6 and the playoffs. Same franchise,
3 years apart, and those are the worst season anybody has ever had and the first
Lions playoff berth in 12 years.

**What it does to the answer:** basically nothing. Correlation between preseason
win rate and regular season win rate is +.106 on 798 team-seasons. Variance
explained 1.1 percent. On the smaller sample it was 1.0. Adding 2008 and 2011
and 476 other team-seasons moved it by a tenth of a point.

**What it does kill is the line I led with.** I said teams that went undefeated
in August did worse than teams that went winless, .466 against .475. That's gone.
On the full sample it's .475 against .473, which is a 2 point gap across 138
teams and means nothing. That inversion was an artifact of an 11 year window and
I shouldn't have made it the headline.

The version that survives is duller and holds up better. Share of teams winning
9 or more per 17 games:

- Undefeated preseason: .456
- Everybody: .469
- Winless preseason: .357

An undefeated August tells you nothing. A winless August is mild bad news. Which
is close to the opposite of what I posted.

For what it's worth, of the 68 teams that swept their preseason, the biggest
single group won 10 games, and 10 teams did that. 4 won 14 and 2 won 15. New
England went 4-0 in the 2003 preseason and 14-2. The win totals run from 0 to 15
with no cluster anywhere, which is what no signal actually looks like once you
stop averaging it.

Detroit's own 25 seasons average .497 in the preseason and .401 in the regular
season, which is its own joke.

Two things in my data were also just wrong, and both were in the first post.
Teams that relocated were getting matched by abbreviation, so a 2015 Rams game
comes back saying STL, nothing matched, and the code used whichever team was
listed first. Often the opponent. San Diego's 2015 was in there as 10-6 when
they actually went 4-12. And games that were never played come back scored 0-0
rather than blank, so 41 of them were counting as ties, half a win each way.
Fixed both.

Anyway. 16-14 Thursday, it means nothing, and now it means nothing with 2008 in
the table instead of conveniently left out of it.

---

## The baseline, to be read at post time and written down here BEFORE posting

**Do not skip this.** On 08-13 the first draft of the follow-up measurement
compared the day's total against a morning reading and reported a modest success
that was 4 views' worth of nonsense. The post-time baseline is the only thing
that catches that.

Run `python scripts/read_analytics.py --days 2` immediately before posting and
fill in:

| | 08-13 | 08-14 before the post |
|---|---|---|
| detroitsportsreporter.com | 13 | _to fill_ |
| project-unmuted.com | 2 | _to fill_ |

**The specific question this post tests:** the 08-13 post argued with the sub and
converted at about 1 visit per 3,000 impressions. This one concedes to it. If
conceding converts the same, the problem is the 3-step post-to-profile-to-site
chain rather than the tone, and no amount of better writing fixes it. That is
worth knowing before another week goes into posts.
