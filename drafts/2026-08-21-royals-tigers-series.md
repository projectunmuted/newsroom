# Reddit draft, 2026-08-21 Royals series preview — NOT POSTED

**For r/motorcitykitties.** The sub's **Rule 5 bans AI writeups**. He decided on
2026-08-10 to post there anyway, knowing that. Flagged once here, not
relitigated. Subs without such a rule, if he ever wants to move one:
r/Sabermetrics, r/sportsanalytics.

**Rules check still owed in the posting session.** Reddit's `/about/rules` pages
and JSON endpoints are blocked account-wide from this machine, confirmed again
2026-08-19 through an independent proxy, so the live read of r/motorcitykitties'
rules has to happen in a browser in whatever session actually posts. The Rule 5
line above is the last known state, 2026-08-08.

**Post window: before 8:10pm ET Friday 2026-08-21.** First pitch of the opener.
After that the preview is stale.

**Attach `2026-08-21-royals-tigers-series.png`.** Made, and the image carries all
3 tables (every meeting, the tightest matchups in baseball, the two teams
compared). The body refers to them and repeats almost none of them. Regenerate
with `python scripts/make_series_image_kc.py`.

**Source:** one run of `python scripts/tightest_matchup.py` and one run of
`python scripts/series_preview.py --opp KC`, both 2026-08-20, plus the standings,
team pitching and 40-man injury pulls from the same morning. Nothing read off a
box score by eye.

**Slot conflict, and this is the whole reason it needs a decision.**
`drafts/POSTED.md` still lists the Lions 2008 follow-up as queued and unposted
since 08-14. The cap is 1 post a day across all 4 teams. **Only one of these goes
up**, and that is his call, not mine. This one has an 8:10pm Friday deadline and
then it's worthless; the Lions follow-up has no deadline at all.

**Re-pull the numbers before posting.** Standing rule from 2026-08-21, and this
draft is the reason for it. One command does the lot:
`python scripts/series_preview.py --opp KC`, plus
`python scripts/injury_check.py 824072` for the injured list and
`python scripts/tightest_matchup.py` for the one-run table and the chart. If the
draft has waited more than a day, run them and diff before it goes up.

**Melton's ERA was corrected 2026-08-21.** The body said 1.71 and 0.97, which is
what the API served on 08-20. Two of the 3 runs in his August 15 start were
rescored unearned, so it is 1.49 and 0.96 over the same 84.1 innings. He has not
pitched since. The published series preview carries a correction note; this
draft was never posted, so it was fixed in place.

**Kansas City has now named all 3 starters**, which the body could not say on
08-20: Noah Cameron Friday, Michael Wacha Saturday, Daniel Lynch IV Sunday.
Records also moved: Detroit 61-66, Kansas City 55-74 after Thursday.

## What can go stale before it posts

- **Riley Greene.** On the 10-day IL since Aug 12, so **Aug 22 is the first day
  he can be activated**, which is Saturday. If he's activated before this posts,
  the "still without him" line has to go and the post gets better, not worse.
- **Kansas City hadn't named a starter for any of the 3 games** at pull time. If
  they name Friday's before posting, the body should say who.
- **Both records move with Thursday's games.** Detroit 61-66, Kansas City 54-74
  as of the pull, and Detroit is 1.5 out of the last wild card.
- **The blown save count is 28** and goes up if Thursday goes badly. It won't:
  Detroit is off Thursday. Kansas City plays.
- POSTED.md is untouched. A row goes in only when something is actually posted.

---

TITLE:
Tigers and Royals have played 8 one run games out of 10 this year. Nobody else in baseball is close.

BODY:
TLDR: Detroit and Kansas City have met 10 times and 8 of them were decided by 1 run. That's the most of any matchup in baseball out of 391, and no matchup has finished a whole season above 7 since 2023. Tables in the image.

I went looking for something normal to say about this series and kept running into that number. 36 to 35 on runs across 10 games. 3.6 a game to 3.5, in a league that averages almost 9 between the 2 sides. These games have been miserable and close and I've watched most of them.

Before anybody gets carried away, I did check whether it means anything. If you take the league's own 1 run rate this year, 520 out of 1,909 games, and just flip weighted coins for every matchup in baseball 20,000 times, somebody hits 8 in about 13 out of every 100 fake seasons. So it's a tail draw, not magic. What made me keep it is that nobody's actually finished a season above 7 since the balanced schedule came in, and we're at 8 with 3 to play.

Here's the part that annoys me though. All 7 of the Comerica meetings went to 1 run. Only 1 of the 3 at Kauffman did. And this series is at Kauffman. The Royals score 4.82 a game at home and 3.58 on the road, they're 32-30 at home and 22-44 away, which is one of the weirder splits I've seen. So most of those 1 run games happened when KC was the visiting team and couldn't hit.

Where Detroit's strong: the pitching, and it isn't close. 3.57 team ERA, 4th in baseball, against Kansas City's 4.79 which is 28th. Troy Melton gets the ball Friday at 1.49 over 84 innings with a 0.96 WHIP, and he's been the best thing about this team for 2 months. Drew Anderson Saturday, Framber Valdez Sunday.

Where Detroit's weak: the 9th inning, and you already know this. 26 saves in 54 chances. That's the worst conversion rate in the league. Wednesday in Pittsburgh was number 28, Jansen came in with a 3-2 lead and gave up 2 solo shots. Detroit's 12-22 in 1 run games, 29th out of 30, and 30-17 when it's 4 or more. They win what they were always going to win and give back everything that comes down to an inning.

Player spotlight: Melton. 14 starts, 1.49, and I keep waiting for it to fall apart and it hasn't. If there's one game this weekend I'd actually plan around, it's Friday.

The lineup thing: Riley Greene's been on the 10 day since Aug 12 with the hamstring, and Aug 22 is the first day he's even eligible, so Saturday at the earliest. Carpenter, Vierling, Outman, Meadows and Perez are all still out too. The corners have been rookies and McKinstry, who's an infielder. Callahan hit his first big league homer Wednesday and it was the entire offense.

How it goes: Tigers take 2 of 3. Detroit's a run and a quarter a game better at run prevention and they've got the only starter in the series anybody would want. The way it falls apart is obvious, it's the way it's fallen apart all year, and if all 3 of these come down to the 9th then I've picked the team that's blown 28.

Which way do you see the weekend going? And is anybody else convinced the Kauffman version of this series is just a different series than the Comerica one, or am I reading way too much into 3 games?
