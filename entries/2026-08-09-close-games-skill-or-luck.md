---
title: "Are the Tigers bad at close games, or unlucky? Five seasons say both, and mostly the second one"
date: 2026-08-09
track: analysis
team: tigers
cycle: "Analysis"
summary: "Readers pushed back on the regression argument: losing close games might be who this team is, not luck waiting to reverse. That is testable. Across 150 team-seasons, a close-game record carries about 61 percent of the repeatable signal an ordinary stretch of schedule carries. Not zero, and not close to all of it. For Detroit it is worth about two wins over the last 45 games, and the reader objection that actually survives is a different one."
---

Last week I wrote that the Tigers were the best team in the AL Central and in
fourth place, and that the gap between their record and their run differential
was a promise the rest of the season would keep.

The comments on that piece were better than the piece. The sharpest one said
the reasoning was not just optimistic but conceptually wrong: run differential
and Pythagorean expectation get read as a guarantee of regression, and they are
not. Blowing out the Athletics does not put a run in the bank. A team that
keeps losing one-run games might simply be a team that is bad at one-run games,
and calling that luck is just refusing to look at it.

That is a real argument and I did not test it before publishing. So here it is,
tested, with the answer up front: **the reader is right about the mechanism and
wrong about the size.** Close-game performance is partly a real, repeatable
property of a team. It is roughly 61 percent as repeatable as an equal number
of ordinary games. That leaves Detroit better than its close-game record but
worse than the pure-regression story implies, and it moves the projection by
about two wins rather than the seven the Pythagorean gap advertises.

## What Detroit's season actually looks like split by margin

| Split | Record | Win rate |
|---|---|---|
| Overall | 57-60 | .487 |
| Decided by 3 runs or fewer | **26-44** | **.371** |
| One-run games | 12-20 | .375 |
| Decided by 4 or more | **31-16** | **.660** |
| vs AL Central | 11-18 | .379 |

*Every game Detroit has played through the final whistle on August 8, from
the MLB Stats API, regular season only.*

A reader also corrected the framing I used, and the correction was an
improvement. I had leaned on the 12-20 one-run split. The better number is
26-44 in games decided by three or fewer: same story, 70 games instead of 32.
Their figure was 26-45 and the true one is 26-44, off by a single loss, which
is closer than most published numbers get.

That 31-16 in blowouts is the part nobody talks about. Detroit beats good teams
badly and loses to bad teams narrowly, and the distance between those two
things is not normal.

```svg
<svg viewBox="0 0 640 763" width="100%" role="img" aria-labelledby="gap-title" style="max-width:640px;height:auto;font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif">
<title id="gap-title">Win rate in blowouts minus win rate in games decided by 3 or fewer, all 30 teams, 2026</title>
<text x="0" y="16" fill="var(--fg)" font-size="13" font-weight="600">Blowout win rate minus close-game win rate</text>
<text x="0" y="34" fill="var(--muted)" font-size="11">Right of the line means a team wins when the game is not close and loses when it is. Close = games decided by 3 or fewer.</text>
<line x1="343.4" y1="44" x2="343.4" y2="737.0" stroke="var(--rule)" stroke-width="2"/>
<text x="138" y="62.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="700">Detroit Tigers</text>
<path d="M344.9098337094614,50H562.210016780442A3.0,3.0 0 0 1 565.210016780442,53.0V63.0A3.0,3.0 0 0 1 562.210016780442,66H344.9098337094614Z" fill="var(--chart-pos)" opacity="1"><title>Detroit Tigers: 0.660 in 47 blowouts, 0.371 in 70 close games (+0.288)</title></path>
<text x="572.2" y="62.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="700">+0.288</text>
<text x="138" y="85.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Chicago Cubs</text>
<path d="M344.9098337094614,73H473.6357226402415A3.0,3.0 0 0 1 476.6357226402415,76.0V86.0A3.0,3.0 0 0 1 473.6357226402415,89H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Chicago Cubs: 0.673 in 52 blowouts, 0.500 in 66 close games (+0.173)</title></path>
<text x="483.6" y="85.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.173</text>
<text x="138" y="108.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Pittsburgh Pirates</text>
<path d="M344.9098337094614,96H449.53058389809405A3.0,3.0 0 0 1 452.53058389809405,99.0V109.0A3.0,3.0 0 0 1 449.53058389809405,112H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Pittsburgh Pirates: 0.564 in 55 blowouts, 0.422 in 64 close games (+0.142)</title></path>
<text x="459.5" y="108.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.142</text>
<text x="138" y="131.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Milwaukee Brewers</text>
<path d="M344.9098337094614,119H441.0154019800539A3.0,3.0 0 0 1 444.0154019800539,122.0V132.0A3.0,3.0 0 0 1 441.0154019800539,135H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Milwaukee Brewers: 0.702 in 47 blowouts, 0.571 in 70 close games (+0.131)</title></path>
<text x="451.0" y="131.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.131</text>
<text x="138" y="154.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Atlanta Braves</text>
<path d="M344.9098337094614,142H425.2968117196304A3.0,3.0 0 0 1 428.2968117196304,145.0V155.0A3.0,3.0 0 0 1 425.2968117196304,158H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Atlanta Braves: 0.660 in 47 blowouts, 0.549 in 71 close games (+0.110)</title></path>
<text x="435.3" y="154.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.110</text>
<text x="138" y="177.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Boston Red Sox</text>
<path d="M344.9098337094614,165H421.06589697117306A3.0,3.0 0 0 1 424.06589697117306,168.0V178.0A3.0,3.0 0 0 1 421.06589697117306,181H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Boston Red Sox: 0.612 in 49 blowouts, 0.507 in 67 close games (+0.105)</title></path>
<text x="431.1" y="177.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.105</text>
<text x="138" y="200.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Los Angeles Dodgers</text>
<path d="M344.9098337094614,188H412.1602470944044A3.0,3.0 0 0 1 415.1602470944044,191.0V201.0A3.0,3.0 0 0 1 412.1602470944044,204H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Los Angeles Dodgers: 0.647 in 51 blowouts, 0.554 in 65 close games (+0.093)</title></path>
<text x="422.2" y="200.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.093</text>
<text x="138" y="223.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Miami Marlins</text>
<path d="M344.9098337094614,211H409.53498629522727A3.0,3.0 0 0 1 412.53498629522727,214.0V224.0A3.0,3.0 0 0 1 409.53498629522727,227H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Miami Marlins: 0.556 in 45 blowouts, 0.466 in 73 close games (+0.090)</title></path>
<text x="419.5" y="223.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.090</text>
<text x="138" y="246.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">New York Yankees</text>
<path d="M344.9098337094614,234H401.52008994379594A3.0,3.0 0 0 1 404.52008994379594,237.0V247.0A3.0,3.0 0 0 1 401.52008994379594,250H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>New York Yankees: 0.614 in 44 blowouts, 0.534 in 73 close games (+0.079)</title></path>
<text x="411.5" y="246.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.079</text>
<text x="138" y="269.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Los Angeles Angels</text>
<path d="M344.9098337094614,257H377.45660496294033A3.0,3.0 0 0 1 380.45660496294033,260.0V270.0A3.0,3.0 0 0 1 377.45660496294033,273H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Los Angeles Angels: 0.412 in 51 blowouts, 0.364 in 66 close games (+0.048)</title></path>
<text x="387.5" y="269.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.048</text>
<text x="138" y="292.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Arizona Diamondbacks</text>
<path d="M344.9098337094614,280H357.6148916934459A3.0,3.0 0 0 1 360.6148916934459,283.0V293.0A3.0,3.0 0 0 1 357.6148916934459,296H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Arizona Diamondbacks: 0.543 in 46 blowouts, 0.521 in 71 close games (+0.022)</title></path>
<text x="367.6" y="292.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.022</text>
<text x="138" y="315.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Baltimore Orioles</text>
<path d="M344.9098337094614,303H351.2792116111026A3.0,3.0 0 0 1 354.2792116111026,306.0V316.0A3.0,3.0 0 0 1 351.2792116111026,319H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Baltimore Orioles: 0.488 in 41 blowouts, 0.474 in 76 close games (+0.014)</title></path>
<text x="361.3" y="315.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.014</text>
<text x="138" y="338.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">New York Mets</text>
<path d="M344.9098337094614,326H349.9293137097562A3.0,3.0 0 0 1 352.9293137097562,329.0V339.0A3.0,3.0 0 0 1 349.9293137097562,342H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>New York Mets: 0.439 in 57 blowouts, 0.426 in 61 close games (+0.012)</title></path>
<text x="359.9" y="338.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.012</text>
<text x="138" y="361.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Chicago White Sox</text>
<path d="M344.9098337094614,349H349.88367470009473A3.0,3.0 0 0 1 352.88367470009473,352.0V362.0A3.0,3.0 0 0 1 349.88367470009473,365H344.9098337094614Z" fill="var(--chart-pos)" opacity="0.62"><title>Chicago White Sox: 0.520 in 50 blowouts, 0.508 in 65 close games (+0.012)</title></path>
<text x="359.9" y="361.0" text-anchor="start" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">+0.012</text>
<text x="138" y="384.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Seattle Mariners</text>
<path d="M341.9098337094614,372H342.93846225784546V388H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Seattle Mariners: 0.478 in 46 blowouts, 0.479 in 71 close games (-0.001)</title></path>
<text x="335.9" y="384.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.001</text>
<text x="138" y="407.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">San Francisco Giants</text>
<path d="M341.9098337094614,395H342.5126896762575V411H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>San Francisco Giants: 0.423 in 52 blowouts, 0.424 in 66 close games (-0.001)</title></path>
<text x="335.5" y="407.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.001</text>
<text x="138" y="430.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Kansas City Royals</text>
<path d="M341.9098337094614,418H328.6463818520241A3.0,3.0 0 0 0 325.6463818520241,421.0V431.0A3.0,3.0 0 0 0 328.6463818520241,434H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Kansas City Royals: 0.400 in 40 blowouts, 0.423 in 78 close games (-0.023)</title></path>
<text x="318.6" y="430.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.023</text>
<text x="138" y="453.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Washington Nationals</text>
<path d="M341.9098337094614,441H324.6244682239251A3.0,3.0 0 0 0 321.6244682239251,444.0V454.0A3.0,3.0 0 0 0 324.6244682239251,457H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Washington Nationals: 0.472 in 53 blowouts, 0.500 in 66 close games (-0.028)</title></path>
<text x="314.6" y="453.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.028</text>
<text x="138" y="476.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Philadelphia Phillies</text>
<path d="M341.9098337094614,464H304.9617793754409A3.0,3.0 0 0 0 301.9617793754409,467.0V477.0A3.0,3.0 0 0 0 304.9617793754409,480H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Philadelphia Phillies: 0.500 in 52 blowouts, 0.554 in 65 close games (-0.054)</title></path>
<text x="295.0" y="476.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.054</text>
<text x="138" y="499.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Texas Rangers</text>
<path d="M341.9098337094614,487H297.99169578396896A3.0,3.0 0 0 0 294.99169578396896,490.0V500.0A3.0,3.0 0 0 0 297.99169578396896,503H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Texas Rangers: 0.463 in 41 blowouts, 0.526 in 76 close games (-0.063)</title></path>
<text x="288.0" y="499.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.063</text>
<text x="138" y="522.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">San Diego Padres</text>
<path d="M341.9098337094614,510H297.7094609881088A3.0,3.0 0 0 0 294.7094609881088,513.0V523.0A3.0,3.0 0 0 0 297.7094609881088,526H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>San Diego Padres: 0.477 in 44 blowouts, 0.541 in 74 close games (-0.063)</title></path>
<text x="287.7" y="522.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.063</text>
<text x="138" y="545.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Colorado Rockies</text>
<path d="M341.9098337094614,533H284.9343044628877A3.0,3.0 0 0 0 281.9343044628877,536.0V546.0A3.0,3.0 0 0 0 284.9343044628877,549H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Colorado Rockies: 0.340 in 47 blowouts, 0.420 in 69 close games (-0.080)</title></path>
<text x="274.9" y="545.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.080</text>
<text x="138" y="568.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Athletics</text>
<path d="M341.9098337094614,556H278.55956673627117A3.0,3.0 0 0 0 275.55956673627117,559.0V569.0A3.0,3.0 0 0 0 278.55956673627117,572H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Athletics: 0.340 in 47 blowouts, 0.429 in 70 close games (-0.088)</title></path>
<text x="268.6" y="568.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.088</text>
<text x="138" y="591.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Cleveland Guardians</text>
<path d="M341.9098337094614,579H275.1559874074436A3.0,3.0 0 0 0 272.1559874074436,582.0V592.0A3.0,3.0 0 0 0 275.1559874074436,595H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Cleveland Guardians: 0.432 in 37 blowouts, 0.525 in 80 close games (-0.093)</title></path>
<text x="265.2" y="591.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.093</text>
<text x="138" y="614.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Toronto Blue Jays</text>
<path d="M341.9098337094614,602H264.4365017612874A3.0,3.0 0 0 0 261.4365017612874,605.0V615.0A3.0,3.0 0 0 0 264.4365017612874,618H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Toronto Blue Jays: 0.400 in 40 blowouts, 0.506 in 77 close games (-0.106)</title></path>
<text x="254.4" y="614.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.106</text>
<text x="138" y="637.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Minnesota Twins</text>
<path d="M341.9098337094614,625H255.70763417132713A3.0,3.0 0 0 0 252.70763417132713,628.0V638.0A3.0,3.0 0 0 0 255.70763417132713,641H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Minnesota Twins: 0.415 in 41 blowouts, 0.532 in 77 close games (-0.118)</title></path>
<text x="245.7" y="637.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.118</text>
<text x="138" y="660.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Tampa Bay Rays</text>
<path d="M341.9098337094614,648H241.8138863606829A3.0,3.0 0 0 0 238.8138863606829,651.0V661.0A3.0,3.0 0 0 0 241.8138863606829,664H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Tampa Bay Rays: 0.521 in 48 blowouts, 0.657 in 67 close games (-0.136)</title></path>
<text x="231.8" y="660.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.136</text>
<text x="138" y="683.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Cincinnati Reds</text>
<path d="M341.9098337094614,671H229.75213331237808A3.0,3.0 0 0 0 226.75213331237808,674.0V684.0A3.0,3.0 0 0 0 229.75213331237808,687H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Cincinnati Reds: 0.391 in 46 blowouts, 0.543 in 70 close games (-0.152)</title></path>
<text x="219.8" y="683.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.152</text>
<text x="138" y="706.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">St. Louis Cardinals</text>
<path d="M341.9098337094614,694H218.40432844815751A3.0,3.0 0 0 0 215.40432844815751,697.0V707.0A3.0,3.0 0 0 0 218.40432844815751,710H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>St. Louis Cardinals: 0.395 in 43 blowouts, 0.562 in 73 close games (-0.166)</title></path>
<text x="208.4" y="706.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.166</text>
<text x="138" y="729.0" text-anchor="end" fill="var(--fg)" font-size="11.5" font-weight="400">Houston Astros</text>
<path d="M341.9098337094614,717H183.78998321955805A3.0,3.0 0 0 0 180.78998321955805,720.0V730.0A3.0,3.0 0 0 0 183.78998321955805,733H341.9098337094614Z" fill="var(--chart-neg)" opacity="0.62"><title>Houston Astros: 0.378 in 45 blowouts, 0.589 in 73 close games (-0.211)</title></path>
<text x="173.8" y="729.0" text-anchor="end" fill="var(--muted)" font-size="11" font-variant-numeric="tabular-nums" font-weight="400">-0.211</text>
</svg>
```

Detroit is not merely at the top of that list. At +.288 the gap is more than
1.6 times the second-place Cubs at +.173, and the gap between Detroit and the
Cubs is wider than the gap between the Cubs and ninth place. Whatever
is happening here, it is happening to the Tigers more than to anyone else in
baseball.

| Team | Blowout win rate | Close-game win rate | Gap |
|---|---|---|---|
| **Tigers** | **.660** (31-16) | **.371** (26-44) | **+.288** |
| Cubs | .673 (35-17) | .500 (33-33) | +.173 |
| Pirates | .564 (31-24) | .422 (27-37) | +.142 |
| Brewers | .702 (33-14) | .571 (40-30) | +.131 |
| Braves | .660 (31-16) | .549 (39-32) | +.110 |
| ... | | | |
| Astros | .378 (17-28) | .589 (43-30) | -.211 |

## The number I found first, and why I am not using it

There is an obvious explanation sitting right there. Detroit has converted 22
of 47 save opportunities, 47 percent, with **25 blown saves, second most in
baseball**, behind a pitching staff whose 3.52 team ERA is fourth best in all
of MLB. Good pitching, handed back after the seventh.

Across the 30 teams, save conversion rate correlates with close-game win rate
at **r = +.783**, and with blowout win rate at **+.069**. That looks like a
smoking gun: bullpen quality drives close games and nothing else.

It is not evidence, and I want to be the one to say so. A save opportunity is
by definition a lead of three runs or fewer, and a blown save in a close game
very often *is* the close loss. The two statistics are built out of
overlapping events. Correlating them measures the dictionary, not the world. If
I published that +.783 as proof, someone would eventually notice, and they
would be right.

So the test has to be one where the answer is not baked in.

## The actual test

If losing close games is a property of a team, then a team's close games should
predict its own other close games. Deal each team's close games alternately
into two piles, odd and even, and correlate the win rate in one pile against
the other across every team. Same roster, same manager, same bullpen, no aging,
no trades in between. That is the friendliest possible test of the skill
hypothesis. Then run the identical test on all games as a control, because team
quality is unquestionably real and has to survive it.

On the 2026 season alone, it does not settle anything:

| Split-half test, 2026 only | r |
|---|---|
| All games | +.432 |
| Games decided by 3 or fewer | +.093 |
| All games, thinned to the same sample size | +.211 |
| Literal coin flips, same sample sizes | .000 (90 percent of simulations land between -.312 and +.304) |

Thirty teams is not enough. The coin-flip simulation shows that a correlation
anywhere inside roughly plus or minus .30 is what pure randomness produces at
these sample sizes, and both the close-game figure and its control sit inside
that band. Anyone who stopped here and reported "+.097, therefore luck" would
be reporting noise with a decimal point on it.

So I ran the same thing over the five completed seasons from 2021 through 2025,
which gives 150 team-seasons instead of 30, on full schedules instead of
two-thirds of one:

| Split-half test, 150 team-seasons | r |
|---|---|
| All games | +.640 |
| Games decided by 3 or fewer | **+.290** |
| All games, thinned to the same sample size | **+.583** |

Now it separates cleanly, and the comparison that matters is the last two rows,
because they use identical sample sizes. A random slice of a team's schedule
predicts the rest of that team's schedule at +.583. The same number of close
games predicts the team's other close games at +.290.

Stepping those up to full-season reliability gives **.449 for close games**
against **.737 for ordinary ones**. A close-game record carries about **61
percent** of the repeatable signal that the same number of ordinary games
carries.

**That is the answer to the objection, and it is a split decision.** Close-game
performance is not noise. Something real and repeatable is in there, and a
reader who says "this team is bad at close games" is describing something that
exists. But it is a good deal less real than the raw record makes it look, and
treating 26-44 as a fixed property of the Tigers overstates it by a wide
margin.

## What that is worth, in wins

Regressing Detroit's .371 by that reliability puts their true close-game talent
at about **.442**. Sixty percent of their games this year have been decided by
three or fewer, so call it 27 close games in the 45 that remain.

| | Record in the next 27 close games |
|---|---|
| At their observed .371 | 10.0-17.0 |
| At the regressed .442 | 11.9-15.1 |
| Difference | **about +1.9 wins** |

Two wins. Not the seven that the Pythagorean gap dangles, and not zero either.
Detroit is 2.0 games back of the third wild card. Two wins is the whole
difference between playing in October and watching, which is a genuinely
strange place for an argument about statistical reliability to land.

For what it is worth on the luck side of the ledger: if close games were coin
flips, a team playing 70 of them finishes 26-44 or worse about 2.1 percent of
the time. That is unusual. It is also the kind of unusual that shows up
somewhere every year when 30 teams each get a turn.

## The objection that survives all of this

A different reader made a point that none of the above touches, and it is the
best argument against everything I wrote last week.

Detroit's worst split is against its own division: **11-18, a .379 clip**. Last
week's piece argued that the 20-odd remaining head-to-head games against the
teams ahead of them were the path back into the race. Against a team playing
.379 ball in exactly those games, the same schedule is the fastest available
route to elimination.

Here is what I found looking into it, and it cuts both ways:

| Detroit vs AL Central | Record |
|---|---|
| Overall | 11-18 |
| In games decided by 3 or fewer | 9-14 |
| In blowouts | 2-4 |
| vs Cleveland | **0-6** |
| vs Cleveland, games decided by 3 or fewer | **0-5** |

The division record is almost entirely a close-game record. Twenty-three of
those 29 games were decided by three runs or fewer, which is a far higher share
than the 60 percent Detroit runs overall. So the division problem and the
close-game problem are not two independent pieces of evidence stacking up
against the Tigers. They are largely the same fact counted twice, and the
regression above applies to most of it.

But 0-6 against Cleveland, with five of those six decided by three or fewer, is
its own small horror. **Seven of Detroit's remaining 45 games are against
Cleveland**, and 23 of the 45 are inside the division. A team that has not
beaten the Guardians once all year now needs that specific matchup more than
any other on the schedule.

That is the honest state of it. The close-game record is about 61 percent as
meaningful as it looks, which is worth roughly two wins and probably a wild
card spot. The division record is mostly the same finding wearing a different
hat. And a winless record against the team they will see seven more times is
not something any correlation coefficient is going to explain away.

## One correction, on a number nobody asked about

While pulling this data I found that my own earlier recomputation of Detroit's
record gave 55-60 where the standings said 56-60. The missing game is April 4
against St. Louis, an 11-6 Tigers win called for rain. The MLB API returns it
with a status of "Completed Early" rather than "Final", and my filter matched
only the exact string "Final", so a real win vanished from every game-by-game
calculation I ran. It is fixed here and in the backtest script. With Saturday
night's 8-0 win in San Francisco added, the Tigers are 57-60.

It is a small thing. It is also exactly the kind of thing that quietly corrupts
a number in a piece like this, and the only reason it got caught is that a
recomputed figure disagreed with a published one by exactly one game and I
wrote it down instead of shrugging.

---

*Sourcing: every game result, margin and standing here comes from the MLB Stats
API, pulled 2026-08-09. Season data covers 1,757 decided regular-season games in
2026 through August 8, plus the complete 2021 through 2025 regular seasons for
the reliability test. Bullpen figures are the team pitching endpoint for the
same date. The chart and every figure in it are generated by
`scripts/close_gap_chart.py`; the reliability tests are
`scripts/close_games.py`, which takes `--margin` and `--seasons` so anyone can
re-run them at a different definition of "close". Both are in the repository
along with this entry.*

*Not betting advice. Just analysis, made in public and kept in public.*
