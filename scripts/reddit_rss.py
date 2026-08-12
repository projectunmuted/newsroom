#!/usr/bin/env python3
"""Read what Detroit fans are talking about, with no account and no API app.

Tested 2026-08-10 from this machine, and the result is split:

  - **Subreddit listing feeds work.** `r/<sub>/.rss`, `/new/.rss`, `/hot/.rss`
    all return 200 with 25 entries and no credentials.
  - **Thread comment feeds do not.** `/comments/<id>/.rss` returns 429 every
    time, including with twelve seconds between requests. So reading the replies
    on our own posts still needs a browser session or OAuth.

That split is why the Reddit API app was dropped rather than queued: the only
thing it bought was unattended comment reading, and the sweep, which is what a
cycle actually needs to pick a topic, works without it.

Be polite. One request at a time, a real user agent, a gap between calls, and a
cache so re-running inside the cache window costs Reddit nothing.

**Rewritten 2026-08-12, because 12 seconds was not enough and the sweep was
lying about its own coverage.** Four cycles running it came back rate limited on
2, 3, 3 and 2 of the 4 subs, printed "0 posts" beside the ones it never read,
and then handed a caller a dict that looks exactly like a sub with nothing in
it. A cycle reading that cannot tell "the fanbase isn't discussing this" from "I
never asked". Three changes, in order of how much they matter:

  1. **A 429 is retried**, twice, at 45 and 90 seconds. Reddit's limit is a
     short window, so waiting it out works where spacing alone did not.
  2. **The gap is 20 seconds**, not 12.
  3. **Coverage is reported as data, not as a guess.** Every sub carries an
     `ok` flag and where it came from, and the JSON has a `coverage` block
     naming the subs that failed. A run that reached 2 of 4 subs says so in a
     line a cycle has to read before it can quote the sweep.

    python scripts/reddit_rss.py                 # all four Detroit subs
    python scripts/reddit_rss.py detroitlions    # one sub
    python scripts/reddit_rss.py --sort new
    python scripts/reddit_rss.py --gap 30        # slower still
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
CACHE = ROOT / "logs" / "reddit-cache"
CACHE_MINUTES = 30
GAP_SECONDS = 20
RETRY_WAITS = (45, 90)  # seconds to wait after a 429, in order

UA = "windows:detroit-sports-reporter:v1.0 (fan sub reading; no posting)"

SUBS = ["motorcitykitties", "detroitlions", "DetroitPistons", "DetroitRedWings"]


def fetch(url: str) -> tuple[str | None, str]:
    """Returns (body, source). Source is 'cache', 'live', or a failure reason.

    The second element exists because the old signature returned None for both
    "rate limited" and "nothing there", and the caller turned both into an empty
    list. Those are opposite facts and the sweep has to keep them apart.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^a-z0-9]+", "-", url.lower()).strip("-")[:80]
    cached = CACHE / f"{key}.xml"
    if cached.exists():
        age = (time.time() - cached.stat().st_mtime) / 60
        if age < CACHE_MINUTES:
            return cached.read_text(encoding="utf-8"), "cache"

    waits = list(RETRY_WAITS)
    while True:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", UA)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429 and waits:
                wait = waits.pop(0)
                print(f"  429 on {url}, waiting {wait}s and trying again",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            reason = "rate limited" if e.code == 429 else f"HTTP {e.code}"
            print(f"  {reason} on {url}", file=sys.stderr)
            return None, reason
        except Exception as e:  # network, DNS, timeout
            print(f"  failed {url}: {e}", file=sys.stderr)
            return None, f"error: {e}"

        cached.write_text(body, encoding="utf-8")
        return body, "live"


def parse(xml: str) -> list[dict]:
    out = []
    for block in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        def grab(tag):
            m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", block, re.S)
            return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""

        link = re.search(r'<link[^>]*href="([^"]+)"', block)
        author = re.search(r"<author>.*?<name>(.*?)</name>.*?</author>", block, re.S)
        out.append({
            "title": unescape(grab("title")),
            "url": link.group(1) if link else "",
            "author": author.group(1) if author else "",
            "updated": grab("updated"),
        })
    return out


def unescape(s: str) -> str:
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                 ("&quot;", '"'), ("&#39;", "'"), ("&#32;", " ")):
        s = s.replace(a, b)
    return s


def sweep(subs: list[str], sort: str = "hot", gap: int = GAP_SECONDS) -> dict:
    posts: dict[str, list] = {}
    sources: dict[str, str] = {}
    for i, sub in enumerate(subs):
        if i:
            time.sleep(gap)
        path = "" if sort == "hot" else f"{sort}/"
        xml, source = fetch(f"https://www.reddit.com/r/{sub}/{path}.rss")
        posts[sub] = parse(xml) if xml else []
        sources[sub] = source
        state = source if xml else f"NOT READ ({source})"
        print(f"{sub:20} {len(posts[sub]):3} posts  {state}", file=sys.stderr)

    reached = [s for s in subs if sources[s] in ("cache", "live")]
    missed = [s for s in subs if s not in reached]
    print(f"\ncoverage: {len(reached)} of {len(subs)} subs", file=sys.stderr)
    if missed:
        print(f"NOT READ: {', '.join(missed)}. A conclusion of the form "
              f"'the fanbase is not talking about X' is unsupported for these.",
              file=sys.stderr)
    return {
        "subs": posts,
        "coverage": {
            "asked": subs,
            "reached": reached,
            "missed": missed,
            "sources": sources,
        },
    }


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    sort = "hot"
    if "--sort" in argv:
        sort = argv[argv.index("--sort") + 1]
        args = [a for a in args if a != sort]
    gap = GAP_SECONDS
    if "--gap" in argv:
        gap = int(argv[argv.index("--gap") + 1])
        args = [a for a in args if a != str(gap)]
    subs = args or SUBS
    result = sweep(subs, sort, gap)
    print(json.dumps({
        "read_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sort": sort,
        "coverage": result["coverage"],
        "subs": result["subs"],
    }, indent=1)[:12000])
    return 0 if not result["coverage"]["missed"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
