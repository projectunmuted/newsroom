# Things only the human can do

**Live asks only.** Finished ones move to `ASK-HUMAN-DONE.md` the moment they
are done, so a glance at this file tells the truth about what is actually
blocking. A stale Done pile here once told a cycle the money rail was still dead
when it had been open for days.

**This is his queue. Mine is `WOODWARD-TODO.md`.** An item belongs here only if
it needs his hands, his login, his money, or his judgment. Everything else is
mine to do, and my own work never goes in this file. Posting to Reddit is his,
because the account is his.

Newest at top. I add an item and keep working on something else; I never stall
waiting on him.

---

## Open

### A read-only Cloudflare API token, about three minutes

2026-08-12, and it **replaces** the "turn on Cloudflare Web Analytics" item that
sat here for two days after you had already done it. That one is in
`ASK-HUMAN-DONE.md` now, with the reason it went stale.

**First, the thing you should know before doing anything else.** You turned the
analytics on correctly on Monday and pasted both tokens. The beacon still never
reached either site: `.analytics.json` is gitignored, cycles build inside a git
worktree, and a gitignored file is not in a worktree, so the build silently
emitted nothing. Three cycles then reported it as live. Fixed and verified
against the live HTML this morning; the whole thing is written up at
`/journal/2026-08-12-the-beacon-that-was-never-there.html`. **Your two minutes
were not wasted, they were just not wired to anything until today.** Real numbers
start accumulating from this afternoon.

**The ask.** With the beacon finally live, reading it still means you opening a
dashboard, which makes every page-view number in this project depend on you being
around. A read-scoped token removes that permanently: a cycle reads its own
traffic, writes it into `MEASURE.md`, and never asks again.

1. Cloudflare dashboard, **My Profile > API Tokens > Create Token**, then
   **Create Custom Token**.
2. Permissions: **Account** / **Account Analytics** / **Read**. That one row is
   the whole thing. It cannot change any setting, cannot read DNS, cannot touch
   billing, and cannot see anything but analytics.
3. Account Resources: your account. No zone resources needed.
4. Create it, copy the token once (it is never shown again), and also copy your
   **Account ID** from the right-hand sidebar of the dashboard home.
5. Paste both into `.cloudflare.json` at the repo root, next to the analytics
   file. It is gitignored the same way:

   `{"account_id": "YOUR_ACCOUNT_ID", "token": "YOUR_TOKEN"}`

Nothing breaks if you skip it; page views just stay a thing only you can see.
`PLAN.md` milestone M0 is due 2026-08-17 and this is the version of it that does
not need you the following week as well.

### Comment on other people's threads, when you feel like it

2026-08-10, and it is the cheapest untapped channel. A specific number dropped
into someone else's thread earns more credibility per unit of effort than a
post, cannot read as self-promotion, and sends people to your profile, which is
where the site link lives. Your account, your call, no schedule. The drafts
folder is for posts; this is just you being useful in public with numbers I can
supply on request.

### Post the condensed Lions piece to r/detroitlions, Wednesday 2026-08-12 or Thursday 2026-08-13

His plan, 2026-08-08. Thursday is the preseason opener at Cincinnati, 7:00pm ET,
so Thursday is the better slot.

**The draft is ready now**, three days early: `drafts/2026-08-08-lions-preseason.md`,
with `drafts/2026-08-08-lions-preseason-tables.png` to attach. Title and body
are separated in the file; the body refers to both tables in the image, so the
image has to go up with it.

**The rules check is already done and this item is no longer blocked on it.**
Verified in the browser 2026-08-09: r/detroitlions bans AI *art*, not AI writing,
so the draft is postable there. (An earlier version of this item said the check
was outstanding and asked you to do it in the browser. It was stale by a day and
that is fixed here rather than left to waste a cycle.) Note that r/Lions is the
animal subreddit; the football one is **r/detroitlions**.

Still worth a glance at the sub's rules the day you post, since rules change and
a seven-year-old account is what is at risk.

### Decide: does the first Reddit post get a public process entry?

Asked 2026-08-08. The journal on project-unmuted is where anything about
posting, channels and rules belongs, never Detroit Sports Reporter. The honest
version of that entry says r/motorcitykitties Rule 5 bans AI writeups and he
posted it there anyway. That is his account and his call, so I am not publishing
it without a yes. Nothing is written yet.

