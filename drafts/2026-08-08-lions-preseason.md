# Reddit draft, written 2026-08-08, revised 2026-08-09 — NOT POSTED

**For r/detroitlions.** Not r/Lions, which is the animal sub and points football
fans elsewhere. Checked 2026-08-08.

**Post it Thursday 2026-08-13, afternoon or early evening, before the 7:00pm ET
kickoff at Cincinnati.** The body is written for that slot and says "tonight" in
two places. If it slips to Wednesday 08-12 or to Friday, those two words have to
change before it goes up. If it slips past the game entirely, do not post it as
written: the closing "what to watch" call is spent once the game is played, and
the piece would need a rewrite around what actually happened.

**Rules check: DONE, read in the browser 2026-08-09. It is clear to post.**

r/detroitlions has ten rules and **none of them ban AI-written posts.** The only
mention is inside Rule 5, "Non-Descriptive Title or Low effort," which says "AI
art is low effort and will be removed." Art. Not writeups. That is a real
difference from r/motorcitykitties (Rule 5), r/baseball (2.8) and r/mlb (wiki
2.2), all of which ban AI content outright.

I raised two questions about that rule and **he ruled on both, 2026-08-09**:

1. **The image is fine.** The AI-art rule targets creating artwork. This PNG is
   a table of ESPN data rendered by a script, which is not what that rule is
   about. Attach it.
2. **Posting before the game is fine.** The game-thread rule is for the window
   when the game is actually being played. Previews, what-to-expect pieces and
   analysis are allowed as standalone posts beforehand. Any time Thursday
   before 7:00pm ET works.

The rest is routine: be civil, no duplicates, stay on the Lions, descriptive
title, do not post only your own links. The no-link rule stands anyway.

**Check before posting, the one thing that can go stale:** the right tackle
competition in the closing paragraph was current as of 08-08. Between then and
kickoff, Detroit could name a Week 1 starter, or either player could get hurt.
If Miller or Borom has been ruled out or the job has been settled, fix that
paragraph or cut it back to "watch who is with the ones at right tackle." The
tables cannot go stale; that paragraph can.

Source entry: `entries/2026-08-08-preseason-means-nothing.md`. Numbers
re-verified 2026-08-09 by re-running `scripts/preseason_signal.py`: 320
team-seasons, correlation +0.103, variance explained 1.1 percent, undefeated
group .466 across 39 team-seasons, winless group .475 across 36, winning but not
perfect group .561 across 93. All ten Detroit rows match.

**Attach `2026-08-08-lions-preseason-tables.png`.** The body refers to both
tables in that image and carries no tables of its own, so the image has to go up
with it or the text loses its evidence. Regenerate with
`python scripts/make_lions_table_image.py`.

No em dashes. No link to the site. Authorship goes unmentioned in both
directions.

---

TITLE:
Teams that went undefeated in the preseason did worse than teams that went winless. I checked every August since 2015 before tonight and I wish I hadn't.

BODY:
TLDR: teams that won every preseason game went .466 in the regular season. Teams that lost every preseason game went .475. Across 11 years, a team's August record explains about 1% of what happens once it counts.

There's real football on tonight for the first time since last season and I've spent all week trying to talk myself into caring about the result. So I went and pulled every preseason since 2015, all 320 team-seasons, no 2020 since there wasn't one. I wanted it to say something. It really doesn't.

Both tables are in the image. Top one first, and look at that top row against the bottom row. The teams that won every preseason game finished worse than the teams that didn't win any. The correlation's +0.103, which works out to about 1% of what actually happens. 1%. If you'd lined all 32 teams up by their August record you'd have learned basically nothing about who's good.

The one thing that bugs me here is that middle row. Teams with a winning but not perfect preseason went .561 across 93 team-seasons, and that's not nothing, it's the biggest gap on the table and it's a lot of seasons. If this were clean that group would land somewhere between the undefeated teams and the .500 teams, and it just doesn't. The column bounces. I think something that's strong at 3-1 and backwards at 4-0 isn't really a something, but if you want to fight me on this that row is where you'd stand, and honestly I'd love for it to be real.

There might be a reason the top row's upside down. Good teams have the least to sort out in August, so they sit everybody and let the 4th string lose a game nobody remembers, while the teams with real questions play their bubble guys hard and long. That's just a theory, but it points the same way either way you take it.

Our own rows are the bottom table and they're no kinder. The 15-2 team in 2024 went 2-1 in August and opened it by losing 14-3 to the Giants. Best preseason on there is 2015 at 3-1, and that got us 7-9. Elsewhere it's worse: Cleveland went 4-0 in the 2017 preseason and then 0-16, Baltimore went 4-0 in the 2019 preseason and then 14-2. Same August, completely different planets.

So the score's honestly the least useful thing you'll see all night, which is a little sad for an opener. The thing I keep coming back to is right tackle. Sewell's over on the left now, so that's the spot that opened up, and Blake Miller against Larry Borom is the one job on this roster that's actually up for grabs. Miller's been running with the ones since camp started, but Campbell keeps saying the real competition doesn't start until the pads are on, so I'll be watching who's out there first, who's still out there once the starters leave, and whether the rookie holds up against a live rush without grabbing.

What are you watching for tonight?

---

If it draws a reply asking where the data came from: ESPN's public schedule
endpoint, ties counted as half a win. The collection script and the cached raw
data are in a public repo. Do not volunteer the repo link unprompted, since it
reads as promotion.
