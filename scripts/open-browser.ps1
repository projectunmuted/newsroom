<#
Opens Chrome on demand so the browser does not have to sit open all day.

Why this exists: the Claude extension only talks to a running Chrome, and the
human does not want to leave one open (his call, 2026-08-09). This launches the
detroitsportsreporter profile with a real page, which wakes the extension's
service worker.

    powershell -File scripts/open-browser.ps1
    powershell -File scripts/open-browser.ps1 -Url "https://old.reddit.com/r/detroitlions/about/rules"

PROFILES, verified 2026-08-09 by reading Chrome's Local State:
    Default   -> Stanley          (his personal profile; do not use)
    Profile 6 -> project-unmuted
    Profile 7 -> Work             = detroitsportsreporter, the one to use
The Claude extension is installed in all three at v1.0.85, none disabled.

KNOWN LIMIT: launching Chrome is not the same as the extension being paired.
If `list_connected_browsers` comes back empty after this runs, the extension
needs a manual click on its toolbar icon to reconnect, which is a human action
and lives in ASK-HUMAN.md. Everything else here is automatic.
#>

param(
    [string]$Url = "about:blank",
    [string]$Profile = "Profile 7",
    [int]$WaitSeconds = 8
)

$ErrorActionPreference = 'Stop'

$exe = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $exe) { throw "Chrome not found in any of the usual locations" }

Start-Process $exe -ArgumentList "--profile-directory=$Profile", $Url
Start-Sleep -Seconds $WaitSeconds

$windows = @(Get-Process chrome -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -ne '' })

Write-Output "launched: $exe"
Write-Output "profile:  $Profile"
Write-Output "url:      $Url"
Write-Output "windows:  $($windows.Count)"
