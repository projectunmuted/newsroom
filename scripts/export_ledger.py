#!/usr/bin/env python3
"""Generate the public prediction-ledger artifact in ledger/.

    python scripts/export_ledger.py --refresh   # re-pull git, GitHub, MLB
    python scripts/export_ledger.py             # regenerate from the cache
    python scripts/export_ledger.py --check     # diff against a temp build,
                                                # exit 1 if ledger/ is stale

Why this exists: `MONEY.md` ranks "the data as an artifact" third among the
things that can move with nobody, and says in as many words that "the pick
ledger with pre-game commit timestamps is the remaining half of this item and is
not done." This is that half.

**What the artifact actually is.** Detroit Sports Reporter's whole claim is that
a prediction was published before the game it predicts. Until this script ran,
that claim rested on a markdown table nobody could audit. Every row here carries
3 timestamps a stranger can re-derive without asking anybody:

1. the git commit that first introduced the pick row into `PICKS.md`,
2. the moment GitHub's own events API recorded that commit being pushed to the
   public repo, which is a third party witnessing it rather than us asserting it,
3. first pitch, from the MLB Stats API, matched on `gamePk`.

A commit timestamp on its own is worth very little: whoever makes the commit
chooses it. The push timestamp is the one that matters, because it is written by
GitHub. Both are in the CSV and the README says which is which.

**The GitHub events API keeps roughly 90 days**, so the raw push events are
snapshotted into `ledger/github-push-events.json` as a receipt. After 90 days
that file is the only copy of the witness and it cannot be regenerated.

Everything in `ledger/` is generated. The README prose lives in this file as a
template and every number in it is computed from the same rows that go into the
CSV, the same contract as `export_dataset.py`.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, "ledger_cache.json")
OUT = os.path.join(ROOT, "ledger")
PICKS = os.path.join(ROOT, "PICKS.md")

REPO = "projectunmuted/newsroom"
CSV_NAME = "predictions.csv"
EVENTS_NAME = "github-push-events.json"

ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\(`(\d+)`\)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|"
    r"\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")


def strip_md(s):
    return s.replace("**", "").strip()


def parse_picks():
    rows = []
    with io.open(PICKS, encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line.rstrip("\n"))
            if not m:
                continue
            seq, matchup, pk, first_pitch, call, conf, result, grade = m.groups()
            grade = strip_md(grade)
            if grade.startswith("✅"):
                correct = "true"
            elif grade.startswith("❌"):
                correct = "false"
            else:
                correct = ""          # still pending
            rows.append({
                "pick": int(seq),
                "game_pk": int(pk),
                "matchup": strip_md(matchup),
                "first_pitch_local_text": strip_md(first_pitch),
                "prediction": strip_md(call),
                "confidence": strip_md(conf),
                "final_score": "" if strip_md(result) == "—" else strip_md(result),
                "correct": correct,
            })
    if not rows:
        raise SystemExit("parsed 0 rows out of PICKS.md; the table format moved")
    return rows


def git(*args):
    p = subprocess.run(["git"] + list(args), cwd=ROOT,
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr))
    return p.stdout


def first_commit_for(game_pk):
    """The commit that first put this gamePk into PICKS.md."""
    out = git("log", "--reverse", "--format=%H %cI", "-S", str(game_pk),
              "--", "PICKS.md")
    lines = out.strip().splitlines()
    if not lines:
        return None, None
    sha, when = lines[0].split()
    return sha, when


def gh_json(path):
    p = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("gh api %s failed: %s" % (path, p.stderr.strip()))
    return json.loads(p.stdout)


def pull_push_events():
    """Main-branch push events from GitHub. Retention is about 90 days."""
    events = []
    for page in range(1, 4):
        batch = gh_json("repos/%s/events?per_page=100&page=%d" % (REPO, page))
        if not batch:
            break
        events.extend(batch)
    return [{"created_at": e["created_at"],
             "before": e["payload"]["before"],
             "head": e["payload"]["head"]}
            for e in events
            if e["type"] == "PushEvent"
            and e["payload"].get("ref") == "refs/heads/main"]


def feed_is_behind(events):
    """True when GitHub's events feed has not caught up with local main yet.

    The feed is served from an asynchronously refreshed cache and answers 200
    with a stale body, so a script that pushes and then reads back its own
    PushEvent gets a confident empty answer rather than an error. Observed
    2026-08-29: the feed's newest event was 8 hours old while the push was 6
    minutes old. Written up in
    findings/github-events-api-lags-a-push-so-read-after-write-returns-200-and-nothing.md.

    Returns (behind, newest_event_utc, head_commit_utc). `behind` being True
    means an unwitnessed row is *unknown*, not absent, and the correct response
    is to try again on a later run rather than to conclude anything.
    """
    if not events:
        return True, "", ""
    newest = max(e["created_at"] for e in events)
    out = git("log", "-1", "--format=%cI", "main")
    head = to_utc(out.strip()) if out else ""
    if not head:
        return False, newest, ""
    return parse_utc(newest) < parse_utc(head), newest, head


def push_time_for(sha, events):
    """Earliest push event whose range contains this commit."""
    best = None
    for e in events:
        p = subprocess.run(["git", "rev-list", e["before"] + ".." + e["head"]],
                           cwd=ROOT, capture_output=True, text=True)
        shas = p.stdout.split() if p.returncode == 0 else [e["head"]]
        if sha in shas and (best is None or e["created_at"] < best):
            best = e["created_at"]
    return best


def mlb_game(game_pk):
    url = "https://statsapi.mlb.com/api/v1/schedule?gamePk=%d" % game_pk
    with urllib.request.urlopen(url, timeout=30) as fh:
        d = json.load(fh)
    g = d["dates"][0]["games"][0]
    return {"first_pitch_utc": g["gameDate"].replace("+00:00", "Z"),
            "status": g["status"]["detailedState"]}


def to_utc(iso):
    d = dt.datetime.fromisoformat(iso)
    return d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc)


def merge_events(fresh):
    """Union the live events with whatever the cache already holds.

    GitHub serves roughly 90 days of events, so a plain overwrite would silently
    drop the witness for every older prediction and the artifact would keep
    publishing as if nothing had happened. Once a push event has been seen it is
    kept forever; the snapshot only ever grows.
    """
    kept = {}
    if os.path.exists(CACHE):
        with io.open(CACHE, encoding="utf-8") as fh:
            for e in json.load(fh).get("push_events", []):
                kept[(e["created_at"], e["head"])] = e
    added = 0
    for e in fresh:
        key = (e["created_at"], e["head"])
        if key not in kept:
            kept[key] = e
            added += 1
    print("push events: %d already held, %d new" % (len(kept) - added, added))
    return sorted(kept.values(), key=lambda e: e["created_at"], reverse=True)


def refresh():
    picks = parse_picks()
    events = merge_events(pull_push_events())
    if not events:
        raise SystemExit("GitHub returned no main-branch push events; refusing "
                         "to write a cache with no witness in it")
    for row in picks:
        sha, when = first_commit_for(row["game_pk"])
        if not sha:
            raise SystemExit("no commit introduces gamePk %d into PICKS.md"
                             % row["game_pk"])
        row["commit_sha"] = sha
        row["commit_time_utc"] = to_utc(when)
        row["github_push_time_utc"] = push_time_for(sha, events) or ""
        row.update(mlb_game(row["game_pk"]))
    cache = {"generated": dt.datetime.now(dt.timezone.utc)
             .strftime("%Y-%m-%dT%H:%M:%SZ"),
             "repo": REPO, "picks": picks, "push_events": events}
    with io.open(CACHE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cache, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("cached %d picks and %d push events" % (len(picks), len(events)))
    return cache


FIELDS = ["pick", "game_pk", "matchup", "first_pitch_utc",
          "first_pitch_local_text", "prediction", "confidence", "final_score",
          "correct", "commit_sha", "commit_time_utc", "github_push_time_utc",
          "minutes_pushed_before_first_pitch", "commit_url"]


def build(cache, dest):
    picks = sorted(cache["picks"], key=lambda r: r["pick"])
    for r in picks:
        fp = parse_utc(r["first_pitch_utc"])
        if r["github_push_time_utc"]:
            delta = (fp - parse_utc(r["github_push_time_utc"])).total_seconds()
            r["minutes_pushed_before_first_pitch"] = str(int(delta // 60))
        else:
            r["minutes_pushed_before_first_pitch"] = ""
        r["commit_url"] = "https://github.com/%s/commit/%s" % (
            cache["repo"], r["commit_sha"])

    os.makedirs(dest, exist_ok=True)
    with io.open(os.path.join(dest, CSV_NAME), "w", encoding="utf-8",
                 newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for r in picks:
            w.writerow({k: r.get(k, "") for k in FIELDS})

    with io.open(os.path.join(dest, EVENTS_NAME), "w", encoding="utf-8",
                 newline="\n") as fh:
        json.dump({"repo": cache["repo"],
                   "note": ("Raw PushEvent records from GitHub's events API for "
                            "the branch these predictions are committed to. "
                            "GitHub retains these for roughly 90 days; this file "
                            "is a snapshot taken while they were still live and "
                            "cannot be regenerated afterwards."),
                   "snapshotted": cache["generated"],
                   "events": cache["push_events"]},
                  fh, indent=1, sort_keys=True)
        fh.write("\n")

    with io.open(os.path.join(dest, "README.md"), "w", encoding="utf-8",
                 newline="\n") as fh:
        fh.write(readme(picks, cache))

    shutil.copy2(os.path.join(HERE, "verify_ledger.py"),
                 os.path.join(dest, "verify.py"))
    return picks


def readme(picks, cache):
    graded = [r for r in picks if r["correct"] in ("true", "false")]
    right = sum(1 for r in graded if r["correct"] == "true")
    wrong = len(graded) - right
    margins = [int(r["minutes_pushed_before_first_pitch"])
               for r in picks if r["minutes_pushed_before_first_pitch"]]
    margins_sorted = sorted(margins)
    late = [r for r in picks
            if r["minutes_pushed_before_first_pitch"]
            and int(r["minutes_pushed_before_first_pitch"]) <= 0]
    unwitnessed = [r for r in picks if not r["github_push_time_utc"]]
    tightest = min(margins) if margins else 0
    widest = max(margins) if margins else 0
    median = margins_sorted[len(margins_sorted) // 2] if margins else 0

    rows = "\n".join(
        "| %d | %s | %s | %s | %s | %s | %s |" % (
            r["pick"], r["matchup"], r["prediction"], r["confidence"],
            r["final_score"] or "not played yet",
            {"true": "correct", "false": "wrong", "": "pending"}[r["correct"]],
            r["minutes_pushed_before_first_pitch"] or "-")
        for r in picks)

    return TEMPLATE.format(
        n=len(picks), graded=len(graded), right=right, wrong=wrong,
        tightest=tightest, widest=widest, median=median,
        late=len(late), unwitnessed=len(unwitnessed),
        rows=rows, repo=cache["repo"], generated=cache["generated"],
        hours_tightest=round(tightest / 60.0, 1),
        hours_median=round(median / 60.0, 1),
    )


TEMPLATE = """# How do you prove a prediction was made before the event?

You publish it somewhere you cannot quietly edit, and you let a third party
record when you did.

This repository is a working example of that, and the audit trail behind it.
{n} baseball game predictions, each one committed to a public git repository
before first pitch, each one graded afterwards against the league's own game id.
Every row carries the evidence, and nothing here asks you to take a number on
trust.

## The record

**{right}-{wrong}** on {graded} graded predictions. {n} committed in total.

That is a small sample and it is not the point of this repository. A coin lands
{right}-{wrong} often enough that no honest reading of it says anything yet. The
point is the method: the record can only ever get more auditable, and a bad run
cannot be quietly deleted, because deleting it would leave a hole in a public
commit history.

## The three timestamps

Each prediction in `predictions.csv` carries all three.

| Column | What it is | Who controls it |
|---|---|---|
| `commit_time_utc` | when the pick row was committed to `PICKS.md` | **us**, and that matters |
| `github_push_time_utc` | when GitHub's events API recorded the push | **GitHub** |
| `first_pitch_utc` | scheduled first pitch, from the MLB Stats API on `gamePk` | **MLB** |

The first one is close to worthless on its own. Git lets whoever makes a commit
write any date they like into it, so a self-reported commit timestamp proves
nothing about when the work happened. Anybody publishing a prediction record
with commit timestamps and no other witness is showing you a number they chose.

The second one is the actual evidence. GitHub writes `created_at` on a
`PushEvent` when it receives the push, from its own clock, and serves it through
a public API to anybody who asks. It is the moment the prediction became visible
to the world.

The third one comes from the league.

`minutes_pushed_before_first_pitch` is column 2 subtracted from column 3. If it
is ever zero or negative, the prediction was not a prediction.

## What the audit says

- Predictions where the push landed **after** first pitch: **{late}**
- Predictions with **no** GitHub push record found: **{unwitnessed}**
- Tightest margin: **{tightest} minutes** ({hours_tightest} hours) before first pitch
- Median margin: **{median} minutes** ({hours_median} hours)
- Widest margin: **{widest} minutes**

## The predictions

| # | Game | Call | Confidence | Final | Grade | Minutes before first pitch |
|---|---|---|---|---|---|---|
{rows}

Confidence has two settings and no percentages. High means the caller expects to
look stupid if it misses. Low means picking a side is the job.

## Verify it yourself

`verify.py` re-derives every column above from public APIs. It needs Python 3
and nothing else, no key and no account:

    python verify.py

It fetches each commit from GitHub's API, each game from the MLB Stats API, and
recomputes the margin. It prints a line per prediction and exits non-zero if any
one of them fails.

To check a single row by hand:

    curl -s https://api.github.com/repos/{repo}/commits/COMMIT_SHA
    curl -s "https://statsapi.mlb.com/api/v1/schedule?gamePk=GAME_PK"

## The honest limits

- **90 days.** GitHub's events API only serves recent events, so
  `github-push-events.json` is a snapshot taken while they were live. After that
  window closes, the file is the only copy, and it is a file in a repository we
  control, which makes it a weaker witness than the live API. Verify early if it
  matters to you. The commit objects themselves do not expire.
- **A push proves publication, not authorship.** It shows the text was public at
  that instant. It cannot show who wrote it or how.
- **Small sample.** {graded} graded games. Treat the win-loss line as a record
  being kept, not as a result.
- **This is analysis and entertainment, not betting advice.** No odds, no stakes
  and no staking guidance, here or on the site it comes from.

## Where these come from

The predictions are written and graded by an AI system at
[detroitsportsreporter.com](https://detroitsportsreporter.com), which covers the
Tigers, Lions, Pistons and Red Wings. The full source, including every commit in
this audit trail, is [{repo}](https://github.com/{repo}). The project's working
journal is at [project-unmuted.com](https://project-unmuted.com).

`predictions.csv` and this README are generated by `scripts/export_ledger.py` in
that repository from a cached pull, so no number here can drift from the data
beside it. Generated {generated}.
"""


def main():
    args = sys.argv[1:]
    if "--refresh" in args:
        cache = refresh()
    else:
        if not os.path.exists(CACHE):
            raise SystemExit("no cache at %s; run with --refresh" % CACHE)
        with io.open(CACHE, encoding="utf-8") as fh:
            cache = json.load(fh)

    if "--check" in args:
        tmp = tempfile.mkdtemp(prefix="ledger-check-")
        try:
            build(cache, tmp)
            stale = []
            for name in sorted(os.listdir(tmp)):
                a, b = os.path.join(tmp, name), os.path.join(OUT, name)
                if not os.path.exists(b):
                    stale.append(name + " (missing)")
                elif io.open(a, "rb").read() != io.open(b, "rb").read():
                    stale.append(name + " (differs)")
            if stale:
                sys.stderr.write("ledger/ is stale: %s\n" % ", ".join(stale))
                return 1
            print("ledger/ matches the cache")
            return 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    picks = build(cache, OUT)
    graded = [r for r in picks if r["correct"] in ("true", "false")]
    late = [r for r in picks if r["minutes_pushed_before_first_pitch"]
            and int(r["minutes_pushed_before_first_pitch"]) <= 0]
    missing = [r for r in picks if not r["github_push_time_utc"]]
    print("wrote %s: %d predictions, %d graded" % (OUT, len(picks), len(graded)))
    print("pushed after first pitch: %d" % len(late))
    print("no GitHub push witness: %d" % len(missing))
    for r in late:
        print("  LATE  pick %d (%s)" % (r["pick"], r["game_pk"]))
    for r in missing:
        print("  UNWITNESSED  pick %d (%s)" % (r["pick"], r["game_pk"]))
    if missing:
        behind, newest, head = feed_is_behind(cache["push_events"])
        if behind:
            print("  NOTE  GitHub's events feed is behind local main: newest "
                  "event %s, HEAD committed %s. An unwitnessed row here is "
                  "unknown, not absent. Re-run on a later cycle before "
                  "concluding anything." % (newest or "none", head or "?"))
    return 1 if (late or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
