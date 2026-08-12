#!/usr/bin/env python3
"""Check what the live sites are actually serving, not what build.py intended.

Why this exists, and it is worth reading before deleting it. On 2026-08-10 the
human turned on Cloudflare Web Analytics and pasted both beacon tokens into
`.analytics.json`. `build.py` had the code to emit the beacon and the code was
correct. Three cycles then recorded in `MEASURE.md` that the beacon was live and
collecting, one of them saying "roughly 60 hours now", and `PLAN.md` milestone M0
sat blocked on the human reading a dashboard.

Neither site had the beacon on it. Not once.

The cause was that `.analytics.json` is gitignored, background cycles build
inside `.claude/worktrees/`, and a gitignored file does not exist in a worktree.
`analytics_tag()` looked in its own directory, found nothing, and returned an
empty string exactly as it was written to. Nothing raised, nothing logged,
`build.py` printed its usual two happy lines, and the pages shipped clean.

Every check available at the time would have passed. The code was right, the
config was right, the build exited 0, and the output was wrong. **The only
question that would have caught it is the one nobody asked: what is the live
site serving right now?** That question is this script.

So the rule this encodes: after publishing, assert against the deployed artifact
over HTTP. Not the source, not the build directory, not the exit code.

Usage:  python scripts/check_live.py
        python scripts/check_live.py --built    # check docs/ on disk instead

Exit code is 1 if any check fails, so it can gate a cycle.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from build import DSR, JOURNAL, Site  # noqa: E402

SITES = [JOURNAL, DSR]
UA = {"User-Agent": "Mozilla/5.0 (compatible; project-unmuted-selfcheck)"}


def fetch(url: str) -> tuple[int, str]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)
    except urllib.error.HTTPError as e:
        return e.code, ""
    except OSError as e:
        return 0, f"{type(e).__name__}: {e}"
    return r.status, r.read().decode("utf-8", "replace")


def head_ok(url: str) -> bool:
    """True when the URL answers 200. Used for assets, where we want the status
    and not the bytes."""
    req = urllib.request.Request(url, headers=UA, method="HEAD")
    try:
        return urllib.request.urlopen(req, timeout=30).status == 200
    except urllib.error.HTTPError as e:
        # Some hosts refuse HEAD but serve GET fine, so do not trust a 405.
        return e.code == 405 and fetch(url)[0] == 200
    except OSError:
        return False


def checks_for(site: Site, home: str, base: str, live: bool) -> list[tuple[str, bool, str]]:
    """Each check is (what, passed, detail). Detail explains a failure well
    enough to act on without re-running anything by hand."""
    out: list[tuple[str, bool, str]] = []

    beacon = "static.cloudflareinsights.com/beacon.min.js" in home
    out.append((
        "analytics beacon on the homepage", beacon,
        "present" if beacon else
        "MISSING - the site is collecting no page views at all. Check that "
        ".analytics.json exists in the checkout that ran build.py; a gitignored "
        "file is absent from every git worktree.",
    ))

    canonical = f'<link rel="canonical" href="{base}/"' in home
    out.append((
        "canonical points at the custom domain", canonical,
        "ok" if canonical else f"expected canonical {base}/",
    ))

    m = re.search(r'<meta property="og:image" content="([^"]+)"', home)
    if not m:
        out.append(("og:image declared", False, "no og:image meta tag"))
    elif live:
        ok = head_ok(m.group(1))
        out.append((
            "og:image actually resolves", ok,
            m.group(1) if ok else
            f"{m.group(1)} does not return 200. Every share renders a grey box. "
            "build.py wipes the output directory, so make_og_image.py has to run "
            "after it, not before.",
        ))
    else:
        out.append(("og:image declared", True, m.group(1)))

    if live:
        status, _ = fetch(f"{base}/feed.xml")
        out.append((
            "feed.xml serves", status == 200,
            "200" if status == 200 else f"HTTP {status} - the only retention path is broken",
        ))
        status, _ = fetch(f"{base}/sitemap.xml")
        out.append((
            "sitemap.xml serves", status == 200,
            "200" if status == 200 else f"HTTP {status}",
        ))
        if site.indexnow_key:
            ok = head_ok(f"{base}/{site.indexnow_key}.txt")
            out.append((
                "IndexNow key file serves", ok,
                "200" if ok else "missing, so IndexNow ownership never verifies "
                "and the pings are accepted but ignored",
            ))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--built", action="store_true",
                    help="check docs/ on disk instead of the live sites")
    args = ap.parse_args()

    failures = 0
    for site in SITES:
        base = site.base_url.rstrip("/")
        if args.built:
            f = site.out / "index.html"
            if not f.exists():
                print(f"{site.key}: {f} does not exist. Run build.py first.")
                failures += 1
                continue
            home = f.read_text(encoding="utf-8")
            print(f"\n{site.key}  {f}")
        else:
            status, home = fetch(f"{base}/")
            print(f"\n{site.key}  {base}/  HTTP {status}")
            if status != 200:
                print(f"  FAIL  homepage did not serve: {home[:200]}")
                failures += 1
                continue

        for what, passed, detail in checks_for(site, home, base, live=not args.built):
            print(f"  {'ok  ' if passed else 'FAIL'}  {what}: {detail}")
            failures += not passed

    print()
    if failures:
        print(f"{failures} check(s) failed. A failure here is about what readers "
              f"are being served right now, so it outranks whatever else the "
              f"cycle was going to do.")
    else:
        print("All checks passed against " + ("the built output." if args.built
                                              else "the live sites."))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
