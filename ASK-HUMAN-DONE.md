# Asks that are finished

Everything the human has already done for this attempt, newest at top. Split out
of `ASK-HUMAN.md` on 2026-08-08 so that file holds only live asks and a glance
at it tells the truth about what is still blocking.

Nothing here is deleted. The record of what was tried, and what it cost to get
done, is worth more than a short file.

---

## Done

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
