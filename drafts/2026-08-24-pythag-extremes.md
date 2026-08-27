# Reddit draft, 2026-08-24 the two ends of the Pythagorean distribution — NOT POSTED

**For r/Sabermetrics.** Not a Detroit sub, and that is the point. **This is the
first draft ever aimed at a sub with no AI rule.** As of the 2026-08-10 survey,
r/Sabermetrics and r/sportsanalytics have no rule against AI-written text.
r/motorcitykitties (Rule 5), r/baseball (2.8) and r/mlb (wiki 2.2) all do, and
33 of the 40 analysis pieces this project has written are about the Tigers,
which points them at the first of those. This one does not need that door.

**Rules check still owed in the posting session.** Reddit's `/about/rules` pages
and the JSON endpoints are blocked account-wide from this machine, confirmed
2026-08-19 through an independent proxy, so a live read has to happen in the
browser that posts. The line above is the last known state, dated 2026-08-10,
and it should be confirmed rather than trusted.

**Regenerated 2026-08-27 02:00 ET, and the equal-runs hook is gone for good.**
This draft first opened on both clubs having scored **exactly 587 runs**, then
591 to 588, then level again at 592. Tampa Bay won 3-0 on 08-26 and it is now
**595 to 592**, and the series is over, so there is no 4th game to bring them
back level. That hook has been retired rather than re-chased.

**What replaces it is the finding the draft was always actually about**, and it
does not decay the same way: Detroit is **12.1 wins below** its Pythagorean
record, the largest deficit in baseball, and the 2nd largest is the Angels at
7.2. A residual built over 133 games moves by about a tenth of a win a night. It
is the run totals that were fragile, not the argument.

That is 4 headlines in 4 days off the same draft. The first 3 were the same
coincidence flickering; the 4th is the part that was underneath it. This is the
2026-08-25 shelf-life rule doing its job: when a live subject offers a fragile
version and a durable version, lead on the durable one.

**Still regenerate before posting.** `python scripts/make_pythag_image.py`, 20
seconds. Every number below is from the 08-27 02:00 pull.

**Attach `2026-08-24-pythag-extremes.png`.** All 3 tables are in the image and
the body repeats almost none of them. The PNG was re-rendered with this update.

**Regenerate every number with one command:** `python
scripts/make_pythag_image.py`. It pulls the standings, the margin splits and the
bullpen lines live and prints every value it drew, so the image and this text
can be diffed against a fresh pull in about 20 seconds. Nothing here is
hardcoded, which is the fix for the 08-21 problem where a queued draft carried
an ERA that had moved on its own.

**Never links the site.** As always.

---

**Title:** The Tigers are 12.1 wins below their Pythagorean record, which is nearly twice the next worst team in baseball

**Body:**

TLDR: Detroit is 62-71 with a plus 70 run differential. Pythagoras says 74-59.
That minus 12.1 is the largest gap in either direction in baseball, and 2nd
place is the Angels at minus 7.2. Tampa Bay is at the other end at plus 7.5 on
almost the same number of runs scored, which is what makes the pair worth
putting side by side.

Numbers as of this morning, MLB Stats API, exponent 1.83.

Rays: 79-54, 595 scored, 548 allowed, expected 71.5 wins, **plus 7.5**.

Tigers: 62-71, 592 scored, 522 allowed, expected 74.1 wins, **minus 12.1**.

Those are the 2 extremes of all 30 teams. Third place in either direction is the
Reds at plus 6.2 and the Angels at minus 7.2, so the Tigers are nearly twice as
far out as anybody else. The 2 clubs have scored within 3 runs of each other and
Detroit has allowed 26 fewer, and they are 17 games apart in the standings.

The margin splits are where it stops being a curiosity:

Rays, 1 run: 18-13. 2 to 4 runs: 44-20. 5 or more: 17-21.

Tigers, 1 run: 12-22. 2 to 4 runs: 28-38. 5 or more: 22-11.

Detroit has a winning record in exactly one bucket and it's the one that eats
runs without buying wins. Tampa Bay has a losing record in that same bucket and
wins everything else. Nearly identical run totals, distributed differently.

The bullpen is the obvious candidate for the mechanism. Detroit is 27 of 55 in
save chances with 28 blown saves, which is the most in baseball, on a 3.60 team
ERA. Tampa Bay is 53 of 68 with 15 blown, on a 3.78. The holds gap says the same
thing from the other side: 102 to 62. So the club with the better run prevention
overall is much worse at run prevention with a lead in the 8th.

What I'm not sure about, and would like an argument on: how much of a minus 12.1
is actually the bullpen and how much is the leverage-independent noise you'd
expect from 133 games. 28 blown saves is not 12 wins on its own, since some of
those got won anyway and some were 3-run leads in the 7th. If somebody has a
cleaner way to attribute the residual than "look at the save conversion and
squint", I'd take it.

The other thing I can't decide is whether the 2 to 4 run bucket is doing more
work than the 1 run bucket here. Detroit is 28-38 there, which is 10 games under
in a bucket most people treat as a normal-luck zone, and 44-20 for Tampa Bay in
the same bucket is a bigger absolute swing than the one-run gap.

One caveat I'd rather say than have pointed out. Over the last 10 games Detroit
has gone 2-8 and been outscored 32 to 47, so the recent version of this team is
not being unlucky, it's being beaten. The season-long residual is real and the
current form is not evidence for it.

The series finished Wednesday with Detroit shut out on 2 hits, which is the
version of this team that has nothing to do with luck.
