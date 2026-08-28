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

### One sitting, 4 accounts, and every one of them is a channel I keep forever

2026-08-26, **not urgent, and deliberately filed as 1 item rather than 4** so it
can be done in one sitting or ignored as one thing.

**Why this is the best use of your time in the project.** What your attention has
been spent on is per-post approval: a recurring cost that buys exactly 1 post.
An account is the opposite. It costs you 5 minutes once and then it is a channel
that runs without you for the rest of the experiment. Everything this project has
ever reached a reader through is 1 subreddit on 1 account of yours, which is a
distribution strategy whose throughput is your spare attention and whose single
point of failure is you being busy, which you have now told me you are.

I cannot make accounts. That is a hard line and not a preference: an account is
an identity, and identities belong to people. So every platform answer is gated
behind you, permanently, unless you spend the 5 minutes.

**In the order I would do them, and stop whenever you like:**

1. **Bluesky.** No invite needed, posts are public and crawlable, and unlike
   Reddit the account can carry a link home in its profile without tripping a
   self-promotion rule. Highest value per minute.
2. **A Hacker News account.** Not to post the sports site, which would be
   correctly killed. The 4 technical findings are HN-shaped, and a single front
   page would be more traffic than this project has seen in total.
3. **YouTube, for Shorts.** Slowest to pay off and the most work per post, but
   it is the only one that reaches Detroit fans who are not on Reddit, which is
   the actual audience.
4. **Google Search Console access**, or the day you can paste what it says.
   Verified 08-08 and never read. Right now search is measured by asking Google
   6 queries and counting zeroes.

Credentials go in the gitignored file, same as `.cloudflare.json`. I never need
the passwords, only whatever token or app password the platform issues.

**If you do none of this, nothing breaks.** The GitHub surface and the findings
route need nobody, and they are being built either way. This is the difference
between one slow channel and several.

### One of the two drafts died. Here are the two that are alive

2026-08-24, and this replaces the 08-20 version of this item, which is now out
of date in a way worth stating plainly.

**The Royals series preview is dead.** It expired at first pitch, 8:10pm ET
Friday, unposted. Nothing ran on this machine between Friday morning and this
morning, so nothing even re-surfaced it to you. That is not your fault and I am
not re-queuing it. It is the first finished draft here to be read by nobody, and
it is written up at `/journal/2026-08-24-three-days-dark.html`.

**The two that are alive, and they do not conflict on a deadline any more:**

| | `2026-08-14-lions-2008-followup.md` | `2026-08-24-pythag-extremes.md` |
|---|---|---|
| Sub | r/detroitlions | **r/Sabermetrics** |
| Their AI rule | bans AI **art** only, text is fine | **no AI rule at all**, per the 08-10 survey |
| Deadline | none, it is a reply to a live thread | **none any more.** Rewritten 2026-08-27 02:00 onto the Pythagorean residual, which moves about a tenth of a win a night |
| Waiting since | **13 days** | 3 days |
| Why it might work | the only sub that has ever measurably sent a reader here | the first door this project has tried that was never closed |

**What is new and why it is worth 5 minutes of your attention.** Every draft
before today pointed at a Detroit sub, and 33 of the 40 analysis pieces here are
about the Tigers, whose sub bans this by Rule 5. The r/Sabermetrics draft is the
first one aimed at an audience that has no rule against it, and its subject is a
league-wide fact rather than a Detroit one: Tampa Bay and Detroit have each
scored **exactly 587 runs** this season and are 16 games apart in the standings.
That is a sabermetrics-sub question, not a fan-sub question, and it does not
spend the one Detroit door known to be open.

**My read:** post the r/Sabermetrics one. It tests a channel nobody has tested,
it cannot be removed for being AI, and the Lions one keeps indefinitely because
it has no deadline. If you would rather do the Lions one, that is also a good
answer and it has waited long enough to deserve it. The cap is still 1 a day, so
it is one or the other.

If the answer is neither, say so and I will retire both rather than keep
re-queuing them.

**Update 2026-08-27: the r/Sabermetrics draft has stopped decaying, and it is a
better draft for it.**

It opened on both clubs having scored exactly 587 runs. That became 591 to 588,
then level again at 592, and after Wednesday's game it is 595 to 592 with the
series over. The coincidence is gone and I have retired it rather than chase a
4th version of the same sentence.

**What it leads on now is the finding that was underneath it all along:** Detroit
is 12.1 wins below its Pythagorean record, the largest gap in baseball, and 2nd
place is the Angels at 7.2. A residual built over 133 games moves about a tenth
of a win a night, so this version keeps for weeks rather than hours. The draft
and its PNG were regenerated at 02:00 this morning against a fresh pull and every
number in it is correct as of then.

That is the whole point of the ask being 4 days old and still live. The version
you would have posted on Monday was fragile. This one is not.

**Update 2026-08-28: this is now issue
[#5](https://github.com/projectunmuted/newsroom/issues/5), and that is where it
lives from here.**

It is the first `--blocker` this project has ever opened, 2 days after the
notification channel was built. Until this morning this ask existed only in this
file, which is a file in a repo rather than something that arrives, so the
honest description of the 14 day wait is that you were never actually asked. The
issue wants one word: **sabermetrics**, **lions**, or **neither**. Closing it is
the whole action. Every number in the r/Sabermetrics draft was re-verified
against a live MLB pull at 10:00 this morning and is unchanged: 62-71, 592
scored, 522 allowed, expected 74.1 wins, minus 12.1.

**Unchanged either way:** you approve the specific post, I submit it through the
browser, I never reply to a comment. Approval is per post and never standing.
The rules line above is from a dated survey, not a live read, because Reddit's
rules pages are blocked from here; confirm it in the browser before you post.

### One `gh auth refresh`, if you happen to be at a terminal

2026-08-19, genuinely minor, no rush, and it is here only because I hit the wall
rather than because it matters much.

I set the homepage field on both GitHub repos this morning so the public repo
pages link to the sites they deploy. The `detroitsportsreporter` repo had no
homepage set at all. The **profile-level** version, a bio and a website on the
`projectunmuted` account, needs the `user` OAuth scope and the stored token has
`gist, read:org, repo, workflow`.

`gh auth refresh -h github.com -s user` as `projectunmuted` and I can do the rest.

Worth being honest about the size of the prize: GitHub marks all of these
`rel="nofollow"`, verified in the rendered HTML this morning, so they are a crawl
path and not a vote. Do it if you are passing. Do not make a trip.

### Check `projectunmuted@proton.me` when you think of it, and paste anything that arrives

2026-08-15. Detroit Sports Reporter now has a `/requests.html` page inviting
readers to email a question, and it is the first step of the route `MONEY.md`
calls the likeliest first dollar. It was missing entirely until this morning: the
site had a tip button on every page and no address anywhere.

**I cannot read that inbox.** It needs a login and a browser, so anything that
arrives sits there until you look. No schedule, and I would rather you ignored
this for a week than treated it as a chore. If something does arrive, paste it
into chat and I will do the rest: it goes in `REQUESTS.md` verbatim, into
`requests.json`, and gets answered on the site whichever way it lands.

Realistically the expected volume this week is zero, at 2 to 16 page views a day.
This is here so that if something does arrive it does not sit unread for a month.

**The version that ends this ask** is a mailbox with an API and a read token,
which costs money and is therefore yours to decide rather than mine to build. Not
asking for that yet; there is no traffic to justify it.

### Tell me the day you posted, within a week. That is the whole ask now

**Shrunk 2026-08-16**, and the old version of this item is retired below because
it asked for something a script can now do.

It used to say: run `read_analytics.py` before you submit and write the numbers
down, every time, or the post's effect is lost. That was true when the only
resolution available was a whole day. It is not true any more. Cloudflare's RUM
API returns **hourly** buckets, `read_analytics.py --hourly` reads them, and a
post's effect can now be reconstructed after the fact without anybody having
written anything down in advance. The 08-14 White Sox preview, previously
recorded here as permanently unknowable, was reconstructed this morning.

**What I still need from you, and it is one sentence:** which sub, and which day.
Not the minute, not a baseline, no dashboard. "I posted the Lions thing
Thursday" is enough, because I can find the hour myself from the traffic shape.

**The one real constraint:** the raw hourly table only reaches back **about 7
days**. Past that Cloudflare serves a 1-in-10 sample, which cannot show a
three-view event at all. So a post you mention within the week is fully
measurable and a post you mention a fortnight later is gone. No urgency beyond
that, and if you forget, say so and I will record it as unmeasured rather than
guess.

Why it still matters: the conversion figure the whole route ranking rests on is
one post, and this morning's hourly reconstruction showed it is an **upper
bound** rather than a measurement. It badly needs a second data point.

### Comment on other people's threads, when you feel like it

2026-08-10, and it is the cheapest untapped channel. A specific number dropped
into someone else's thread earns more credibility per unit of effort than a
post, cannot read as self-promotion, and sends people to your profile, which is
where the site link lives. Your account, your call, no schedule. The drafts
folder is for posts; this is just you being useful in public with numbers I can
supply on request.

