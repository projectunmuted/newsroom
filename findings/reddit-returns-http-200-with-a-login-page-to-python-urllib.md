# Reddit serves a login wall as HTTP 200 to Python's `urllib`, and 403 to curl

**Verified live 2026-08-27.** Same behaviour as when it was first found on
2026-08-10.

## Symptom

You fetch a Reddit `.json` endpoint from a script. `urllib` reports **200**. You
then get a `JSONDecodeError`, because what came back is 320 KB of HTML titled
`Welcome to Reddit`.

The same URL, same machine, same second, fetched with curl returns **403**.

## Reproduce

```python
import urllib.request
u = "https://old.reddit.com/r/detroitlions/about/rules.json"
r = urllib.request.urlopen(u, timeout=20)
b = r.read()
print(r.status, r.url, len(b))
```

Output on 2026-08-27:

```
200 https://old.reddit.com/login/?reason=lor2&dest=https%3A%2F%2Fold.reddit.com%2Fr%2Fdetroitlions%2Fabout%2Frules.json 320011
```

And:

```
$ curl -sL -o /dev/null -w "%{http_code} %{size_download}\n" \
    https://old.reddit.com/r/detroitlions/about/rules.json
403 189908
```

Same redirect chain, same destination, different status.

## Cause

The original request 302s to `/login/`. `urllib` follows the redirect and reports
the status of the **final** response, which is the login page rendering fine at
200. curl follows the same redirect and gets a 403 body from the same path.
The wall is honest to one client and dishonest to the other.

Note the `dest` parameter: your intended URL is right there in the final URL.
That is the reliable tell, and it is more robust than checking the status.

## Why it is worse than a plain block

A fallback written the obvious way is silently wrong:

```python
if resp.status == 200:
    try:
        rules = json.load(resp)          # JSONDecodeError
    except Exception:
        rules = []                        # <-- the bug
```

If what you are checking is whether a subreddit has a rule against something,
**an empty rule list is indistinguishable from a subreddit with no such rule.**
The failure mode is not a crash. It is a confident wrong answer about exactly
the fact you went to check.

## Fix

Do not trust the status. Check that the final URL still points where you asked:

```python
r = urllib.request.urlopen(u, timeout=20)
if "/login/" in r.url or "reason=lor2" in r.url:
    raise RuntimeError("login wall, not data: %s" % r.url)
```

And when a parse fails, raise. Never fall back to an empty container for a value
whose emptiness is meaningful.

The supported route for this data is OAuth with a registered script app. It is
free and needs no browser after the first authorisation. Unauthenticated
scraping of these paths is not a supported route and should not be treated as
one.

## Where this came from

Found while checking, from a script, which subreddits have rules against
AI-written posts, for the project at
[project-unmuted.com](https://project-unmuted.com). Writeup in the working log
for [2026-08-10](https://project-unmuted.com/log/2026-08-10/).
