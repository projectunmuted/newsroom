#!/usr/bin/env python3
"""Ask whether either site is actually in a search index, not whether IndexNow said 200.

Why this exists. `CYCLE.md` has carried the line "search is seeded: IndexNow
accepted all URLs 2026-08-08" since the day it was true, and every cycle since
has re-pinged IndexNow and recorded another 200. A 200 from api.indexnow.org
means one thing: the submission was accepted. It says nothing about whether a
crawler came, whether a page was stored, or whether a human searching for the
exact title of an entry would ever be shown it.

That is the same shape of mistake as the analytics beacon in `check_live.py`.
The input was fine and nobody asked what the output was. So this script asks the
output question: type a phrase that appears on our pages and nowhere else into a
real search engine, and see whether our page comes back.

**The control is the point.** A scrape of a search results page can return zero
hits because the page is not indexed, or because the engine served a captcha, a
consent wall, or an empty shell to a script. Those are indistinguishable from
the outside, and a cycle reading "0 results" as "not indexed" would be repeating
the exact error this file was written to prevent. So every run first issues a
control query whose correct answer is known and non-empty. If the control comes
back empty the engine is not answering us, the run is reported as UNRELIABLE for
that engine, and no conclusion is drawn from its zeros.

Usage:  python scripts/search_index_check.py
        python scripts/search_index_check.py --json

Exit codes:
    0  at least one engine answered its control, and our pages were found
    1  at least one engine answered its control, and our pages were not found
    2  no engine answered its control; the run proves nothing either way
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

OUR_DOMAINS = ("detroitsportsreporter.com", "project-unmuted.com")

# Phrases that appear verbatim in a published title on one of our sites and,
# as far as anything can be, nowhere else on the web. Keep these to entries
# that have been live for at least a week, or a miss only proves the page is
# new. Each is (label, phrase, which site it lives on).
OUR_PHRASES = [
    (
        "dsr-pick1",
        "the unluckiest team in baseball plays the worst team in California",
        "detroitsportsreporter.com",
    ),
    (
        "dsr-backtest",
        "I tested my own method on 1,743 games before asking you to trust it",
        "detroitsportsreporter.com",
    ),
    (
        "journal-lane",
        "Third time, with a lane",
        "project-unmuted.com",
    ),
]

# A phrase that is definitely indexed and definitely obscure, so a zero here
# means the engine is refusing us rather than telling us something true. It is
# the title of a small Substack post, chosen because a big-site title could be
# answered from an engine's own cache of popular queries.
CONTROL_PHRASE = "The Royals And A's Are Racing To The Bottom"
CONTROL_EXPECT = "neilpaine.substack.com"

ENGINES = {
    "bing": "https://www.bing.com/search?q={q}&count=30",
    "ddg": "https://html.duckduckgo.com/html/?q={q}",
    "mojeek": "https://www.mojeek.com/search?q={q}",
    "marginalia": "https://old-search.marginalia.nu/search?query={q}",
}

LINK_RE = re.compile(r'https?://[^\s"\'<>]+', re.I)


def fetch(url: str, timeout: int = 40) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:  # 202/403/429 all land here or above
        return e.code, ""
    except Exception:
        return 0, ""


def search(engine: str, phrase: str) -> tuple[int, str]:
    q = urllib.parse.quote_plus('"%s"' % phrase)
    return fetch(ENGINES[engine].format(q=q))


def contains_host(body: str, host: str) -> bool:
    """True if any link on the results page points at `host`.

    Substring-matching the bare domain would count our own query string echoed
    back in the page, so only real links count.
    """
    for link in LINK_RE.findall(body):
        netloc = urllib.parse.urlparse(link).netloc.lower()
        if netloc == host or netloc.endswith("." + host):
            # Skip the engine's own redirector pointing at itself.
            return True
    return False


def run(sleep: float = 2.0) -> dict:
    out = {"engines": {}, "found": [], "not_found": [], "unreliable": []}
    for engine in ENGINES:
        status, body = search(engine, CONTROL_PHRASE)
        ok = bool(body) and contains_host(body, CONTROL_EXPECT)
        out["engines"][engine] = {
            "control_status": status,
            "control_bytes": len(body),
            "control_passed": ok,
            "results": {},
        }
        if not ok:
            out["unreliable"].append(engine)
            print("%-11s control FAILED (http %s, %d bytes) -- zeros from this "
                  "engine prove nothing" % (engine, status, len(body)))
            continue
        print("%-11s control passed" % engine)
        time.sleep(sleep)
        for label, phrase, host in OUR_PHRASES:
            st, b = search(engine, phrase)
            hit = bool(b) and contains_host(b, host)
            out["engines"][engine]["results"][label] = {
                "status": st, "bytes": len(b), "found": hit,
            }
            key = "found" if hit else "not_found"
            out[key].append("%s:%s" % (engine, label))
            print("   %-14s %s  (http %s, %d bytes)"
                  % (label, "FOUND" if hit else "not found", st, len(b)))
            time.sleep(sleep)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="dump the raw result")
    ap.add_argument("--sleep", type=float, default=2.0, help="seconds between queries")
    args = ap.parse_args()

    res = run(sleep=args.sleep)
    reliable = [e for e in res["engines"] if res["engines"][e]["control_passed"]]

    print()
    print("engines answering: %s" % (", ".join(reliable) or "none"))
    print("unreliable:        %s" % (", ".join(res["unreliable"]) or "none"))
    print("our pages found:   %d of %d checks"
          % (len(res["found"]), len(res["found"]) + len(res["not_found"])))

    if args.json:
        print(json.dumps(res, indent=1))

    if not reliable:
        print("\nVERDICT: no engine answered its control. This run says nothing "
              "about whether the sites are indexed. Do not record a number.")
        return 2
    if res["found"]:
        print("\nVERDICT: at least one of our pages is in an index.")
        return 0
    print("\nVERDICT: %d engine(s) answered their control and returned none of "
          "our pages for phrases that appear on them verbatim. On the evidence "
          "available here the sites are not in those indexes." % len(reliable))
    return 1


if __name__ == "__main__":
    sys.exit(main())
