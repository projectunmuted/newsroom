# How do you prove a prediction was made before the event?

You publish it somewhere you cannot quietly edit, and you let a third party
record when you did.

This repository is a working example of that, and the audit trail behind it.
19 baseball game predictions, each one committed to a public git repository
before first pitch, each one graded afterwards against the league's own game id.
Every row carries the evidence, and nothing here asks you to take a number on
trust.

## The record

**10-8** on 18 graded predictions. 19 committed in total.

That is a small sample and it is not the point of this repository. A coin lands
10-8 often enough that no honest reading of it says anything yet. The
point is the method: the record can only ever get more auditable, and a bad run
cannot be quietly deleted, because deleting it would leave a hole in a public
commit history.

## The three timestamps

Each prediction in `predictions.csv` carries all three.

| Column | What it is | Who controls it |
|---|---|---|
| `commit_time_utc` | when the pick row was committed to `PICKS.md` | **us**, and that matters |
| `github_push_time_utc` | when GitHub's events API recorded the push | **GitHub** |
| `first_pitch_utc` | scheduled first pitch, from the MLB Stats API on `gamePk` | **MLB** |

The first one is close to worthless on its own. Git lets whoever makes a commit
write any date they like into it, so a self-reported commit timestamp proves
nothing about when the work happened. Anybody publishing a prediction record
with commit timestamps and no other witness is showing you a number they chose.

The second one is the actual evidence. GitHub writes `created_at` on a
`PushEvent` when it receives the push, from its own clock, and serves it through
a public API to anybody who asks. It is the moment the prediction became visible
to the world.

The third one comes from the league.

`minutes_pushed_before_first_pitch` is column 2 subtracted from column 3. If it
is ever zero or negative, the prediction was not a prediction.

## What the audit says

- Predictions where the push landed **after** first pitch: **0**
- Predictions with **no** GitHub push record found: **0**
- Tightest margin: **509 minutes** (8.5 hours) before first pitch
- Median margin: **1121 minutes** (18.7 hours)
- Widest margin: **2478 minutes**

## The predictions

| # | Game | Call | Confidence | Final | Grade | Minutes before first pitch |
|---|---|---|---|---|---|---|
| 1 | Tigers at Giants, Jobe vs Roupp | Tigers win | Low | Tigers 8, Giants 0 | correct | 1121 |
| 2 | Tigers at Giants, Melton vs Webb | Tigers win | Low | Tigers 3, Giants 1 (10) | correct | 1565 |
| 3 | Guardians at Tigers, Bibee vs Anderson | Tigers win | Low | Tigers 6, Guardians 4 | correct | 2191 |
| 4 | Guardians at Tigers, Griffin vs Valdez | Tigers win | Low | Guardians 6, Tigers 4 | wrong | 983 |
| 5 | Guardians at Tigers, Messick vs Montero | Tigers win | Low | Tigers 3, Guardians 0 | correct | 1226 |
| 6 | White Sox at Tigers, Newcomb vs Jobe | Tigers win | Low | White Sox 9, Tigers 5 | wrong | 980 |
| 7 | White Sox at Tigers, Kay vs Melton | Tigers win | Low | White Sox 4, Tigers 3 | wrong | 647 |
| 8 | White Sox at Tigers, Burke vs Anderson | White Sox win | Low | White Sox 7, Tigers 5 | correct | 1644 |
| 9 | Tigers at Pirates, Valdez vs Mlodzinski | Tigers win | High | Tigers 8, Pirates 5 | correct | 532 |
| 10 | Tigers at Pirates, Montero vs Ashcraft | Tigers win | Low | Pirates 4, Tigers 1 | wrong | 890 |
| 11 | Tigers at Pirates, Jobe vs Skenes | Pirates win | Low | Pirates 4, Tigers 3 | correct | 622 |
| 12 | Tigers at Royals, Melton vs Cameron | Tigers win | Low | Royals 5, Tigers 2 | wrong | 1076 |
| 13 | Rays at Tigers, Rasmussen vs Valdez | Rays win | Low | Rays 4, Tigers 1 | correct | 509 |
| 14 | Rays at Tigers, Seymour vs Jobe | Rays win | Low | Tigers 4, Rays 1 | wrong | 985 |
| 15 | Rays at Tigers, Peralta vs Melton | Tigers win | Low | Rays 3, Tigers 0 | wrong | 1612 |
| 16 | Dodgers at Tigers, Skubal vs Anderson | Dodgers win | High | Dodgers 2, Tigers 1 | correct | 2428 |
| 17 | Dodgers at Tigers, Snell vs Montero | Dodgers win | Low | Tigers 2, Dodgers 1 | wrong | 1623 |
| 18 | Dodgers at Tigers, Glasnow vs Valdez | Dodgers win | High | Dodgers 6, Tigers 1 | correct | 1651 |
| 19 | Tigers at Twins, TBD vs TBD | Tigers win | Low | not played yet | pending | 2478 |

Confidence has two settings and no percentages. High means the caller expects to
look stupid if it misses. Low means picking a side is the job.

## Verify it yourself

`verify.py` re-derives every column above from public APIs. It needs Python 3
and nothing else, no key and no account:

    python verify.py

It fetches each commit from GitHub's API, each game from the MLB Stats API, and
recomputes the margin. It prints a line per prediction and exits non-zero if any
one of them fails.

To check a single row by hand:

    curl -s https://api.github.com/repos/projectunmuted/newsroom/commits/COMMIT_SHA
    curl -s "https://statsapi.mlb.com/api/v1/schedule?gamePk=GAME_PK"

## The honest limits

- **90 days.** GitHub's events API only serves recent events, so
  `github-push-events.json` is a snapshot taken while they were live. After that
  window closes, the file is the only copy, and it is a file in a repository we
  control, which makes it a weaker witness than the live API. Verify early if it
  matters to you. The commit objects themselves do not expire.
- **A push proves publication, not authorship.** It shows the text was public at
  that instant. It cannot show who wrote it or how.
- **Small sample.** 18 graded games. Treat the win-loss line as a record
  being kept, not as a result.
- **This is analysis and entertainment, not betting advice.** No odds, no stakes
  and no staking guidance, here or on the site it comes from.

## Where these come from

The predictions are written and graded by an AI system at
[detroitsportsreporter.com](https://detroitsportsreporter.com), which covers the
Tigers, Lions, Pistons and Red Wings. The full source, including every commit in
this audit trail, is [projectunmuted/newsroom](https://github.com/projectunmuted/newsroom). The project's working
journal is at [project-unmuted.com](https://project-unmuted.com).

`predictions.csv` and this README are generated by `scripts/export_ledger.py` in
that repository from a cached pull, so no number here can drift from the data
beside it. Generated 2026-08-31T06:11:46Z.
