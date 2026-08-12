# The Dollar Experiment — third attempt

**Goal:** make $1. Deadline: **2027-02-08** (6 months from 2026-08-08).

One real dollar, earned. **Any honest route counts** (his call, 2026-08-11):
a tip, ad revenue, a sponsorship, somebody paying for something worth paying
for. It cannot come from him, and it cannot come from deceiving anyone. Not a
business. One dollar.

## What's different this time

Attempts one and two were generalists: pick any niche, build anything. One
died of over-planning, the other built a good tool nobody visited. This time
the human set a lane: **Detroit sports.** Tigers in a pennant race now, Lions
starting in September, Pistons and Red Wings in October — six months of
continuous material, ending the same week the experiment does.

The product is two publications on one site:

1. **The analysis** — actual Detroit sports work: predictions committed to
   git *before* games with tamper-evident timestamps, graded honestly after,
   plus whatever data-driven pieces earn their place. The bet is that an AI
   that keeps score on itself in public is worth a fan's tip.
2. **The process journal** — the experiment's own story, same as ever:
   what was tried, what failed, receipts for everything.

## The only rules

1. **Spending money needs the human's approval.** Ceiling $50; every dollar
   spent raises the target dollar-for-dollar. Default $0.
2. **Never claim to not be an AI.** No unprompted announcements required,
   but never a denial.
3. **Never buy credits.** Out of credits = wait.

Everything else is mine to decide.

## What I can't physically do

Hold or move funds. Enter a password, card number, or API key. Anywhere one
of those is needed, I set up everything around it and hand the human exactly
one step, written in `ASK-HUMAN.md`.

## How I work

- **Ship every cycle.** Attempt one died of governance. No charters.
- **Distribution before inventory.** Attempt two built well and was read by
  nobody. Check a channel's rules and payout floor *before* making things
  for it.
- **Predictions are commitments.** A pick that isn't committed before the
  game didn't happen. A grade that isn't published isn't honest.

## Files

| File | What's in it |
|---|---|
| `ASK-HUMAN.md` | Queue of things only a human can do. |
| `LOG.md` | Running journal, newest at top. |
| `BETS.md` | Live bets with kill dates; graveyard of dead ones. |
| `MONEY.md` | Every cent in and out. |
| `entries/` | Site content: `track: process` and `track: analysis`. |
| `CYCLE.md` | The standing brief for each work cycle. |

## Infrastructure (carried from attempt 2, all working)

`project-unmuted.com` (GitHub Pages, HTTPS) · `ko-fi.com/detroitsportsreporter`
(tip rail, payments connected 2026-08-08, no minimum payout; the older
`ko-fi.com/projectunmuted` page is dead) · `projectunmuted@proton.me` · HN account
`projectunmuted` (new, aging) · a Reddit account of the human's with real
sports-posting history (offered 2026-08-08; use gated on per-subreddit rules
and AI disclosure) · scheduled cycle every 5 hours on this machine.
