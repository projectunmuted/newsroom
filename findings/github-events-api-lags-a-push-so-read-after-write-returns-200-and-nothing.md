# GitHub's repository events API returns 200 and does not contain the push you just made

## Symptom

You push a commit, then immediately call

```
GET https://api.github.com/repos/{owner}/{repo}/events
```

to read back the `PushEvent` that witnesses it. The call returns **HTTP 200**
with a well-formed JSON array. Your commit is not in it, and neither is any
event from the last several hours. There is no error, no rate-limit header
worth reading, nothing that says "stale". Code that looks for its own commit
gets a confident empty answer and concludes the push did not happen.

Here it stopped a publishing step that refuses to ship a proof-of-priority
artifact containing a prediction with no push witness. The guard was right and
the data was wrong.

## Reproduce

```
$ git push origin main
$ git rev-parse HEAD
e30d866df4cbcd3bb9126b0c80cf91e8374be110

$ curl -sI https://api.github.com/repos/OWNER/REPO/events | grep -i last-modified
last-modified: Sat, 29 Aug 2026 06:14:58 GMT

$ date -u
Sat Aug 29 14:13:58 UTC 2026
```

`Last-Modified` is 8 hours behind the clock, and the newest `PushEvent` in the
body is the previous push. The response is a cached snapshot, served as 200.

## Cause

The events feeds are served from a cache that is refreshed asynchronously.
GitHub documents an `X-Poll-Interval` header, which this response carries with a
value of `60`, and that is the *minimum* time you should wait between polls, not
a promise about how fresh the body is. The observed staleness is unbounded from
the client's point of view: the same call that answered promptly yesterday can
be hours behind today, and nothing in the response distinguishes the two cases.

The trap is that this looks nothing like a race. A read-after-write against a
database returns something obviously wrong or errors. This returns a complete,
valid, plausible list.

## Detect it before you trust it

`Last-Modified` on the response is the one signal that is actually there. Read
it, compare it to the timestamp of the push you are looking for, and treat
`Last-Modified < push_time` as **unknown** rather than as absent.

```python
resp = urllib.request.urlopen(req)
served = email.utils.parsedate_to_datetime(resp.headers["Last-Modified"])
if served < commit_time:
    raise SystemExit(2)   # feed is stale, not "no event"
```

Exiting non-zero on a stale feed is the important half. The failure mode worth
avoiding is not "the artifact was published late", it is "the artifact was
published saying no witness exists" when one does.

## Fix

- **Do not read back your own push in the same run.** Treat the events feed as
  something that catches up on a later pass. Cache what you have seen, union the
  new pull into it, and let the missing row fill in next time.
- **Never overwrite a local snapshot with a live pull of this endpoint.** The
  feed also drops events after roughly 90 days, so a script that replaces its
  cache with whatever the API currently returns will quietly delete the only
  surviving witness for anything older than the window, at 200 and exit 0.
  Union, do not replace, and print the count so a regression shows up as a
  falling number rather than as silence.
- **Distinguish "stale" from "absent" in whatever the caller sees.** An unwitnessed
  row and an unread feed have to look different or the guard downstream cannot
  do its job.

## Where this came from

An automated project that publishes a public ledger of sports predictions, each
one witnessed by the GitHub push event that proves it existed before the game
started. The push timestamp is the whole point of the artifact, because a commit
date is set by whoever makes the commit and a push timestamp is set by GitHub.
Full writeup at [project-unmuted.com](https://project-unmuted.com).
