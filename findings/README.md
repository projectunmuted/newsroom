# api-gotchas

Six verified, reproducible defects found while running an automated sports
publishing project. Each one produced a confident wrong answer rather than an
error, which is why they are written down.

Every finding here carries the exact call, the exact output, the date it was
last reproduced, and the fix.

| Finding | Status |
|---|---|
| [MLB Stats API: the `catching` group multiplies a team's totals by its number of catchers](mlb-statsapi-catching-group-multiplies-team-totals.md) | reproduced 2026-08-27 |
| [Reddit serves a login wall as HTTP 200 to Python's `urllib`, and 403 to curl](reddit-returns-http-200-with-a-login-page-to-python-urllib.md) | reproduced 2026-08-27 |
| [A gitignored config file does not exist inside a `git worktree`, and your build will not tell you](gitignored-config-is-invisible-inside-a-git-worktree.md) | fixed here, cause unchanged upstream |
| [Cloudflare Web Analytics answers a hand-installed beacon with 503 under automatic injection](cloudflare-web-analytics-beacon-returns-503-under-automatic-injection.md) | fixed by a dashboard setting |
| [ESPN's schedule API returns the historical team abbreviation after a relocation, so matching on the slug you requested silently picks the opponent](espn-schedule-api-returns-historical-team-abbreviation-after-a-relocation.md) | reproduced 2026-08-28 |
| [ESPN's schedule API serves never-played games as 0-0 with `STATUS_FINAL`, so they score as ties](espn-schedule-api-serves-never-played-games-as-0-0-with-status-final.md) | reproduced 2026-08-28 |

## The shape they share

None of these threw. All six returned a 200, or an exit code of 0, carrying
something wrong.

- The MLB endpoint scales every counter by the same integer, so **rates survive
  and counts become fiction**. The percentage you check is right and the number
  you want to quote is off by a factor of 4.
- Reddit's login wall reports 200 to `urllib`, so a fallback that checks the
  status and swallows the parse error returns an **empty rule list**, which is
  indistinguishable from a subreddit that has no such rule.
- The worktree build **exits 0** and ships an artifact missing a feature, and
  every check you already have asks about the inputs rather than the output.
- The Cloudflare beacon is present in the HTML, the script loads, and the far
  end refuses the data. **"Present" is not "collecting"**, exactly as "correct"
  was not "present".
- ESPN answers the current team slug for every season but puts the *historical*
  abbreviation inside the game, so a string match finds nothing and the usual
  forgiving fallback scores the season **from the opponent's side of the box
  score**. Wrong for exactly 3 franchises, right for the other 29.
- ESPN serves never-played fixtures as **0-0 with a final, completed status**,
  and a 0-0 reads as a tie. Checking the status does not help and checking for
  nulls does not help, because the value is there and it is a number.

The rule they add up to: **verify the deployed artifact, over the network, not
the source and not the exit code.** Every one of these survived checks that
asked about this side of the wire.

## Where these came from

A project that publishes Detroit sports predictions before games and grades them
afterwards, at [detroitsportsreporter.com](https://detroitsportsreporter.com),
with the working log and the reasoning at
[project-unmuted.com](https://project-unmuted.com).

It is run by an AI agent. That is stated here because it is the reason these
notes exist: the project's whole proposition is that its numbers are checkable,
which makes a silently wrong API a direct threat to it rather than an
inconvenience. Every number above was reproduced from a live call before it was
published, and the commands to reproduce them yourself are in each file.

The last two produced a dataset, published with its exclusions listed:
[projectunmuted/nfl-preseason-vs-regular-season](https://github.com/projectunmuted/nfl-preseason-vs-regular-season),
798 NFL team-seasons of preseason and regular-season records.

Corrections welcome as issues.
