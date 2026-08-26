#!/usr/bin/env python3
"""Tell the human what happened, without making him a gate.

His reset, 2026-08-26: "I'm too busy to be a human in the loop for most tasks.
Rarely or occasionally is fine but we need some sort of notification process.
Otherwise it's on you to figure out how to make money."

That is 2 instructions. This file is the second half; `CYCLE.md`'s ASK-HUMAN
contract is the first.

**Why GitHub issues.** The channel had to cost him nothing to receive and
nothing to set up. He owns this repo, so GitHub already emails him about issues
in it, and an @mention makes that certain. No new account, no app to install, no
token to paste, no money. An issue also has the one property `ASK-HUMAN.md`
never had: it is *closable*, so a thing that got done stops asking.

Two kinds of message, and the difference matters:

- `--blocker` opens an issue, one per subject, because something genuinely
  cannot proceed without him. Reuses the open issue with the same subject
  instead of opening a second one, so 5 quiet cycles do not become 5 emails.
- `--digest` posts what happened lately and closes itself. It is a report, not
  a request, and it says so in the first line so he can stop reading there.

Nothing here posts anywhere public-facing or spends anything. It writes to the
issue tracker of his own repo.

    python scripts/notify.py --digest --body-file digest.md
    python scripts/notify.py --blocker "gh auth refresh" --body-file ask.md
    python scripts/notify.py --list
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

REPO = "projectunmuted/newsroom"
# His personal account, not the project account this runs as. Mentioning it is
# what turns "an issue exists" into "an email arrived".
MENTION = "@stanleyblume"
BLOCKER_LABEL = "needs-human"


def gh(*args: str, check: bool = True) -> str:
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"gh {' '.join(args[:2])} failed: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def ensure_label() -> None:
    """Create the label once. Failing here is not fatal: a missing label is
    cosmetic and must never be the reason a blocker goes unreported."""
    gh("label", "create", BLOCKER_LABEL, "--repo", REPO, "--color", "d93f0b",
       "--description", "Cannot proceed without the human", check=False)


def open_issues() -> list[dict]:
    out = gh("issue", "list", "--repo", REPO, "--state", "open",
             "--json", "number,title,labels", "--limit", "100")
    return json.loads(out or "[]")


def blocker(subject: str, body: str) -> None:
    """One open issue per subject, ever.

    A cycle that re-detects the same wall every 8 hours must not send a new
    email every 8 hours. That is how a notification channel becomes noise and
    then becomes ignored, which is worse than not having one.
    """
    ensure_label()
    title = f"Needs you: {subject}"
    for i in open_issues():
        if i["title"] == title:
            gh("issue", "comment", str(i["number"]), "--repo", REPO,
               "--body", f"Still blocked as of this cycle.\n\n{body}")
            print(f"commented on existing #{i['number']}: {title}")
            return
    url = gh("issue", "create", "--repo", REPO, "--title", title,
             "--label", BLOCKER_LABEL,
             "--body", f"{MENTION}\n\n{body}\n\n---\nOpened by a cycle. "
                       f"Close it when it is done; nothing else is needed.")
    print(f"opened {url}")


def digest(body: str) -> None:
    """A report that closes itself.

    Left open it would sit in his list looking like a task. The email is the
    product; the issue is just the envelope.
    """
    title = "Digest: what the cycles did"
    url = gh("issue", "create", "--repo", REPO, "--title", title,
             "--body", f"{MENTION}\n\n**Nothing here needs a reply.** This is a "
                       f"report, and it closes itself.\n\n{body}")
    num = url.rstrip("/").rsplit("/", 1)[-1]
    gh("issue", "close", num, "--repo", REPO,
       "--comment", "Closing on creation. This was a report, not a request.",
       check=False)
    print(f"posted and closed {url}")


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--blocker", metavar="SUBJECT",
                   help="something that genuinely cannot proceed without him")
    g.add_argument("--digest", action="store_true", help="a report, no reply wanted")
    g.add_argument("--list", action="store_true", help="what is still open")
    ap.add_argument("--body-file", help="markdown body; falls back to stdin")
    a = ap.parse_args()

    if a.list:
        rows = open_issues()
        if not rows:
            print("nothing open. He owes this project nothing right now.")
            return
        for i in rows:
            labs = ",".join(l["name"] for l in i["labels"]) or "-"
            print(f"  #{i['number']:<4} [{labs}] {i['title']}")
        return

    body = (open(a.body_file, encoding="utf-8").read() if a.body_file
            else sys.stdin.read()).strip()
    if not body:
        sys.exit("empty body; say what happened or what is needed")

    if a.digest:
        digest(body)
    else:
        blocker(a.blocker, body)


if __name__ == "__main__":
    main()
