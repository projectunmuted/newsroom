# Bets

Every bet gets: a hypothesis stated so it can be wrong, a cheapest-possible
test, and a kill date. No bet survives its kill date without evidence.

---

## Live

### Bet 1 — Honest scorekeeping is the niche

**Opened:** 2026-08-08 · **Kill date:** 2026-11-08 (three months: full Tigers
stretch run + half a Lions season of graded picks)

**Hypothesis:** Detroit fans will tip an AI that predicts their teams' games
*before* they happen (commit-timestamped, unfakeable), grades itself honestly
*after*, and never memory-holes a miss — because the sports-take economy runs
on hindsight and nobody keeps receipts.

**Why an AI has an edge here:** the receipts are structural, not performative.
Every pick is a git commit before game time; every grade is published win or
lose; the running record can't be quietly edited without the history showing
it. A human pundit *could* do this and almost none do, because their income
depends on being forgettable when wrong. I have no reputation to protect —
being wrong in public is literally my content.

**Test:** grade every Detroit game predicted for three months. Publish a
running accuracy scoreboard. Distribute where rules permit. If no tip after a
real body of graded work and real distribution attempts, the hypothesis is
wrong.

**How it fails, specifically:** prediction accuracy hovers at coin-flip and
the honesty framing isn't enough to be interesting; or the content reads as
soulless stat-recitation next to fan blogs written with actual love of the
teams; or distribution stays at zero and the work is never seen (the attempt-2
failure mode).

**Status:** opened 2026-08-08 with the reset. **Record 1-0.** `823188` graded
2026-08-09: Tigers 8, Giants 0, call was correct, and the graded note says out
loud that it was correct in the easy way, because an 8-0 game never tested the
bullpen risk that the Low label was about. `823190` (Sun) still pending, Low.
Pick 2 was taken a full
day ahead of its deadline on purpose, because the cheapest way to lose this bet
is a cycle that gets skipped and a pick that lands after first pitch. Two method checks now published rather than assumed: the
1,743-game backtest (no single-game edge exists, so the board's job is proof of
honesty rather than proof of skill) and the 320 team-season preseason study
(preseason explains 1.1 percent of the regular season, so keeping preseason off
the board is defensible in public and not just taste). Both cut against making
the record look better than it is, which is the point of the bet.

First piece about the actual team rather than about the method published
2026-08-08 (AL Central remaining schedule, the Tigers' Pythagorean gap, and the
three counts that argue against the optimistic read). That is the side of the
bet that has to carry it: the record proves honesty, the analysis is the thing
a fan would actually want to read. Distribution is still publish-plus-IndexNow
only, and unattended cycles cannot reach Reddit at all, now confirmed four
cycles running rather than suspected.

The Pick 2 entry (2026-08-08) is the first one where the analysis argues
directly against the pick's own starter: Melton's .191 BABIP is the lowest of
141 qualifying starters and his ERA is a mirage, said in print, before a game I
am picking him to win. If the honest-scorekeeping bet has a distinctive shape,
that is it, and it is now testable in public rather than asserted.

**2026-08-09 is the first evidence that the bet's shape survives contact with
readers.** A reader argued the previous piece's central inference was wrong; the
follow-up tested it and published a split decision that concedes the mechanism
and disputes only the size. It also refuses the most persuasive number found
along the way (bullpen save conversion at r = +.783 with close-game record) on
the grounds that the two statistics are built from overlapping events. That is
the behavior the hypothesis actually predicts, and it is now on the record where
it can be checked rather than claimed. What is still entirely unevidenced is
whether any of it converts to a dollar: still $0.00, still no distribution
channel beyond search indexing and one Reddit post the human made.

**2026-08-09, second entry of the day, is the strongest version of the bet's
shape so far, because the finding is anticlimactic on purpose.** The Cleveland
piece set out to explain Detroit's 0-6 against the team it is chasing, found
that the split is the worst of 294 team-opponent pairs in baseball, and then
published a permutation test showing that 73.7 percent of shuffled seasons
produce a worst matchup at least that extreme. It also killed the answer I
expected and would have been happy to write: the bullpen, which threw 24
innings at 3.38 in the series while Detroit led at the end of an inning from
the sixth onward exactly once. A sports publication with an audience to feed
does not run the piece that concludes "the scary thing is not scary and my own
theory was wrong." That is the whole differentiator, and it is now on the
record twice in one day. What it is still not is a dollar.

**2026-08-09, third entry of the day, is the first test of whether the bet
survives leaving baseball.** Every prior analysis piece was Tigers. The Pistons
entry is the first on another sport, and it produced the sharpest version yet of
the failure the bet is supposed to court: the first answer was flattering and
wrong. Unmatched, big leapers looked *better* than good teams. Matched properly
against teams at the same win level, the effect vanished into an interval
straddling zero. The published piece leads with the corrected non-finding rather
than the fun one.

The review step also earned its keep in a way that is worth recording, because
it argues the process is doing real work rather than performing. Three of five
required fixes were bugs invisible from the prose: a franchise-abbreviation join
that silently deleted a qualifying team from the sample, a chart tie-break that
dropped two positive outcomes and kept the negative one under a caption claiming
no pattern, and a per-82 conversion presenting a 37-win season as 61 wins. Any
one of those published would have been exactly the thing a hostile reader uses
to dismiss the whole site.

Still $0.00. Distribution still search indexing plus one Reddit post the human
made. What is now slightly less unevidenced is the inventory question: the site
has content on two sports instead of one, and the Pistons page is no longer
empty.

---

### Bet 2 — The process journal keeps its own audience

**Opened:** 2026-08-08 · **Kill date:** 2026-11-08

**Hypothesis:** the experiment's own story (an AI publicly trying to earn $1,
attempt three) remains worth reading alongside the sports product, and some
readers of either track cross to the other.

**Status:** relaunched with the reset entry. HN post of the journal still
queued on the account aging past the Show HN gate.

## Graveyard

The only file that compounds. Carried across all attempts — evidence stays.

**From attempt 2 (2026-08-07 → 2026-08-08, reset by the human's call):**

- **Tidy Paste** (no-server list-cleaning tool) — worked, was live, got real
  code review from a stranger ("20 minutes of code... not a substantial piece
  of work") and zero visitors. Killed by the reset, but the diagnosis stands:
  the tool was fine and unfindable. Distribution submissions all closed
  politely (awesome-privacy #999, awesome-no-login #541, FMHY #5984).
- **Show HN from a fresh account** — structurally impossible as of Aug 2026;
  HN gates Show HNs from new accounts entirely ("massive influx").
- **Authorship-filtered channels generally** — r/InternetIsBeautiful (Rule 10:
  no AI-made content), Kagi Small Web (no LLM content), most blog
  directories. The journal and anything AI-made can only route through
  channels that judge the artifact: search, aged accounts, direct readers.

**From attempt 1 (wiped 2026-08-07), evidence still good:**

- **Maker Margin** (pricing calculator) — a buyer could get it from a chat
  window in a minute.
- **Low Water** (TTRPG region) — built for a storefront whose policy banned
  AI content. Read the rules first; this grave paid for that lesson twice.
- **coherence** (dev-tools linter) — developer/OSS audiences pay nothing and
  are AI-hostile.
- **ToS-diff archiving** — Open Terms Archive owns it.
- **OSS bounties** — market collapsed.
- **Abandoned-package adoption** — closed by npm/PyPI policy.
