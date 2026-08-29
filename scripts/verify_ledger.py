#!/usr/bin/env python3
"""Independently re-verify every row of predictions.csv.

    python verify.py

Copied verbatim into the published ledger repository as `verify.py`, which is
why it takes no arguments, imports nothing outside the standard library, and
needs no key, no token and no account. A reader who does not trust this project
should be able to run it on a laptop and reach their own conclusion.

What it re-derives from scratch, per row:

- the commit exists in the public repository, and GitHub reports its committer
  date. (GitHub's copy, not the CSV's copy.)
- the game exists in the MLB Stats API under that `gamePk`, and the league
  reports its scheduled first pitch.
- first pitch minus the recorded push time equals the margin in the CSV, and
  that margin is positive.

What it cannot re-derive: the push timestamps themselves, once GitHub's events
API has aged them out at roughly 90 days. Those live in
`github-push-events.json`, and for rows past that window the script says so
rather than pretending it checked. Unverifiable is printed as unverifiable.

Exit 0 all rows pass, 1 any row fails, 2 the network or the files got in the way.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "predictions.csv")
EVENTS_PATH = os.path.join(HERE, "github-push-events.json")
UA = {"User-Agent": "prediction-ledger-verifier"}
TOLERANCE_SECONDS = 90


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as fh:
        return json.load(fh)


def parse_utc(s):
    s = s.replace("Z", "+00:00")
    return dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc)


def main():
    if not os.path.exists(CSV_PATH):
        sys.stderr.write("no predictions.csv beside this script\n")
        return 2
    with io.open(CSV_PATH, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.stderr.write("predictions.csv has no rows\n")
        return 2

    witnessed = set()
    if os.path.exists(EVENTS_PATH):
        with io.open(EVENTS_PATH, encoding="utf-8") as fh:
            snap = json.load(fh)
        witnessed = {e["head"] for e in snap.get("events", [])}
        repo = snap.get("repo", "projectunmuted/newsroom")
    else:
        repo = "projectunmuted/newsroom"

    failures = 0
    for r in rows:
        pick = r["pick"]
        problems = []
        notes = []

        try:
            commit = get_json("https://api.github.com/repos/%s/commits/%s"
                              % (repo, r["commit_sha"]))
            gh_date = parse_utc(commit["commit"]["committer"]["date"])
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429):
                sys.stderr.write("GitHub rate limited this machine (%d). "
                                 "Wait an hour or use a token.\n" % exc.code)
                return 2
            problems.append("commit %s not found on GitHub (%d)"
                            % (r["commit_sha"][:8], exc.code))
            gh_date = None
        if gh_date is not None:
            claimed = parse_utc(r["commit_time_utc"])
            if abs((gh_date - claimed).total_seconds()) > TOLERANCE_SECONDS:
                problems.append("commit date disagrees: GitHub says %s, CSV "
                                "says %s" % (gh_date.isoformat(),
                                             r["commit_time_utc"]))

        try:
            sched = get_json("https://statsapi.mlb.com/api/v1/schedule?gamePk=%s"
                             % r["game_pk"])
            game = sched["dates"][0]["games"][0]
            first_pitch = parse_utc(game["gameDate"])
        except Exception as exc:                       # noqa: BLE001
            problems.append("MLB lookup failed for gamePk %s: %s"
                            % (r["game_pk"], exc))
            first_pitch = None
        if first_pitch is not None:
            claimed = parse_utc(r["first_pitch_utc"])
            if abs((first_pitch - claimed).total_seconds()) > TOLERANCE_SECONDS:
                problems.append("first pitch disagrees: MLB says %s, CSV says %s"
                                % (first_pitch.isoformat(), r["first_pitch_utc"]))

        pushed = r.get("github_push_time_utc") or ""
        margin = r.get("minutes_pushed_before_first_pitch") or ""
        if not pushed:
            problems.append("no push timestamp recorded")
        elif first_pitch is not None:
            expect = int((first_pitch - parse_utc(pushed)).total_seconds() // 60)
            if margin == "" or int(margin) != expect:
                problems.append("margin should be %d minutes, CSV says %r"
                                % (expect, margin))
            elif expect <= 0:
                problems.append("pushed %d minutes AFTER first pitch" % -expect)

        if pushed and r["commit_sha"] not in witnessed:
            notes.append("push time is from the snapshot, and this commit is "
                         "not a push head; re-derived from the event range")

        if problems:
            failures += 1
            print("FAIL pick %s (gamePk %s)" % (pick, r["game_pk"]))
            for p in problems:
                print("       %s" % p)
        else:
            print("ok   pick %s  gamePk %s  pushed %s minutes before first "
                  "pitch  (%s)" % (pick, r["game_pk"], margin, r["prediction"]))
        for n in notes:
            print("       note: %s" % n)

    print()
    print("%d rows checked, %d failed" % (len(rows), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
