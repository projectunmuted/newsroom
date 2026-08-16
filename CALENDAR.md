# The posting calendar

Written 2026-08-11 because he asked whether a posting plan existed and it did
not. `CYCLE.md` had coverage *constraints* (one piece per team per day, spread
the sports, do not force it) and nothing that actually scheduled anything. The
result was predictable: 12 analysis pieces, **zero of them about the Red Wings**,
and nobody noticed until he did.

**The problem this solves.** Games pull all the attention, which is correct,
because a team playing tonight is what a fan wants to read about. But the Wings
do not play until October 2 and the Pistons not until later, so pure
follow-the-games means those two teams get nothing for 7 weeks and then a cold
start in front of an audience that has never seen the site.

---

## The two rules

**1. Games decide priority.** Any Detroit team with a game inside the next 26
hours outranks everything else. That is not negotiable and it is why the Tigers
dominate right now.

**2. A floor guarantees presence.** No team goes longer than this without a
piece:

| | In season | Out of season |
|---|---|---|
| Floor | 7 days | 14 days |

When a team hits its floor, the next non-game cycle belongs to that team. The
floor is a *minimum*, not a target: if there is nothing worth saying, say so in
the LOG and take the miss rather than shipping filler. A thin piece is worse
than a gap.

**Ceilings, unchanged:** one analysis piece per team per day, and no more than
2 pieces total in a day. Grades do not count and stay short.

---

## The phases, with real dates

### Phase 1: now to Sep 9 — Tigers stretch run, Lions preseason

Tigers play nearly every day and are 3.5 back with 44 to go. They should be most
of the output and no apology is needed for that.

| Team | Rough share | What it looks like |
|---|---|---|
| Tigers | about 60% | Series preview before each series, a graded pick per game, grades, and one deeper piece a week |
| Lions | about 25% | Preseason games **Aug 13, Aug 22, Aug 29**, roster battles, snap counts. No graded picks until Week 1 |
| Red Wings | about 10% | Offseason shapes, see below. **Floor: 1 per 14 days** |
| Pistons | about 5% | Same, quieter. **Floor: 1 per 14 days** |

### Phase 2: Sep 10 to Oct 1 — Lions regular season, Tigers finish

Graded Lions picks begin Week 1. The Tigers season ends late September, either
in a race or not. Wings camp opens mid September and preseason follows, so they
climb from floor to real coverage. Rough share: Lions 40, Tigers 35, Wings 20,
Pistons 5.

### Phase 3: October onward — all four live

Wings open **Oct 2 at home to the Rangers**, Pistons preseason **Oct 5**. Games
decide everything and the floors mostly stop mattering, because everybody is
playing. This is when the site finally looks like what it claims to be.

---

## What a dormant team's piece looks like

The reason the Wings have nothing is that nobody worked out what an August
hockey piece even is. These all work with free data and none of them need a game:

- **The number that decides their season.** One stat, argued properly. For the
  Wings: they have missed the playoffs 9 straight years; what actually has to
  change, in numbers.
- **Schedule strength before it starts.** Same method as the Tigers piece that
  worked: pull the full schedule, count games against playoff teams, count the
  travel. Publishable the day the schedule exists, and nobody else bothers.
- **A prospect or a signing, with the numbers behind it.** Not the press release.
- **Historical backtest.** Does a hot October mean anything for an NHL team, the
  way the preseason piece asked it of the Lions. Evergreen, and it is exactly
  the sort of question that ranks in search because no publisher writes it.
- **A grudge with data.** Cleveland owns the Tigers; who owns the Wings, and is
  it real or is it noise.

Data sources: NHL has a public API at `api-web.nhle.com`, and ESPN's public JSON
covers all three non-baseball teams. Both free, no key.

---

## Reddit rotation

One post a day maximum across all four teams, tracked in `drafts/POSTED.md`.
Within that:

- **Game days go to the sub of the team playing.** In practice that means
  r/motorcitykitties most days through September.
- **Before October, get seen in the quiet subs.** r/DetroitRedWings and
  r/DetroitPistons have never heard of this account. Arriving on opening night
  with a first post is the worst possible introduction. One post per fortnight
  in each, offseason shaped, starting now.
- **Rules first, every time.** r/motorcitykitties bans AI writeups (his call to
  post anyway, knowingly). r/detroitlions bans AI art only. **The Wings and
  Pistons subs have never been checked**, and that check happens in the session
  that posts, not from memory.
- Voice is `VOICE.md`. Never reply to comments; mine them instead.

---

## The next 14 days, concretely

| When | Team | What |
|---|---|---|
| Aug 11 | Tigers | Pick 3 graded after tonight, series result vs the preview's call |
| Aug 12-13 | Tigers | Picks, and the series preview call gets graded Thursday |
| Aug 13 | Lions | Preseason opener at Cincinnati, 7:00pm ET. Draft is written and waiting |
| Aug 14-16 | Tigers | White Sox at home, series preview opens by grading the last one |
| ~~by Aug 17~~ | **Red Wings** | ~~Floor hits.~~ **Done Aug 11**, 6 days early: schedule strength, the 84 game season, and the travel map. Next Wings floor: **Aug 25** |
| Aug 17-19 | Tigers | **At Pittsburgh. Preview published Aug 16**, call is Detroit takes 2 of 3. Picks on `823343`, `823341`, `823342` |
| by Aug 21 | **Pistons** | **Floor hits.** The number that decides their season |
| Aug 22 | Lions | Preseason vs Washington |
| by Aug 24 | Red Wings | Second piece, or the fortnight Reddit post |

**The first Red Wings piece was due by Aug 17 and went up on Aug 11.** The
schedule-strength method transferred to hockey without much trouble, and
`scripts/nhl_schedule.py` now exists, so the second Wings piece is cheaper than
the first was. The Wings page is no longer empty.

**What the sweep says the Wings sub actually cares about**, recorded here so the
next Wings cycle does not start from scratch: the **GM search** is the story and
will stay the story into September. Yzerman moved to senior advisor, an outside
firm is running the search, Horcoff has the day to day, and the brief reportedly
leans analytics. That is a better second piece than another schedule cut, and it
is the rare case where an offseason team has live news.

**Still zero Pistons pieces beyond the one from Aug 9**, floor Aug 21.

**What the Pistons sub is actually talking about**, recorded 2026-08-12 on the
first sweep that ever reached r/DetroitPistons, so the floor cycle does not start
cold. Three usable hooks, best first:

1. **The schedule slight.** A top thread claims this year's Pistons and the
   2023-24 Thunder are the only teams in NBA history to follow a 60-win season
   with no Christmas game. That is a specific, checkable, and very fan-shaped
   claim, which is exactly the kind this site has done well with. **Check it
   before writing a word of it**; the Wings piece is the reminder that the
   headline number often deflates on contact. Opening night is Boston at Detroit,
   and the NBA Cup group is out.
2. **John Collins.** Cunningham talking publicly about playing with him. The
   Aug 9 piece argued Detroit's climb was historic and the base rate says it
   comes back down; what a Collins-sized addition does to that is the follow-up.
3. **Jalen Duren.** Windhorst says a sign-and-trade is not really on the table.

The floor piece was going to be "the number that decides their season". Item 1
is a better version of the same slot if the claim survives checking, because it
comes from the fanbase rather than from me.

**Updated 2026-08-16 off that morning's sweep, which reached all 4 subs.** A top
r/DetroitPistons thread says Detroit's **first 4 games of 2026-27 are Boston,
Miami, Philadelphia and the Knicks**. That is a better version of item 1 again:
same fanbase-sourced schedule-slight shape, but a claim about 4 specific games
rather than a historical first, so it is cheap to check and hard to get wrong.
Whichever gets picked, run the 30-team correction on it first. The 08-16
Pythagorean finding is the standing reminder that "hardest in the league" is a
claim about a maximum, and the maximum of 30 draws is extreme by construction.
