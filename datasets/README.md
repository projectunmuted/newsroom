# Does an NFL team's preseason record predict its regular season?

**No. It explains 1.1% of the variance.**

This repository is the data behind that answer: **798 team-seasons**, every NFL team's preseason and regular-season record for **25 seasons, 2000 to 2025**, pulled from ESPN's public schedule endpoint and cross-checked against live calls.

- **[`nfl-preseason-vs-regular-season-2000-2025.csv`](nfl-preseason-vs-regular-season-2000-2025.csv)** is the dataset, one row per team-season.
- **[`excluded-games.json`](excluded-games.json)** is every fixture dropped and why, so the exclusions are auditable rather than implied.
- **[`nfl-preseason-2026.csv`](nfl-preseason-2026.csv)** is the 2026 preseason, finished 2026-08-29, with each team's historical base rate attached.

Free to use for anything, with attribution. No API key, no signup, no scraper to maintain.

## The 2026 preseason, and what the history says about it

The 2026 preseason finished **2026-08-29**. Every team's record is in **[`nfl-preseason-2026.csv`](nfl-preseason-2026.csv)**, with the historical base rate for its bucket attached to each row.

| 2026 preseason | Teams | Historical mean regular-season win rate | n |
|---|---|---|---|
| Won every preseason game | Ravens (3-0), Bills (3-0), Bengals (3-0), Rams (3-0) | 0.475 | 68 |
| Winning preseason | Panthers (3-1), Falcons (2-1), Bears (2-1), Cowboys (2-1), Broncos (2-1), Lions (2-1), Packers (2-1), Jaguars (2-1), Giants (2-1), 49ers (2-1), Buccaneers (2-1), Titans (2-1) | 0.538 | 226 |
| Even preseason | Patriots (1.5-1.5) | 0.521 | 217 |
| Losing preseason | Browns (1-2), Chargers (1-2), Raiders (1-2), Vikings (1-2), Saints (1-2), Jets (1-2), Steelers (1-2), Commanders (1-2), Cardinals (1-3), Colts (0.5-2.5), Chiefs (0.5-2.5), Seahawks (0.5-2.5) | 0.458 | 217 |
| Lost every preseason game | Texans (0-3), Dolphins (0-3), Eagles (0-3) | 0.473 | 70 |

So the 4 unbeaten teams above are the group that historically finished **0.475**, which is *below* .500. If you are about to write that your team is peaking, the 68 previous unbeaten preseasons disagree.

And the 3 winless teams join the group that finished **0.473**, which is almost the same number. That is the whole finding: the two extremes of August are separated by 0.002 of regular-season win rate, which is 0.03 games over a 17-game schedule.

**Why Carolina Panthers and Arizona Cardinals played 4 games and everybody else played 3:** the Hall of Fame Game. It is a preseason fixture and it counts, so a check that asserts 3 games a team fails on exactly these 2 every year. Noted because it is the kind of thing that turns into a silent exclusion.

**These rows are deliberately not in the historical CSV.** They have no regular season yet. Adding them with blank outcome columns is how a correlation quietly acquires 32 rows of nothing; they get their regular-season columns when 2026 finishes.

## The answer, in one table

Correlation between preseason win rate and regular-season win rate across all 798 rows: **r = +0.106**, so preseason record explains **1.1%** of what happens next.

| Preseason | n | Mean regular-season win rate | vs. .500 |
|---|---|---|---|
| Won every preseason game | 68 | 0.475 | -0.025 |
| Winning preseason | 226 | 0.538 | +0.038 |
| Even preseason | 217 | 0.521 | +0.021 |
| Losing preseason | 217 | 0.458 | -0.042 |
| Lost every preseason game | 70 | 0.473 | -0.027 |

The interesting part is the top row. Teams that went **undefeated** in the preseason went on to be **worse than .500**, not better. Going unbeaten in August was a slightly negative signal, and the best preseason bucket in the whole table is merely *winning*, not perfect.

## The tails

68 undefeated preseasons and 70 winless ones in the sample.

**Worst regular seasons that followed an undefeated preseason:**

| Team | Season | Preseason | Regular season |
|---|---|---|---|
| Detroit Lions | 2008 | 4-0 | **0-16** |
| Cleveland Browns | 2017 | 4-0 | **0-16** |
| Los Angeles Chargers | 2000 | 4-0 | **1-15** |
| Los Angeles Rams | 2011 | 4-0 | **2-14** |
| Chicago Bears | 2022 | 3-0 | **3-14** |

**Best regular seasons that followed an undefeated preseason**, because a table of only the disasters would be the same cherry-picking this dataset exists to make unnecessary:

| Team | Season | Preseason | Regular season |
|---|---|---|---|
| New England Patriots | 2003 | 4-0 | 14-2 |
| Baltimore Ravens | 2019 | 4-0 | 14-2 |
| Minnesota Vikings | 2024 | 3-0 | 14-3 |
| Denver Broncos | 2025 | 3-0 | 14-3 |
| Denver Broncos | 2005 | 4-0 | 13-3 |

## Schema

| Column | Type | Notes |
|---|---|---|
| `season` | int | 2000 to 2025. **2020 is absent**: no preseason was played. |
| `team` | str | ESPN's team slug, e.g. `det`. Constant across relocations, so the Rams are `lar` in every season including the St Louis ones. |
| `team_name` | str | Current franchise name. |
| `preseason_wins` | float | **Ties count as half a win.** |
| `preseason_games` | float | Games actually played and finished. **The preseason shortened from 4 games to 3 in 2021**, so an unbeaten preseason is 4-0 in the older rows and 3-0 in the newer ones. |
| `preseason_win_pct` | float | `preseason_wins / preseason_games`. |
| `regular_wins` | float | Ties count as half a win. |
| `regular_games` | float | 16 through 2020, 17 from 2021. |
| `regular_win_pct` | float | `regular_wins / regular_games`. |

32 franchises. 2000 and 2001 carry 31 rows rather than 32 because the Houston Texans did not exist until 2002.

## Three corrections already made, and they are the reason to use this rather than re-scrape it

Each of these was a wrong number that a reasonable scrape produces and that nothing warns you about. All three were found the expensive way.

**1. The window was not the data floor.** An earlier version of this analysis ran 2015 to 2025 and described that as the limit of ESPN's coverage. It is not: the endpoint serves preseason schedules back to 2000, and 1999 and earlier return zero events. The short window excluded the 2008 Lions, who went 4-0 in the preseason and 0-16, which is the single most famous case of the very claim being tested. A reader pointed this out and was right.

**2. Three franchises were being counted as their opponents.** ESPN answers `/teams/lar/` for every season, but the box score inside carries the *historical* abbreviation, so a 2015 Rams game says `STL`. Code that finds its own side by matching the requested abbreviation matches nothing and falls back to the first competitor listed, which is frequently the opponent. The same applies to the Chargers (`SD` through 2016) and the Raiders (`OAK` through 2019). **Match on ESPN's numeric team id instead**, which is stable across all three relocations: Rams 14, Chargers 24, Raiders 13.

**3. Never-played fixtures come back as 0-0, not null.** Older seasons carry them with a final-looking score of 0-0, and a 0-0 scores as a tie, which is half a win to both sides. Detroit's 2001 season came back **2.5-13.5** against a real 2-14 because of a phantom Detroit-St Louis fixture dated 2001-10-09. **No NFL game has finished 0-0 since 1943**, so treating a 0-0 as unplayed costs nothing real. 82 such fixtures across 56 team-seasons were dropped; every one is listed in `excluded-games.json`.

## Known limitation: 40 rows have a short denominator

This follows from correction 3 and is the one thing to know before using the data for something else.

When ESPN serves a phantom 0-0 fixture it is usually serving it **in place of** a real game rather than in addition to one, so dropping it leaves that team-season a game short. Detroit 2001 is the worked example: counting the 0-0 as a tie gives 2.5-13.5 over 16, dropping it gives **2-13 over 15**, and the real record is 2-14. Dropping it fixes the wins and leaves the denominator one short.

**40 of 798 rows (5.0%) carry fewer regular-season games than that season's schedule length.** Every one of them is explained by a fixture in `excluded-games.json`; there are no unexplained short rows. The distribution is 13 games: 5 rows, 14 games: 16 rows, 15 games: 17 rows, 16 games: 2 rows.

**It does not move the answer**, and the check is worth showing rather than asserting. Restricting to the 756 rows with a complete schedule:

| Sample | n | r | Variance explained | Undefeated-preseason mean |
|---|---|---|---|---|
| All rows | 798 | +0.106 | 1.1% | 0.475 |
| Complete schedules only | 756 | +0.095 | 0.9% | 0.474 |

Both say the same thing. If you are computing win *rates*, as the headline above does, the effect is immaterial. If you need exact win *totals* for a specific team-season, check it against a second source first.

## Provenance

Source: ESPN's public schedule endpoint, no key required.

```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team}/schedule?season={season}&seasontype={1|2}
```

`seasontype=1` is preseason, `seasontype=2` is regular season. Only games with a final status and two numeric scores are counted.

**Last verified against live calls: 2026-08-30.** 4 team-seasons were re-fetched live and matched the cache exactly: DET 2008 (preseason 4-0, regular 0-16), LAR 2011, LAC 2000 and LV 2015. The last 3 are the relocation franchises that correction 2 above is about. On 2026-08-30 all 32 rows of the 2026 file were fetched live and every listed fixture came back final.

The code that produced this, and the full derivation including the subsample breakdowns, is `scripts/preseason_full.py` in the newsroom repo. This file and the CSV beside it are both generated by `scripts/export_dataset.py`; nothing here is edited by hand, so the prose cannot drift from the numbers.

## Where this came from

It is a by-product of [Detroit Sports Reporter](https://detroitsportsreporter.com), where predictions get committed before games and graded after, and of the project journal at [project-unmuted.com](https://project-unmuted.com).

If you use the data, a link back is appreciated and not required.
