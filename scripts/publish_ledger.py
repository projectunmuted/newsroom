#!/usr/bin/env python3
"""Publish ledger/ to the standalone public repo
projectunmuted/prove-a-prediction-was-made-before-the-event.

Same contract as publish.py, publish_findings.py and publish_dataset.py: this
repo holds the source and the cache, the other repo is publish output and is
never edited by hand. Idempotent; exits 0 with a message when there is nothing
to push.

Why a separate repo rather than a folder here: `PLAN.md` M4 says a citation from
somewhere else is the gate on everything downstream, and a repository whose name
is the question somebody types is the shape of thing that gets linked. A
subfolder of an unrelated repository is not.

**Refuses to publish a stale ledger.** `export_ledger.py --check` runs first, so
what gets pushed is always what the cache generates. And it re-runs the audit:
if any prediction turns out to have been pushed after first pitch, or to have no
GitHub push record at all, this script stops. Publishing a proof-of-priority
artifact that fails its own proof would be worse than publishing nothing.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO_NAME = "prove-a-prediction-was-made-before-the-event"
REMOTE = "https://github.com/projectunmuted/%s.git" % REPO_NAME
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "ledger")

# Allowlist rather than copy-everything, so a scratch file in ledger/ cannot
# end up in a public repository.
PUBLISH = (".csv", ".md", ".json", ".py")


def run(cmd, cwd, check=True):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        sys.stderr.write("FAILED %s\n%s\n%s\n" % (cmd, p.stdout, p.stderr))
        sys.exit(2)
    return p


def audit_passes():
    """Re-run the ledger build and refuse to publish if the audit fails."""
    p = subprocess.run([sys.executable, os.path.join(HERE, "export_ledger.py")],
                       capture_output=True, text=True)
    print(p.stdout.strip())
    if p.returncode != 0:
        sys.stderr.write("the ledger audit failed; refusing to publish an "
                         "artifact that does not survive its own check\n%s\n"
                         % p.stderr)
        return False
    return True


def main():
    if not os.path.isdir(SRC):
        sys.stderr.write("no ledger/ directory at %s\n" % SRC)
        return 2

    if not audit_passes():
        return 1

    check = subprocess.run(
        [sys.executable, os.path.join(HERE, "export_ledger.py"), "--check"],
        capture_output=True, text=True)
    if check.returncode != 0:
        sys.stderr.write(
            "ledger/ does not match the cache, refusing to publish.\n"
            "Run: python scripts/export_ledger.py\n%s\n" % check.stderr)
        return 1
    print(check.stdout.strip())

    tmp = tempfile.mkdtemp(prefix="ledger-pub-")
    try:
        run(["git", "clone", "--depth", "1", REMOTE, "repo"], tmp, check=False)
        repo = os.path.join(tmp, "repo")
        if not os.path.isdir(os.path.join(repo, ".git")):
            os.makedirs(repo, exist_ok=True)
            run(["git", "init", "-b", "main"], repo)
            run(["git", "remote", "add", "origin", REMOTE], repo)
        for name in os.listdir(repo):
            if name == ".git":
                continue
            path = os.path.join(repo, name)
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
        copied = 0
        for name in sorted(os.listdir(SRC)):
            if name.endswith(PUBLISH):
                shutil.copy2(os.path.join(SRC, name), os.path.join(repo, name))
                copied += 1
        if not copied:
            sys.stderr.write("nothing to publish from %s\n" % SRC)
            return 2
        run(["git", "add", "-A"], repo)
        if not run(["git", "status", "--porcelain"], repo).stdout.strip():
            print("%s already up to date, nothing to push" % REPO_NAME)
            return 0
        with io.open(os.path.join(SRC, "predictions.csv"), encoding="utf-8") as fh:
            n = sum(1 for _ in fh) - 1
        run(["git", "commit", "-m",
             "Publish the prediction ledger: %d predictions with push "
             "timestamps" % n], repo)
        run(["git", "push", "-u", "origin", "main"], repo)
        head = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
        print("pushed %s (%d files) to %s" % (head[:8], copied, REMOTE))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
