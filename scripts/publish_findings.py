#!/usr/bin/env python3
"""Publish findings/ to the standalone public repo projectunmuted/api-gotchas.

Same pattern as publish.py: this repo holds the source, the other repo is
publish output and is never edited by hand. Idempotent; exits 0 with a message
when there is nothing to push.

Why a separate repo rather than a folder in the newsroom: the point of these
files is to be found by somebody searching the symptom, and a repo whose name
and description are the symptoms ranks where a subfolder of an unrelated repo
does not. Rationale in MONEY.md, "What can move with nobody".
"""
import os, shutil, subprocess, sys, tempfile

REMOTE = "https://github.com/projectunmuted/api-gotchas.git"
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "findings")


def run(cmd, cwd, check=True):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and p.returncode != 0:
        sys.stderr.write("FAILED %s\n%s\n%s\n" % (cmd, p.stdout, p.stderr))
        sys.exit(2)
    return p


def main():
    if not os.path.isdir(SRC):
        sys.stderr.write("no findings/ directory at %s\n" % SRC)
        return 2
    tmp = tempfile.mkdtemp(prefix="findings-")
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
        for name in sorted(os.listdir(SRC)):
            if name.endswith(".md"):
                shutil.copy2(os.path.join(SRC, name), os.path.join(repo, name))
        run(["git", "add", "-A"], repo)
        if not run(["git", "status", "--porcelain"], repo).stdout.strip():
            print("api-gotchas already up to date, nothing to push")
            return 0
        run(["git", "commit", "-m", "Publish findings from the newsroom repo"], repo)
        run(["git", "push", "-u", "origin", "main"], repo)
        head = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
        print("pushed %s to %s" % (head[:8], REMOTE))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
