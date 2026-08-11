---
title: "Somebody said the whole season is the blown saves. So I counted the leads instead."
date: 2026-08-11
track: analysis
team: tigers
cycle: "Analysis"
summary: "Detroit has led after 7 innings 57 times and lost 11 of those games. The league holds 90.2% of those leads. At that rate the Tigers would have about 5 more wins, which puts them in first place. The claim checks out."
---

Somebody on the Tigers sub put it about as plainly as it can be put: the whole
season is that blown save number, and if it was 20 instead of 26 we'd be in
first. 25 people upvoted it. So I went and checked whether that's actually true.

Here's the thing about blown saves though. A blown save isn't a loss. You can
blow 1 in the 8th and win in the 10th, and that still goes in the column. So
counting them doesn't tell you what it cost. What tells you is the leads that
turned into losses.

So I pulled every inning of every game for all 30 teams and rebuilt the score
after 7.

**Detroit has led after 7 innings 57 times this year and lost 11 of them.**

## What everyone else does with a lead

The league held 1,436 of 1,592 leads after 7. That's 90.2%.

```svg
<svg viewBox="0 0 640 288" width="100%" role="img" aria-labelledby="lead-t" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="lead-t">Share of leads after 7 innings that each team held</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">How often a lead after 7 innings survives</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">Teams with at least 35 such leads. The line is the league rate.</text>
<line x1="445.5" y1="48" x2="445.5" y2="268" stroke="var(--rule)" stroke-width="2"/>
<text x="182" y="67" text-anchor="end" fill="var(--fg)" font-size="12">Kansas City Royals</text>
<rect x="190" y="57" width="56.0" height="15" rx="4" fill="var(--chart-neg)"><title>Kansas City Royals: held 38 of 49</title></rect>
<text x="252.0" y="69" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">77.6%</text>
<text x="182" y="93" text-anchor="end" fill="var(--fg)" font-size="12">Athletics</text>
<rect x="190" y="83" width="81.5" height="15" rx="4" fill="var(--chart-neg)"><title>Athletics: held 38 of 48</title></rect>
<text x="277.5" y="95" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">79.2%</text>
<text x="182" y="119" text-anchor="end" fill="var(--fg)" font-size="12">Detroit Tigers</text>
<rect x="190" y="109" width="105.7" height="15" rx="4" fill="var(--chart-neg)"><title>Detroit Tigers: held 46 of 57</title></rect>
<text x="301.7" y="121" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">80.7%</text>
<text x="182" y="145" text-anchor="end" fill="var(--fg)" font-size="12">Los Angeles Angels</text>
<rect x="190" y="135" width="108.0" height="15" rx="4" fill="var(--chart-neg)"><title>Los Angeles Angels: held 38 of 47</title></rect>
<text x="304.0" y="147" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">80.9%</text>
<text x="182" y="171" text-anchor="end" fill="var(--fg)" font-size="12">San Francisco Giants</text>
<rect x="190" y="161" width="147.2" height="15" rx="4" fill="var(--chart-neg)"><title>San Francisco Giants: held 45 of 54</title></rect>
<text x="343.2" y="173" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">83.3%</text>
<text x="182" y="197" text-anchor="end" fill="var(--fg)" font-size="12">San Diego Padres</text>
<rect x="190" y="187" width="377.8" height="15" rx="4" fill="var(--chart-pos)"><title>San Diego Padres: held 48 of 49</title></rect>
<text x="573.8" y="199" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">98.0%</text>
<text x="182" y="223" text-anchor="end" fill="var(--fg)" font-size="12">Texas Rangers</text>
<rect x="190" y="213" width="377.8" height="15" rx="4" fill="var(--chart-pos)"><title>Texas Rangers: held 48 of 49</title></rect>
<text x="573.8" y="225" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">98.0%</text>
<text x="182" y="249" text-anchor="end" fill="var(--fg)" font-size="12">Tampa Bay Rays</text>
<rect x="190" y="239" width="383.7" height="15" rx="4" fill="var(--chart-pos)"><title>Tampa Bay Rays: held 59 of 60</title></rect>
<text x="579.7" y="251" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">98.3%</text>
</svg>
```

| Team | Leads after 7 | Lost | Held |
|---|---|---|---|
| Royals | 49 | 11 | 77.6% |
| Athletics | 48 | 10 | 79.2% |
| **Tigers** | **57** | **11** | **80.7%** |
| Angels | 47 | 9 | 80.9% |
| Giants | 54 | 9 | 83.3% |
| League | 1,592 | 156 | 90.2% |
| Padres | 49 | 1 | 98.0% |
| Rangers | 49 | 1 | 98.0% |
| Rays | 60 | 1 | 98.3% |

*Every completed game through Aug 10, rebuilt from the linescores on the MLB
Stats API. Script's in the repo, run it yourself.*

Tampa's led after 7 60 times and lost 1. Detroit's had 3 fewer chances
and lost 11.

## What it cost, in wins

At the league rate Detroit loses about 5.6 of those 57 leads. They lost 11. So
call it **5 extra losses**, and those 5 are the whole argument.

58-60 becomes roughly 63-55. Chicago's at 61-56. That's first place, by about a
game and a half, and it's the middle of August.

So yeah, the guy was right.

## Where I'd push back on myself

A couple of things before anybody takes 63-55 as gospel.

Not every one of those 11 was a save situation. Detroit was up 5-1 after 7 on
March 31 and lost 7-5, and that's a starter and a middle reliever coming apart,
not a closer. The blown save number and the lost lead number overlap a lot but
they aren't the same list.

And you don't automatically win the ones you don't lose. Some of those games are
tied in the 9th and you're playing extras either way. The 5 wins is the ceiling
of the argument, not a promise.

There's also a thing that cuts the other direction and nobody mentions it.
Detroit has led after 7 in 57 games, which is 7th most in baseball. **They keep
getting into these positions.** The bullpen is what it is, but the rest of the
team keeps handing it leads to lose, and a team that couldn't get there wouldn't
even have the complaint.

## The narrower version

Leads after 8 are the closer's problem more cleanly. Detroit's led after 8 in 54
games and lost 5. That's better. It's still 5.

Tonight it's Bibee against Anderson, and 5 of the 6 games against Cleveland this
year came down to 1 or 2 runs. If this series turns on a 1 run game in the 8th,
now you know what the number behind that feeling actually is.
