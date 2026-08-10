<#
Keeps this PC and GitHub in step so either one can be trusted when checking on
the project.

Why this exists (his requirement, 2026-08-10): he monitors from GitHub when he
is away and from the folder when he is at the machine, and those two only agree
if something keeps them agreeing. `run-cycle.ps1` already pulls before a cycle
and pushes after, but cycles are now twelve hours apart, so between them the
local folder can sit stale while GitHub moves, or a commit can sit local while
GitHub sits behind.

This is pure git. No model, no tokens, safe to run often. Registered hourly by
setup-sync-task.ps1.

What it does, in order, for the newsroom repo and the detroitsportsreporter
deploy clone beside it:

  1. fetch
  2. if the local branch is behind and clean, fast-forward
  3. if the local branch is ahead, push
  4. if the two have diverged, report and STOP. A merge is a judgment call and
     this script does not make judgment calls unattended.
  5. report uncommitted changes rather than committing them. Committing on a
     schedule would put half-finished work into the record, and the record is
     the product.

    powershell -File scripts/sync-repo.ps1
    powershell -File scripts/sync-repo.ps1 -Quiet    # only prints problems
#>

param(
    [switch]$Quiet
)

$ErrorActionPreference = 'Continue'

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Deploy = Join-Path (Split-Path -Parent $Repo) 'detroitsportsreporter'
$LogDir = Join-Path $Repo 'logs'
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$Log = Join-Path $LogDir 'sync.log'

$script:problems = 0

function Say($msg, [switch]$Problem) {
    $line = "[{0}] {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg
    Add-Content -Path $Log -Value $line -Encoding utf8
    if ($Problem) { $script:problems++ }
    if ($Problem -or -not $Quiet) { Write-Output $line }
}

function Sync-One($path, $name) {
    if (-not (Test-Path (Join-Path $path '.git'))) {
        Say "$name : not a git repo at $path" -Problem
        return
    }
    Push-Location $path
    try {
        git fetch --quiet origin 2>$null
        $branch = (git rev-parse --abbrev-ref HEAD).Trim()
        $dirty = @(git status --porcelain)
        $counts = (git rev-list --left-right --count "HEAD...origin/$branch" 2>$null)
        if (-not $counts) {
            Say "$name : no upstream for $branch" -Problem
            return
        }
        $ahead, $behind = $counts -split '\s+'
        $ahead = [int]$ahead; $behind = [int]$behind

        if ($ahead -eq 0 -and $behind -eq 0) {
            Say "$name : in sync at $(git rev-parse --short HEAD)"
        }
        elseif ($ahead -gt 0 -and $behind -gt 0) {
            Say "$name : DIVERGED, $ahead local and $behind remote commits. Not merging unattended; resolve by hand." -Problem
        }
        elseif ($behind -gt 0) {
            if ($dirty.Count -gt 0) {
                Say "$name : $behind behind but working tree is dirty; not touching it." -Problem
            } else {
                git pull --quiet --ff-only origin $branch 2>$null
                if ($LASTEXITCODE -eq 0) {
                    Say "$name : pulled $behind, now at $(git rev-parse --short HEAD)"
                } else {
                    Say "$name : fast-forward failed" -Problem
                }
            }
        }
        else {
            git push --quiet origin $branch 2>$null
            if ($LASTEXITCODE -eq 0) {
                Say "$name : pushed $ahead, now at $(git rev-parse --short HEAD)"
            } else {
                Say "$name : push of $ahead commits FAILED" -Problem
            }
        }

        if ($dirty.Count -gt 0) {
            Say "$name : $($dirty.Count) uncommitted file(s), left alone" -Problem
        }
    }
    finally { Pop-Location }
}

Sync-One $Repo 'newsroom'
if (Test-Path $Deploy) { Sync-One $Deploy 'detroitsportsreporter' }

if ($script:problems -gt 0) {
    Say "sync finished with $($script:problems) thing(s) needing attention" -Problem
    exit 1
}
Say "sync clean"
exit 0
