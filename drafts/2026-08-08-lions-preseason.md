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
Before tonight's opener: I pulled every NFL preseason since 2015. The teams that went undefeated in August did worse than the teams that went winless.

BODY:
TLDR: teams that won every preseason game went .466 in the regular season. Teams that lost every preseason game went .475. Across eleven years, preseason record explains about one percent of what happens after Labor Day. Watch the right tackle job tonight, not the score.

Tables are in the image. 320 team-seasons, 2015 through 2025, no 2020 because there was no preseason that year. Ties count as half a win.

Top table, first row against last row. The undefeated group finished worse than the winless group. Correlation between preseason and regular season winning percentage is +0.103, which squares to 1.1 percent of the variance. If you sorted all 32 teams by preseason record you would have done almost nothing to sort them by how good they are.

Here is the part that argues against me, and it is the middle row of that same table. Teams with a winning but not perfect preseason went .561 across 93 team-seasons, which is a real gap over .500 and a bigger one than anything else on the table. If the story were clean, that group would sit between the undefeated group and the even group. It does not. The column does not climb, it bounces. My honest read is that a signal that is strong at 3-1 and reversed at 4-0 is not a signal, but if you want to argue that row is real, that is where you would plant your flag.

There is at least a plausible mechanism for the inverted top row. Good teams have the least to figure out in August, so they rest starters and let the fourth string lose a game nobody remembers. Winning in August may be mild evidence a roster needed the reps. That is a story, not a proof, and it points the same direction either way: do not read the score.

Detroit's own rows are the bottom table. The 15-2 team in 2024 went 2-1 in the preseason and opened it with a 14-3 loss to the Giants. The best preseason record on that table is the 2015 team at 3-1, and they went 7-9. But the two worst preseasons, 2019 and 2021, were also the two worst seasons, so it does not invert cleanly here either. It is noise pointing wherever it feels like.

The extremes elsewhere: Cleveland went 4-0 in the 2017 preseason and then 0-16. Baltimore went 4-0 in the 2019 preseason and then 14-2. Same August, opposite universes.

So tonight at Cincinnati, watch the right tackle job and not the scoreboard. Blake Miller against Larry Borom is the one genuinely open competition on this roster and it protects the blind side. Who is with the ones, who is still out there after the starters leave, whether the rookie holds up against a live rush without holding. The final score is the least informative number the whole night produces.

---

If it draws a reply asking where the data came from: ESPN's public schedule
endpoint, ties counted as half a win. The collection script and the cached raw
data are in a public repo. Do not volunteer the repo link unprompted, since it
reads as promotion.
