#!/usr/bin/env python3
"""Publish datasets/ to the standalone public repo
projectunmuted/nfl-preseason-vs-regular-season.

Same pattern as publish.py and publish_findings.py: this repo holds the source,
the other repo is publish output and is never edited by hand. Idempotent; exits
0 with a message when there is nothing to push.

Why a separate repo rather than a folder in the newsroom: a dataset is the
shape of thing people link to and cite, and `PLAN.md` M4 says a citation is the
gate on everything downstream of it. A repo whose name is the question somebody
types gets found where a subfolder of an unrelated repo does not. Rationale in
`MONEY.md`, "What can move with nobody", item 3.

**Refuses to publish a stale dataset.** `export_dataset.py --check` runs first,
so the files pushed are always the ones the current cache generates. That guard
exists because the 08-21 Reddit draft shipped a stat that had moved since it was
written, and a published dataset drifting from its source would be the same
failure with a longer half-life.
"""
import os
import shutil
import subprocess
import sys
import tempfile

REPO_NAME = "nfl-preseason-vs-regular-season"
REMOTE = "https://github.com/projectunmuted/%s.git" % REPO_NAME
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "datasets")

# Only these are published. An allowlist rather than a copy-everything, so a
# stray scratch file in datasets/ cannot end up in a public repo.
PUBLISH = (".csv", ".md", ".json")


def run(cmd, cwd, check=True):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        sys.stderr.write("FAILED %s\n%s\n%s\n" % (cmd, p.stdout, p.stderr))
        sys.exit(2)
    return p


def main():
    if not os.path.isdir(SRC):
        sys.stderr.write("no datasets/ directory at %s\n" % SRC)
        return 2

    check = subprocess.run(
        [sys.executable, os.path.join(HERE, "export_dataset.py"), "--check"],
        capture_output=True, text=True)
    if check.returncode != 0:
        sys.stderr.write(
            "datasets/ does not match the cache, refusing to publish.\n"
            "Run: python scripts/export_dataset.py\n%s\n" % check.stderr)
        return 1
    print(check.stdout.strip())

    tmp = tempfile.mkdtemp(prefix="dataset-")
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
        run(["git", "commit", "-m",
             "Publish the NFL preseason dataset from the newsroom repo"], repo)
        run(["git", "push", "-u", "origin", "main"], repo)
        head = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
        print("pushed %s (%d files) to %s" % (head[:8], copied, REMOTE))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
