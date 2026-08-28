# ESPN's schedule API serves never-played games as 0-0 with STATUS_FINAL and completed=true, so they score as ties

**Status: reproduced live 2026-08-28. Still current.**

## Symptom

A team's win-loss record comes back with a `.5` in it for a season that had no
tie. Nothing errors. The extra half-win comes from a fixture that was never
played, served with a final status and a score of 0-0, which any reasonable
tie-detection reads as a tie.

## The call

```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/det/schedule?season=2001&seasontype=2
```

## What comes back, 2026-08-28

```
DET 2001 regular season events: 16
  0-0 fixture: ('2001-10-09', ['DET', 'STL'], 'STATUS_FINAL', True)
```

That fixture is dated **Tuesday 9 October 2001**. The NFL does not play on
Tuesdays, and Detroit did not play St Louis that day. It is a placeholder,
almost certainly an artifact of the schedule being rebuilt after the September
2001 postponements, and it is served with `status.type.name` of
`STATUS_FINAL` and `status.type.completed` of `true`.

## The arithmetic it produces

```
counting the 0-0 as a tie   : 2.5-13.5 over 16 games
treating the 0-0 as unplayed: 2-13 over 15 games
real 2001 Detroit Lions record: 2-14
```

## Why the obvious guards do not catch it

- **Checking the status does not help.** It says final and completed.
- **Checking for null scores does not help.** The scores are present and
  numeric, they are just both zero.
- **The result stays plausible.** 2.5-13.5 looks like a bad season, which 2001
  was, so nothing about the output invites a second look.

## The fix

**Treat a 0-0 as unplayed.** No NFL game has finished 0-0 since 1943, so the
rule costs nothing real and catches every one of these:

```python
scores = [s.get("score", {}).get("value") for s in sides]
if any(v is None for v in scores):
    continue                      # unplayed or cancelled
if scores[0] == 0 and scores[1] == 0:
    continue                      # never-played fixture served as a final 0-0
```

**Log every one you drop** rather than dropping silently, so the exclusions can
be audited later. Across 2000-2025 this rule dropped **82 fixtures over 56
team-seasons**.

## The part worth knowing before you use the fix

The placeholder usually stands in **for** a real game rather than in addition
to one, so dropping it leaves that team-season a game short: Detroit 2001 ends
up 2-13 over 15 rather than the true 2-14. The fix gets the wins right and
leaves the denominator one low.

In a 798-row NFL dataset built this way, **40 rows (5.0%) end up with fewer
games than the season's schedule length**, all traceable to a dropped fixture.
For win *rates* the effect is immaterial. For exact win *totals* on a specific
team-season, check against a second source.

## How it was found

A 25-season backtest reported Detroit at 2.5-13.5 for 2001. A half-win in a
season with no ties is not a rounding artifact, it is a game that should not be
in the sample.

Verified again on 2026-08-28 against a live call. The dataset, with the full
exclusion list in `excluded-games.json`:
[projectunmuted/nfl-preseason-vs-regular-season](https://github.com/projectunmuted/nfl-preseason-vs-regular-season).
