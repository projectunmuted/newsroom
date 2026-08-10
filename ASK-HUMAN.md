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

### Create a Reddit script app so cycles can read Reddit without you, about two minutes

His idea, 2026-08-10, and it is the right one. Anonymous reads are dead: I
tested every combination from this machine on 2026-08-10 and all of them 403,
including curl and a browser user agent, against www.reddit.com, api.reddit.com
and the thread endpoint. It is not the user agent, it is Reddit blocking
unauthenticated non-browser clients. That is why four unattended cycles logged
the comment check as unreachable.

OAuth fixes it permanently and costs nothing. Steps:

1. Go to **reddit.com/prefs/apps** while signed in as u/ICantSpellorWrite.
2. "create another app...", name it anything, choose **script**, redirect URI
   `http://localhost:8080` (unused, but required).
3. Copy the **client id** (under the app name) and the **secret**.
4. Save them at the repo root as `.reddit-credentials.json`, already gitignored:

   ```json
   {"client_id": "...", "client_secret": "...",
    "user_agent": "windows:detroit-sports-reporter:v1.0 (by /u/ICantSpellorWrite)"}
   ```

Then `python scripts/reddit_api.py rules detroitlions` works from any cycle,
unattended. The client is written and waiting; it fails with a clear message
until the file exists.

**Read-only by design.** Client credentials, no password, no posting scope.
Posting stays your hand, deliberately. What this buys: every cycle can read the
comments on a live post, check a sub's rules before drafting, and sweep the fan
subs, none of which currently happens without you.


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

