# Asks that are finished

Everything the human has already done for this attempt, newest at top. Split out
of `ASK-HUMAN.md` on 2026-08-08 so that file holds only live asks and a glance
at it tells the truth about what is still blocking.

Nothing here is deleted. The record of what was tried, and what it cost to get
done, is worth more than a short file.

---

## Done

## Three items that were never his, closed 2026-08-26

His reset that day: he is too busy to be a gate, and `ASK-HUMAN.md` had grown to
8 open items. Reviewed against the new 4-category contract in `CYCLE.md`, 3 of
the 8 did not belong to him at all. Answered here rather than left sitting.

### Do r/DetroitRedWings and r/DetroitPistons ban AI-written posts? No, neither.

Read in a browser 2026-08-26, both rule pages in full. **Neither sub has any
rule about AI-written content.** That is 2 of the 4 teams unblocked, and it
matters most for the Wings and Pistons, who have had almost no coverage because
the Tigers play every day.

What each sub *does* have, and both are stricter than r/detroitlions on
promotion:

- **r/DetroitRedWings**, 11 rules. Rule 7 caps self-promotion at Reddit's 10:1
  ratio, with personal blog posts limited to 1 every 14 days. Rule 3 bans low
  content, Rule 5 requires a descriptive title.
- **r/DetroitPistons**, 12 rules. Rule 3 is the sharp one: "If you are an
  outsider to this subreddit, you may not promote your content here. Attempts to
  do so will result in an immediate ban." Rule 2 allows removal for low quality.

Neither is a problem for the format used so far, because these posts carry the
analysis in the body and never link the site. It does mean the Pistons sub is
unforgiving of a first-time account that looks like it is advertising, so the
first post there has to be worth reading on its own or not happen.

This was queued as "90 seconds in a browser". It sat open for 8 days because it
needed a browser session and cycles do not have one, which is a real structural
gap and not laziness: anything needing a live browser has to be done in a
session with him or not at all. Noted in `WOODWARD-TODO.md`.

### How does a reader find out their request got answered? Decided, not asked.

This was filed as "judgment call", which the new contract says is the tell that
a cycle is about to hand over something that is its own.

**The decision: `/requests.html` is the answer, and it is the only answer.** It
lists every request with the URL of the piece that answered it. A piece written
from a request opens by stating the question it answers, in the reader's terms,
without naming the asker or the thread.

What was rejected and why: replying to the commenter is his rule against and
stays that way; naming the asker in the piece turns a stranger into a character
without their consent; and mentioning it in a later post is the backward
self-reference he cut out of a draft on 08-14.

The honest limit, recorded rather than smoothed over: a reader who asked in a
thread and never comes back will never know. That is a real loss and there is no
lever on it that does not run through his account.

### Does the first Reddit post get a public process entry? No.

**Decided 2026-08-26.** No standalone entry. The journal is the money log now,
and how a channel performed belongs inside a money essay next to what it cost
and what it returned, which is where it has been appearing anyway. A separate
piece about our own first post is the site talking about itself, and he has said
twice that reading a piece refer back to its own author's earlier work is a
turnoff.

## Post the condensed Lions piece to r/detroitlions

**Done 2026-08-13**, before the 7:00pm ET preseason opener at Cincinnati, exactly
the slot the ask named. Thread `1vne8nx`, not removed.

**He retitled it and edited the body.** Mine was 28 words describing the method;
his was **"Preseason record really doesn't matter."** That lesson is written into
`VOICE.md` as its own section, because it is about titles generally rather than
about this post.

**Reception: 5 up, 33 comments, about 9,000 views at 2 hours.** The
comment-to-upvote ratio is the result: it argued rather than landed. The top
comment, at 13 up, is that the 2008 Lions went 4-0 in the preseason and 0-16 in
the season, and the sample starts in 2015 so it is missing. That went to
`REQUESTS.md` and the answer is already published.

**And it is the first thing this project ever distributed with a working page
view counter, which is what makes it worth this much space.** The measurement, read
2026-08-14 against a baseline recorded at post time: **3 page views on
detroitsportsreporter.com, 0 on the journal.** About 1 visit per 3,000 people who
saw the post. Full working in `MEASURE.md` and `drafts/POSTED.md`.

The ask is closed. What it bought is a real number for a channel that had only
ever been guessed at, and the number is discouraging.

## Cloudflare Web Analytics: the API token, and the radio button that was the whole bug

2026-08-12 evening. Two asks, closed together because the second one is what the
first one found.

**The read-scoped API token.** Created under the correct account and saved to
`.cloudflare.json`. Verified: token active, `Account Analytics: Read`, GraphQL
answering. A cycle can now read its own page views with
`python scripts/read_analytics.py` and never has to ask him for a dashboard
screenshot again.

**What it immediately proved.** Zero page views for either site across ninety
days, his own visits from a PC and a phone included. The beacon's POST to
`cloudflareinsights.com/cdn-cgi/rum` was answered **503** on every load of both
sites. Not an ad blocker; a blocked request never leaves the browser.

**The cause, found in his dashboard.** Both Web Analytics properties were set to
"Enable - the JS Snippet will be automatically injected", which only injects for
hostnames proxied through Cloudflare and refuses a hand-installed beacon. He
switched both to "Enable with JS Snippet installation" and the next page load
returned **204**. Both sites are collecting.

Neither token was ever wrong. `13bd0d16...` and `4b76f352...` matched the
dashboard snippets exactly, on the correct sites, the entire time. No code
change was needed to fix it.

Two things worth keeping from the search. There are **two Cloudflare logins**:
`Stanleyblume@gmail.com` owns an empty account with no domains and no analytics,
and `Projectunmuted@proton.me` owns everything real, account
`f750028a5c96e346209c425df4119574`. Half an hour went into looking at the wrong
one. And `.cloudflare.json` was **not** gitignored, though the ask claimed it
was; that was fixed before the token existed, which is the only safe order.

### 2026-08-10 — Cloudflare Web Analytics turned on (and the ask went stale for two days)

He created Web Analytics properties for both sites and pasted the two beacon
tokens into `.analytics.json` the same evening it was asked. **Done on the day.**

It stayed in the Open pile until 2026-08-12 anyway, which is exactly the failure
the top of `ASK-HUMAN.md` warns about, so it is recorded here rather than quietly
moved. He would have read his queue on Tuesday and seen a job he had already
finished on Monday.

Worse, and found the same morning: **the beacon was never actually on either
site.** `.analytics.json` is gitignored, background cycles build inside
`.claude/worktrees/`, and a gitignored file does not exist in a worktree, so
`build.py` found no tokens and emitted no beacon while three cycles of
`MEASURE.md` recorded it as live and collecting. Fixed in `build.py`, which now
looks in the main checkout and shouts on stderr when it emits nothing, and caught
by the new `scripts/check_live.py`, which asserts against the live HTML rather
than the source. Written up at
`/journal/2026-08-12-the-beacon-that-was-never-there.html`.

So his two minutes were not wasted, they were just not connected to anything
until now. The live ask that replaces this one is the read-scoped API token,
which is the version that stops a cycle needing him at all.

### 2026-08-10 — Reddit API app dropped, and mostly replaced for free

He asked whether registering a developer account and an app was more trouble
than it was worth. Tested rather than guessed, and the answer split:

- **Subreddit listing feeds work with no account at all.** `r/<sub>/.rss`
  returns 200 with 25 posts, verified on r/detroitlions and r/motorcitykitties.
  So the sweep a cycle needs to pick a topic costs nothing.
- **Thread comment feeds do not.** `/comments/<id>/.rss` returns 429 every time,
  including with twelve seconds between requests.

So the app's entire value was reading replies on our own posts unattended. He is
present when posts go up and replies himself, live sessions are frequent, and a
browser session reads any thread. Against a developer account plus terms
acceptance, that is not worth it. **Dropped, not deferred.**

`scripts/reddit_rss.py` takes the free half: polite sweeps of all four Detroit
subs with a cache and a gap between requests. `scripts/reddit_api.py` stays in
the tree, unused, and its docstring now records why: if posting cadence ever
rises enough that overnight comment reading matters, the client is written and
only needs credentials.

### 2026-08-09 — Browser reconnected, and it opens on demand now

He signed into claude.ai in the detroitsportsreporter profile, pinned the
extension, and closed Chrome. Launching it again with `scripts/open-browser.ps1`
paired on the first try. So the fix was: sign in, pin, restart. Chrome does not
have to stay open, which was his actual requirement; I start it when I need it
and it connects.

Used it immediately for the thing it was blocking: r/detroitlions' rules,
verified in the browser rather than guessed. Recorded in the Lions draft.

### 2026-08-09 — Hacker News dropped, not parked

He killed it: "no longer needed with the new direction." It had sat as a parked
item since attempt 2, waiting for the `projectunmuted` account to age past HN's
gate on Show HNs from new accounts. The direction now is Detroit sports readers,
reached where they already are, and a tech-forum launch aimed at people who do
not care about the Tigers was borrowed from a different project. Not a failure,
just no longer the plan. The account still exists if that ever changes.

### 2026-08-08 — Merged the two-queue split to main

He asked me to merge it myself rather than clicking through GitHub, and to keep
main current from here. Merged `worktree-todo-split` into `main` and pushed;
`WOODWARD-TODO.md`, `ASK-HUMAN-DONE.md`, `drafts/` and
`scripts/make_table_image.py` are live on main, so unattended cycles see them.
His working folder is the source of truth again; he should not have to read
GitHub to know the current state.


### 2026-08-08 — Ko-fi payments connected, the rail is open

You linked a payment method. Verified in the browser: the "Action required"
banner is gone, the default amount is $1 and the button reads Tip $1. This had
been the top blocker, since ko-fi.com/detroitsportsreporter could not accept a
cent without it. **For the first time in three attempts a stranger can actually
give this project a dollar.** Everything I could do around it was already done:
display name, bio, website link, category, Lions-blue theme, auto thank-you,
and minimum price dropped from $5 to $1 (a five dollar floor made a one-dollar
goal literally impossible). Recorded in `MONEY.md`. *(Moved out of Open on
2026-08-08 morning; it had been left sitting in the Open list after the fact,
which would have told a future cycle the rail was still dead.)*

### 2026-08-08 — Ko-fi rebuilt on the Detroit brand, Proton and Ko-fi sessions live

New account ko-fi.com/detroitsportsreporter created and configured; both
sites now point at it (one account means one payment connection to keep
alive). Old projectunmuted page retired. Browser sessions for Ko-fi and
Proton are in the profile, so I can now see earnings and mail myself instead
of being blind to the project's only success metric.

### 2026-08-08 — detroitsportsreporter.com live, repo renamed to newsroom

Domain flipped, HTTPS enforced, own IndexNow key. Source repo renamed
dollar-experiment -> newsroom so the proof link stopped announcing the
framing we removed from the page; old URL 301s, Pages and Search Console
both survived. Note: the rename silently broke Pages' auto-build trigger
(status said "built" at a stale commit), fixed with a forced rebuild.

### 2026-08-08 — Google Search Console verified, sitemap submitted

Done end to end from the browser, no DNS needed. Property added as **URL
prefix** rather than Domain specifically because Domain requires DNS
verification (your hands) while URL prefix allows HTML-file verification
(mine): Google names a token file, `build.py` emits it every build so it can
never silently vanish, Pages serves it, Google fetched it. Ownership
verified, `sitemap.xml` submitted and accepted. Google now crawls alongside
the IndexNow engines. This had been the top queued item for a day.

### 2026-08-08 — Browser and accounts connected

Claude extension installed in the Work profile and paired. The diagnosis that
unstuck it: Chrome extensions are per-profile, and the profile you had moved
to was the only one without it. Reddit confirmed as **u/ICantSpellorWrite**
(created 2019, 5,480 karma, verified email, no suspensions) — a genuinely
aged account, which is the one thing a new account cannot fake. Nothing
posted.

### 2026-08-08 — Attempt 2 closeout

All three tool submissions closed politely; see LOG. Ko-fi, domain, HN
account, scheduled task, Chrome profile all carried into attempt 3.
