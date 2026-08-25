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

**Regenerated 2026-08-25 02:00 ET, and the hook changed.** The original version
of this draft opened on both clubs having scored **exactly 587 runs**. Tampa Bay
won 4-1 on the night of 08-24, so it is 591 to 588 now and the exact tie is gone.
Every number below is from the 08-25 pull. Had this been posted this morning as
written it would have led with a figure that stopped being true 8 hours earlier.
The residuals moved too: Detroit from minus 11.9 to **minus 12.1**, Tampa Bay
from plus 7.4 to **plus 7.5**.

**It still decays, once a night.** They play again 08-25 and 08-26. Regenerate
before posting, whenever that is.

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

**Title:** The Rays and the Tigers have scored within 3 runs of each other this season and are 17 games apart

**Body:**

TLDR: Tampa Bay has scored 591 runs in 131 games and Detroit has scored 588 in
131. Detroit has allowed 26 fewer. Tampa Bay is 17 games ahead in the standings.
They are the biggest positive and the biggest negative Pythagorean residuals in
baseball and they are playing each other this week.

Numbers as of this morning, MLB Stats API, exponent 1.83.

Rays: 78-53, 591 scored, 544 allowed, expected 70.5 wins, **plus 7.5**.

Tigers: 61-70, 588 scored, 518 allowed, expected 73.1 wins, **minus 12.1**.

Those are the 2 extremes of all 30 teams. Third place in either direction is the
Reds at plus 6.1 and the Angels at minus 6.5, so the Tigers are nearly twice as
far out as anybody else.

The margin splits are where it stops being a curiosity:

Rays, 1 run: 18-13. 2 to 4 runs: 43-19. 5 or more: 17-21.

Tigers, 1 run: 12-22. 2 to 4 runs: 27-37. 5 or more: 22-11.

Detroit has a winning record in exactly one bucket and it's the one that eats
runs without buying wins. Tampa Bay has a losing record in that same bucket and
wins everything else. Nearly identical run totals, distributed differently.

The bullpen is the obvious candidate for the mechanism. Detroit is 26 of 54 in
save chances with 28 blown saves, which is the most in baseball, on a 3.61 team
ERA. Tampa Bay is 52 of 67 with 15 blown, on a 3.81. The holds gap says the same
thing from the other side: 101 to 60. So the club with the better run prevention
overall is much worse at run prevention with a lead in the 8th.

What I'm not sure about, and would like an argument on: how much of a minus 12.1
is actually the bullpen and how much is the leverage-independent noise you'd
expect from 131 games. 28 blown saves is not 12 wins on its own, since some of
those got won anyway and some were 3-run leads in the 7th. If somebody has a
cleaner way to attribute the residual than "look at the save conversion and
squint", I'd take it.

The other thing I can't decide is whether the 2 to 4 run bucket is doing more
work than the 1 run bucket here. Detroit is 27-37 there, which is 10 games under
in a bucket most people treat as a normal-luck zone, and 43-19 for Tampa Bay in
the same bucket is a bigger absolute swing than the one-run gap.

One caveat I'd rather say than have pointed out. Over the last 10 games Detroit
has gone 1-9 and been outscored 36 to 56, so the recent version of this team is
not being unlucky, it's being beaten. The season-long residual is real and the
current form is not evidence for it.

They play Tuesday and Wednesday at Comerica.
