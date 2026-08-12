<#
Runs one cycle of the Dollar Experiment locally.

Why this exists: the claude.ai cloud routine does the work but its commits only
seem to reach GitHub via a sync on this machine — a cycle that runs at 3am with
the laptop off doesn't land. Locally there is no such gap: this is the same
`claude` binary, in the real repo, with real push credentials.

The trade is that cycles only run when this PC is on. That is fine. The failure
mode of this project has always been not shipping, never cycle frequency.

Registered as a Scheduled Task by setup-cycle-task.ps1. Run it by hand any time:
    powershell -File run-cycle.ps1

PERMISSIONS: this runs unattended, so it uses -dangerously-skip-permissions --
an interactive permission prompt with nobody watching is just a hung job. The
blast radius is bounded by the fact that it starts in this repo and its brief
(CYCLE.md) says never to spend money. To tighten it, set $SkipPermissions to
$false below; cycles will then be limited to .claude/settings.json's allowlist
and will fail (not hang) on anything outside it.
#>

param(
    # Exercise the sync, logging and push-check plumbing without spending a
    # cycle. Everything runs except the call to claude.
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$SkipPermissions = $true

$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogDir = Join-Path $Repo 'logs'
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }

$Stamp = Get-Date -Format 'yyyy-MM-dd_HHmmss'
$Log = Join-Path $LogDir "cycle-$Stamp.log"

function Write-Log($msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $msg
    Write-Output $line
    Add-Content -Path $Log -Value $line -Encoding utf8
}

Set-Location $Repo
Write-Log "cycle start in $Repo"

# Start from the current remote state. A cycle that edits a stale tree will
# collide on push and waste itself resolving the conflict.
try {
    git fetch --quiet origin
    git pull --quiet --ff-only origin main
    Write-Log "synced to $(git rev-parse --short HEAD)"
} catch {
    Write-Log "WARNING: could not fast-forward ($_). Working tree may have local changes; continuing anyway."
}

$Prompt = @'
Run one cycle of the Dollar Experiment. Read CYCLE.md in the repo root first and
follow it exactly - it is the complete brief and assumes you have no memory of
previous cycles. Then read README.md, ASK-HUMAN.md, LOG.md, BETS.md and MONEY.md,
pick the single thing that most advances the goal of earning one dollar, do it,
log it honestly including anything that failed, and commit and push to main. Do
not end the cycle having only queued work for a human, and never spend money.
'@

$claudeArgs = @('-p', $Prompt)
if ($SkipPermissions) { $claudeArgs += '--dangerously-skip-permissions' }

$Before = git rev-parse HEAD

if ($DryRun) {
    Write-Log "DRY RUN - skipping claude. Would run: claude -p <CYCLE.md brief>$(if ($SkipPermissions) { ' --dangerously-skip-permissions' })"
    $code = 0
} else {
    Write-Log "running claude (skip-permissions=$SkipPermissions)"
    # `2>&1` on a native command wraps every stderr line in an ErrorRecord, and
    # with $ErrorActionPreference = 'Stop' the first one kills the script. That
    # is how a cycle died one second in on 2026-08-12: claude printed a harmless
    # workspace-trust warning to stderr and PowerShell treated it as fatal. The
    # whole point of capturing stderr is to keep the warnings, so drop the
    # preference to Continue for exactly this call instead of the redirect.
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & claude @claudeArgs 2>&1 | ForEach-Object {
            Add-Content -Path $Log -Value $_ -Encoding utf8
            Write-Output $_
        }
        $code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }
}

$After = git rev-parse HEAD
Write-Log "claude exited $code"

# The only outcome that counts. CYCLE.md says an unpushed cycle did not happen,
# so check rather than assume.
if ($After -ne $Before) {
    git push --quiet origin main 2>&1 | Out-Null
    git fetch --quiet origin 2>&1 | Out-Null
    $remote = git rev-parse --short 'origin/main'
    $local = git rev-parse --short HEAD

    # A push usually fails for one reason: the remote moved while the cycle was
    # running. Rebase onto it and try once more rather than leaving the work
    # stranded until someone notices. Only once: a second failure means
    # something that needs a human, and retry loops hide that.
    if ($remote -ne $local) {
        Write-Log "push rejected, remote is $remote - rebasing and retrying once"
        git pull --quiet --rebase origin main 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            git push --quiet origin main 2>&1 | Out-Null
            git fetch --quiet origin 2>&1 | Out-Null
            $remote = git rev-parse --short 'origin/main'
            $local = git rev-parse --short HEAD
        } else {
            git rebase --abort 2>&1 | Out-Null
            Write-Log "rebase failed and was aborted; leaving the tree as the cycle left it"
        }
    }

    if ($remote -eq $local) {
        Write-Log "PUSHED $local"
    } else {
        Write-Log "COMMITTED $local BUT REMOTE IS $remote - push did not land"
    }
} else {
    Write-Log "no new commit this cycle"
}

# Leave the machine and GitHub agreeing regardless of what happened above, so
# that whichever one he looks at tells the same story. His requirement,
# 2026-08-10.
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Repo 'scripts\sync-repo.ps1') -Quiet 2>&1 |
    ForEach-Object { Write-Log "sync: $_" }

Write-Log "cycle end"
