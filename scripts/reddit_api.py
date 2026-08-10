#!/usr/bin/env python3
"""Read Reddit without a browser and without his login being open.

Why this exists: anonymous JSON reads are dead. Verified 2026-08-10 from this
machine, every combination 403s: urllib with no user agent, urllib with a
descriptive one, urllib with a browser one, and curl, against www.reddit.com,
api.reddit.com and the thread endpoint. It is not the user agent. Reddit blocks
unauthenticated non-browser clients. So four unattended cycles logged the
comment check as unreachable and were right to.

The supported path is OAuth with a registered script app, rate limited at 100
requests per minute.

**NOT SET UP, deliberately, 2026-08-10.** Reddit wants a developer account and
terms acceptance, and testing showed the app would only buy one thing: reading
replies on our own posts unattended. Subreddit listings turned out to work over
RSS with no account at all (see `scripts/reddit_rss.py`), and comments are read
in live browser sessions, which happen often. If posting cadence ever rises
enough that overnight comment reading matters, this client is finished and only
needs `.reddit-credentials.json` to exist.

Credentials live in `.reddit-credentials.json` at the repo root, gitignored,
never committed:

    {"client_id": "...", "client_secret": "...",
     "user_agent": "windows:detroit-sports-reporter:v1.0 (by /u/USERNAME)"}

Read-only client credentials. No password, no posting scope: this reads, and
posting stays a human action by design.

Usage:
    python scripts/reddit_api.py rules detroitlions
    python scripts/reddit_api.py comments 1viuuv9
    python scripts/reddit_api.py top motorcitykitties week 10
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from base64 import b64encode
from pathlib import Path

ROOT = Path(__file__).parent.parent
CREDS = ROOT / ".reddit-credentials.json"
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API = "https://oauth.reddit.com"


class NotConfigured(RuntimeError):
    pass


def creds() -> dict:
    if not CREDS.exists():
        raise NotConfigured(
            f"{CREDS.name} not found. See ASK-HUMAN.md: it takes one visit to "
            "reddit.com/prefs/apps to create a script app. Until then, Reddit "
            "reads need a live browser session."
        )
    return json.loads(CREDS.read_text(encoding="utf-8"))


def token() -> tuple[str, str]:
    c = creds()
    ua = c.get("user_agent") or "windows:detroit-sports-reporter:v1.0"
    basic = b64encode(
        f"{c['client_id']}:{c['client_secret']}".encode()
    ).decode()
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(TOKEN_URL, data=data)
    req.add_header("Authorization", f"Basic {basic}")
    req.add_header("User-Agent", ua)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)["access_token"], ua


def get(path: str, **params) -> dict | list:
    tok, ua = token()
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"bearer {tok}")
    req.add_header("User-Agent", ua)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def rules(sub: str) -> list[dict]:
    d = get(f"/r/{sub}/about/rules")
    return [
        {"name": r.get("short_name"), "text": r.get("description", "")}
        for r in d.get("rules", [])
    ]


def comments(thread_id: str, limit: int = 100) -> dict:
    """Post state plus comments, flattened, up to `limit`. Checks takedown too:
    a post pulled by a mod is a real datum about the channel.

    Reddit truncates deep or wide threads and marks the cut with `more` stubs
    rather than an error. Those are counted, not silently dropped: a caller that
    cannot tell a complete thread from a truncated one will eventually read
    "no objections" off a thread that had them. `truncated` is the flag that
    matters; if it is true the reader is looking at a sample."""
    d = get(f"/comments/{thread_id}", limit=limit, depth=10, sort="new")
    post = d[0]["data"]["children"][0]["data"]
    out = []
    unfetched = 0

    def walk(children):
        nonlocal unfetched
        for c in children:
            if c.get("kind") == "more":
                # count(), not children: Reddit reports how many it withheld.
                unfetched += c["data"].get("count", 0) or 0
                continue
            if c.get("kind") != "t1":
                continue
            cd = c["data"]
            out.append(
                {
                    "author": cd.get("author"),
                    "score": cd.get("score"),
                    "body": cd.get("body", ""),
                    "created_utc": cd.get("created_utc"),
                }
            )
            rep = cd.get("replies")
            if isinstance(rep, dict):
                walk(rep["data"]["children"])

    walk(d[1]["data"]["children"])
    return {
        "title": post.get("title"),
        "score": post.get("score"),
        "num_comments": post.get("num_comments"),
        # removed_by_category also covers author deletion, automod and spam
        # filtering, so this is "taken down", not specifically "by a mod".
        "removed": bool(post.get("removed_by_category")),
        "removed_by": post.get("removed_by_category"),
        "fetched": len(out),
        "unfetched": unfetched,
        "truncated": unfetched > 0,
        "comments": out,
    }


def top(sub: str, when: str = "week", limit: int = 10) -> list[dict]:
    d = get(f"/r/{sub}/top", t=when, limit=limit)
    return [
        {
            "title": c["data"]["title"],
            "score": c["data"]["score"],
            "comments": c["data"]["num_comments"],
            "id": c["data"]["id"],
        }
        for c in d["data"]["children"]
    ]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, *rest = argv[1:]
    try:
        if cmd == "rules":
            out = rules(rest[0])
        elif cmd == "comments":
            out = comments(rest[0])
        elif cmd == "top":
            out = top(rest[0], rest[1] if len(rest) > 1 else "week",
                      int(rest[2]) if len(rest) > 2 else 10)
        else:
            print(f"unknown command {cmd!r}")
            return 2
    except NotConfigured as e:
        print(f"not configured: {e}")
        return 3
    print(json.dumps(out, indent=2)[:8000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
