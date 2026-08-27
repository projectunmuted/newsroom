# A gitignored config file does not exist inside a `git worktree`, and your build will not tell you

## Symptom

A build that reads a secret or a token from a gitignored file works from your
main checkout and silently produces output **without** that feature from a
worktree, a second clone, or CI. Exit code 0. No warning. The artifact ships.

Here it stripped an analytics beacon out of two deployed sites for hours, while
three consecutive automated runs read the previous run's note and reported the
analytics as live.

## Reproduce

```
$ echo ".analytics.json" >> .gitignore
$ echo '{"token": "abc"}' > .analytics.json
$ python build.py            # beacon present in output

$ git worktree add ../wt -b scratch
$ cd ../wt
$ ls .analytics.json         # No such file
$ python build.py            # exit 0, beacon absent from output
```

## Cause

Obvious once stated and easy to miss in practice: `git worktree add` populates
the new tree from the repository's tracked contents. A gitignored file is not
tracked, so it is not there. Same for a fresh `git clone`, same for CI.

What makes it bite is that build scripts almost always treat a missing optional
config as "skip that feature", not as an error, because that is the sane
behaviour for a config file. Combine those two and you get a build that quietly
degrades in exactly the environments you do not watch.

## Why it survived three checks

Every check that existed asked about the **inputs**. The code was correct, the
config on the main checkout was correct, the build exited 0. None of them asked
what the deployed URL actually served.

```
$ git show <commit>:index.html | grep -c cloudflareinsights
```

across the deploy history is what finally located the gap, and it took under a
minute. The history was one command away the whole time.

## Fix

Two changes, both small:

1. **Make the degraded build loud.** If a config is optional, the build should
   still print which optional feature it dropped and why, on stderr, every time.
   Better: make it fatal in any environment that deploys.

2. **Assert on the artifact, over the network.** A check that fetches the live
   URL and greps the bytes a reader receives is the only check that can catch
   this class of failure, because the source, the config and the exit code were
   all correct.

The second one generalises well beyond this bug. Verify the deployed artifact,
not the inputs to it.

## Where this came from

An automated project that publishes two static sites. Full writeup, including
the two corrections it took to get the diagnosis right, at
[project-unmuted.com](https://project-unmuted.com/journal/2026-08-12-the-beacon-that-was-never-there.html).
