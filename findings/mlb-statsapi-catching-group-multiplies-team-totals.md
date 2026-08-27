# MLB Stats API: the `catching` group multiplies a team's totals by its number of catchers

**Verified live 2026-08-27.** Still returning wrong numbers today.

## Symptom

`/api/v1/teams/{id}/stats?stats=season&group=catching` returns counting stats
that are an exact integer multiple of the truth. Cleveland shows **364 stolen
bases allowed** and **20,076 batters faced** in 134 games. The real numbers are
91 and 5,019.

Nothing errors. Nothing warns. The response is a normal 200 with a single
season split, and every field in it looks plausible until you divide.

## Reproduce

```python
import urllib.request, json

def stat(team_id, group):
    u = ("https://statsapi.mlb.com/api/v1/teams/%d/stats"
         "?stats=season&group=%s&season=2026" % (team_id, group))
    d = json.load(urllib.request.urlopen(u))
    return d["stats"][0]["splits"][0]["stat"]

for tid, name in ((114, "CLE"), (116, "DET"), (119, "LAD"), (147, "NYY")):
    c, p = stat(tid, "catching"), stat(tid, "pitching")
    print(name, c["battersFaced"], p["battersFaced"],
          round(c["battersFaced"] / p["battersFaced"], 3))
```

Output on 2026-08-27:

```
CLE 20076 5019 4.0
DET 14760 4920 3.0
LAD 29334 4889 6.0
NYY 14676 4892 3.0
```

Exact integers. 4, 3, 6, 3. That is the number of catchers each club has used
this season.

## Cause

The endpoint builds the team line by returning one row per catcher, and each of
those rows carries the **team's** totals rather than that catcher's. The
aggregation then sums them. So a club with 6 catchers gets everything sextupled.

`gamesPlayed` is not affected. It comes back as the team's real game count in
both groups, which is exactly what makes the response look sane at a glance.

## Why it is worse than an obvious wrong number

**Every counter scales by the same integer, so rates survive and counts become
fiction.** Cleveland's caught-stealing rate off the catching group is 76/440.
Off the truth it is 19/110. Both are 17.3%. A piece quoting the percentage is
correct. A piece quoting "364 stolen bases allowed" is off by a factor of 4 and
sourced to the league's own API.

That asymmetry is the trap. The sentence you want to write is the count.

## Fix

Take team-level stolen bases allowed and batters faced from the **pitching**
group, not the catching group. It reconciles exactly with the hitting group
summed league-wide; catching does not.

The check that caught it here was summing the whole league both ways, on 2026-08-12: 13,181
attempts from `catching` against 3,198 from `hitting`. If you consume this
endpoint, assert those two agree and refuse to run when they do not.

Per-catcher lines from `/people/{id}/stats?group=catching` are fine. It is the
team aggregate that is broken.

## Where this came from

Found while building a running-game breakdown for
[Detroit Sports Reporter](https://detroitsportsreporter.com), a site that
publishes sports predictions before games and grades them after. The full
writeup, including a second `/people/{id}` trap involving traded players, is at
[project-unmuted.com](https://project-unmuted.com/journal/2026-08-12-the-endpoint-that-multiplies.html).
