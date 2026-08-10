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

### Turn on Cloudflare Web Analytics, about two minutes

2026-08-10. **Right now nobody knows how many people have read either site.**
Not a small number: no number. GitHub Pages keeps no server logs, so page views
simply do not exist unless something measures them.

Cloudflare Web Analytics is free, needs no cookie and no consent banner, and
works on any host. Your Cloudflare account already exists, since
project-unmuted.com's DNS lives there.

1. Cloudflare dashboard, **Analytics & Logs > Web Analytics**, "Add a site".
2. Add **detroitsportsreporter.com** and **project-unmuted.com**.
3. Copy the beacon token for each and paste them into `.analytics.json` at the
   repo root (gitignored):
   `{"dsr": "TOKEN", "journal": "TOKEN"}`

`build.py` emits the beacon whenever that file exists, so nothing changes until
you do it and no token ever lands in git. Without this, `PLAN.md` milestone M0
cannot be met and the whole bet stays unfalsifiable: if no dollar arrives we
would not be able to tell whether nobody read it or people read it and did not
care, which need opposite responses.

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

