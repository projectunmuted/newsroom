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

    python scripts/reddit_rss.py                 # all four Detroit subs
    python scripts/reddit_rss.py detroitlions    # one sub
    python scripts/reddit_rss.py --sort new
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
GAP_SECONDS = 12

UA = "windows:detroit-sports-reporter:v1.0 (fan sub reading; no posting)"

SUBS = ["motorcitykitties", "detroitlions", "DetroitPistons", "DetroitRedWings"]


def fetch(url: str) -> str | None:
    CACHE.mkdir(parents=True, exist_ok=True)
    key = re.sub(r"[^a-z0-9]+", "-", url.lower()).strip("-")[:80]
    cached = CACHE / f"{key}.xml"
    if cached.exists():
        age = (time.time() - cached.stat().st_mtime) / 60
        if age < CACHE_MINUTES:
            return cached.read_text(encoding="utf-8")

    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"  rate limited on {url}", file=sys.stderr)
        else:
            print(f"  HTTP {e.code} on {url}", file=sys.stderr)
        return None
    except Exception as e:  # network, DNS, timeout
        print(f"  failed {url}: {e}", file=sys.stderr)
        return None

    cached.write_text(body, encoding="utf-8")
    return body


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


def sweep(subs: list[str], sort: str = "hot") -> dict:
    result = {}
    for i, sub in enumerate(subs):
        if i:
            time.sleep(GAP_SECONDS)
        path = "" if sort == "hot" else f"{sort}/"
        xml = fetch(f"https://www.reddit.com/r/{sub}/{path}.rss")
        result[sub] = parse(xml) if xml else []
        print(f"{sub:20} {len(result[sub]):3} posts", file=sys.stderr)
    return result


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    sort = "hot"
    if "--sort" in argv:
        sort = argv[argv.index("--sort") + 1]
    subs = args or SUBS
    data = sweep(subs, sort)
    print(json.dumps({
        "read_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sort": sort,
        "subs": data,
    }, indent=1)[:12000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
