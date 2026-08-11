---
title: "The Wings got handed the hardest schedule in hockey, and it barely matters"
date: 2026-08-11
track: analysis
team: redwings
cycle: "Analysis"
summary: "Detroit plays 45 games against last season's playoff teams, tied for most in the NHL. Then you look at the spread and the whole league fits inside 3.5 points of opponent quality. The number that actually should worry you is 92 points on a minus 17 goal differential."
---

The Wings don't play until October 2, home to the Rangers. But the 2026-27
schedule is out, all 84 games of it, so I pulled the whole thing for all 32
teams and scored it. Nobody writes this piece in August, which is exactly why
it's worth writing.

First thing worth knowing: it's 84 games now, not 82. That's what the league's
own schedule feed says for every team.

## The headline, which I don't really believe

Detroit plays **45 games against teams that made the 2026 playoffs**. That's the
most in the NHL. League average is 42.

Sounds brutal. Then you look at who else is on 45, and it's Florida and Toronto,
and suddenly it isn't a curse, it's an address. Those are the 3 Atlantic teams
that missed the playoffs last year, and the Atlantic sent 5 of its 8 to the
postseason. Buffalo, Tampa, Montreal, Boston, Ottawa. You play each of your
division 4 times, so that's 20 of your 45 before anybody sits down to make a
schedule.

The formula does the rest. 4 games against each of the 7 division rivals, 3
against each of the 8 in the Metro, 2 against each of the 16 out west. 28 plus
24 plus 32 is 84. There's almost no room in there for the league to do anything
to you.

Here's what that looks like when you put every team on the same axis. Average
points their opponents earned last season, weighted by how often they meet:

```svg
<svg viewBox="0 0 640 176" width="100%" role="img" aria-labelledby="nhl-sos-t" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="nhl-sos-t">Every NHL team's 2026-27 schedule strength, plotted as average opponent points from last season. All 32 teams fall between 90.4 and 93.9, with Detroit at 93.2.</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">Every team's 2026-27 schedule, on one axis</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">Average points each team's opponents earned last season. 32 dots. The whole league fits in 3.5 points.</text>
<line x1="40" y1="118" x2="600" y2="118" stroke="var(--rule)" stroke-width="1"/>
<line x1="40.0" y1="118" x2="40.0" y2="123" stroke="var(--rule)" stroke-width="1"/>
<text x="40.0" y="137" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">90</text>
<line x1="180.0" y1="118" x2="180.0" y2="123" stroke="var(--rule)" stroke-width="1"/>
<text x="180.0" y="137" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">91</text>
<line x1="320.0" y1="118" x2="320.0" y2="123" stroke="var(--rule)" stroke-width="1"/>
<text x="320.0" y="137" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">92</text>
<line x1="460.0" y1="118" x2="460.0" y2="123" stroke="var(--rule)" stroke-width="1"/>
<text x="460.0" y="137" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">93</text>
<line x1="600.0" y1="118" x2="600.0" y2="123" stroke="var(--rule)" stroke-width="1"/>
<text x="600.0" y="137" text-anchor="middle" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums">94</text>
<line x1="346.2" y1="60" x2="346.2" y2="118" stroke="var(--rule)" stroke-width="2" stroke-dasharray="3 3"/>
<text x="346.2" y="55" text-anchor="middle" fill="var(--muted)" font-size="11">league average 92.19</text>
<circle cx="585.0" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>TOR: 93.89</title></circle>
<circle cx="553.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>NYR: 93.67</title></circle>
<circle cx="545.0" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>FLA: 93.61</title></circle>
<circle cx="491.7" cy="108" r="6" fill="var(--chart-neg)"><title>Detroit: 93.23, rank 4 of 32</title></circle>
<line x1="491.7" y1="72" x2="491.7" y2="101" stroke="var(--chart-neg)" stroke-width="1"/>
<text x="491.7" y="69" text-anchor="middle" fill="var(--fg)" font-size="11" font-weight="700">DET</text>
<circle cx="486.7" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>NJD: 93.19</title></circle>
<circle cx="460.0" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>NYI: 93.00</title></circle>
<circle cx="453.3" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>CBJ: 92.95</title></circle>
<circle cx="445.0" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>OTT: 92.89</title></circle>
<circle cx="438.3" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>BOS: 92.85</title></circle>
<circle cx="433.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>WSH: 92.81</title></circle>
<circle cx="426.7" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>CHI: 92.76</title></circle>
<circle cx="413.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>PHI: 92.67</title></circle>
<circle cx="413.3" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>PIT: 92.67</title></circle>
<circle cx="398.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>MTL: 92.56</title></circle>
<circle cx="398.3" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>TBL: 92.56</title></circle>
<circle cx="378.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>BUF: 92.42</title></circle>
<circle cx="378.3" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>VAN: 92.42</title></circle>
<circle cx="360.0" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>WPG: 92.29</title></circle>
<circle cx="333.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>NSH: 92.10</title></circle>
<circle cx="333.3" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>STL: 92.10</title></circle>
<circle cx="313.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>CAR: 91.95</title></circle>
<circle cx="293.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>UTA: 91.81</title></circle>
<circle cx="251.7" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>CGY: 91.51</title></circle>
<circle cx="238.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>SEA: 91.42</title></circle>
<circle cx="213.3" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>MIN: 91.24</title></circle>
<circle cx="191.7" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>SJS: 91.08</title></circle>
<circle cx="165.0" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>LAK: 90.89</title></circle>
<circle cx="160.0" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>DAL: 90.86</title></circle>
<circle cx="151.7" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>ANA: 90.80</title></circle>
<circle cx="145.0" cy="97" r="4" fill="var(--muted)" opacity="0.55"><title>EDM: 90.75</title></circle>
<circle cx="131.7" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>VGK: 90.65</title></circle>
<circle cx="100.0" cy="108" r="4" fill="var(--muted)" opacity="0.55"><title>COL: 90.43</title></circle>
<text x="0" y="170" fill="var(--muted)" font-size="11">Detroit 93.23, rank 4 of 32. Hardest TOR 93.89, easiest COL 90.43.</text>
</svg>
```

| | Average opponent points |
|---|---|
| Toronto, hardest | 93.89 |
| NY Rangers | 93.67 |
| Florida | 93.61 |
| **Detroit, 4th** | **93.23** |
| League average | 92.19 |
| Edmonton | 90.75 |
| Vegas | 90.65 |
| Colorado, easiest | 90.43 |

Toughest schedule in the league to easiest is 3.5 points of opponent quality.
Detroit sits about 1 point above average. Over 84 games that's real but it's not
the story, and if the Wings miss by 2 points in April I don't think you get to
point at this.

## The number in their favour is bigger than the one against

This is the part I didn't expect. Detroit travels **35,625 miles** next season,
counting great circle distance between arenas and the trips home at each end.
That's 4th least in the league. Only Pittsburgh, Buffalo and Philly move less.

League average is 42,464. Seattle does 51,973.

So the Wings will be about 6,800 miles fresher than a typical team and roughly
16,000 fresher than Seattle. In a sport where the whole conversation in March is
about legs, that's a bigger edge than 1 point of opponent quality is a
disadvantage.

The rest of the fatigue picture is unremarkable. 12 back-to-backs, which is
right in the middle, and only 2 of those are the bad kind where they're on the
second night and the other team's had at least 2 days off. Longest road trip is 5,
longest homestand is 4. 42 home, 42 away.

## What should actually worry you

92 points last season. 41-31-10. And a goal differential of **minus 17**.

Those don't normally go together. Fit points against goal differential across
all 32 teams and the line is tight, 91% of the variation, typical miss under 4
points. Detroit finished **5.0 points above** what its goals said it should
have, 3rd most in the league behind San Jose and Montreal.

Now the honest version of that, because 3rd of 32 sounds worse than it is: the
typical team misses the line by 3.9 points, so 5.0 is barely outside ordinary.
It's not a scandal. It's a nudge.

But it's a nudge in the wrong direction, and the gap is what makes it sting. The
last Eastern wild card was Ottawa at 99. Detroit had 92. That's 7 points short,
and if you think even a few of those 92 were borrowed, the real climb is closer
to 10 or 12.

You don't get 12 points out of a friendly travel map. You get it from scoring
more than you give up, and 241 for and 258 against is a team that didn't.

## The thing hanging over all of it

I can't write about the Wings today and skip this. Yzerman's moving to a senior
advisor role and there's an actual GM search running, with an outside firm doing
it and Shawn Horcoff handling the day to day in the meantime. Reporting says
they're prioritizing somebody with a heavy analytics background and might not
decide until September.

Which is a little funny given everything above. The next guy is being hired
partly to know the difference between a number that means something and a number
that just looks scary, and the schedule is about to hand him a great example of
the second kind. 45 games against playoff teams is going to get quoted all
season. Minus 17 is the one that decides anything.

I'd hold off on reading much into the schedule until we know who's reading it.

## What I'll be watching

Goal differential through American Thanksgiving. Not points, not the standings,
not whatever a hot October does to everyone's mood. If they're plus by then, the
schedule stuff above is noise and this is a playoff team. If they're 12-8-3 with
a minus 6, that's last season again and the travel savings won't cover it.

I'll take the under on the schedule being the reason, either way.

*Everything above comes from the NHL's public API: the 2026-27 schedule for all
32 clubs and the final 2025-26 standings. The script that derives every number
here, including the chart, is `scripts/nhl_schedule.py` in the repository.
Arena coordinates were entered by hand because the league doesn't publish them,
and travel is great circle miles between arenas, which isn't the same as flight
miles.*
