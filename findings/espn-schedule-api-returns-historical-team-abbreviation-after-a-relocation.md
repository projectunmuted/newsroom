# ESPN's schedule API returns the historical team abbreviation after a relocation, so matching on the slug you requested silently picks the opponent

**Status: reproduced live 2026-08-28. Still current.**

## Symptom

You request a team's schedule by slug, find "your" side of each game by
comparing that slug to the abbreviation in the box score, and get back a record
that belongs partly to the opponents. No error, no warning, HTTP 200. For the
Rams the bug is worth several wins a season and it is invisible unless you
already know the right answer.

## The call

```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/lar/schedule?season=2015&seasontype=2
```

## What comes back, 2026-08-28

The root of the response says `LAR`. The competitors inside the game say `STL`.

```
requested slug: lar   season 2015
  team block abbreviation in schedule root: LAR
  first game date: 2015-09-13
   competitor id=14 abbr=STL home/away=home
   competitor id=26 abbr=SEA home/away=away
  -> matching on the string 'lar' finds: []
  -> matching on numeric id 14 finds: ['STL']
```

The endpoint accepts the *current* slug for every season it serves, but the
game objects carry the abbreviation the franchise used **at the time**. So the
lookup you requested by and the value you get back disagree, and they disagree
only for seasons before the move, which is why this survives a spot check on
recent data.

## Why it produces a wrong answer rather than an exception

The natural way to write the match is:

```python
mine = next(s for s in sides if s["team"]["abbreviation"].lower() == team)
```

That raises, so people write the forgiving version instead:

```python
mine = next((s for s in sides
             if s["team"]["abbreviation"].lower() == team), sides[0])
```

`sides[0]` is whichever competitor ESPN happened to list first, frequently the
opponent. Now every pre-relocation game is scored from the wrong side of the
box score, and `winner` is read off the other team. The result is a plausible
looking record that is wrong, which is worse than a crash.

## Affected franchises

Three, and all three are still served under their current slug:

| Slug | Historical abbreviation | Through | ESPN numeric id |
|---|---|---|---|
| `lar` | `STL` | 2015 | **14** |
| `lac` | `SD` | 2016 | **24** |
| `lv` | `OAK` | 2019 | **13** |

## The fix

**Match on `competitor["team"]["id"]`, which is stable across all three
relocations.** Resolve the slug to its numeric id once, then compare ids and
never strings.

```python
IDS = {"lar": "14", "lac": "24", "lv": "13", "det": "8", ...}

mine = next((s for s in sides if str(s["team"]["id"]) == IDS[team]), None)
if mine is None:
    raise RuntimeError(f"{team} {season}: id absent from a game it is listed in")
```

And **raise rather than falling back.** The fallback is the whole defect: if
the team you asked for is genuinely not in a game the endpoint returned for
that team, something is wrong and you want to know, not to average it in.

## How it was found

A backtest of 798 NFL team-seasons produced records for the Rams, Chargers and
Raiders that did not match the history books, while every other franchise was
correct. Anything that is wrong for exactly three teams is a lookup problem,
not a data problem.

Verified again on 2026-08-28 against a live call, along with the dataset the
fix produced:
[projectunmuted/nfl-preseason-vs-regular-season](https://github.com/projectunmuted/nfl-preseason-vs-regular-season).
