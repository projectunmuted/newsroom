<#
Registers the hourly git sync so this PC and GitHub stay in step between cycles.

    powershell -File setup-sync-task.ps1

Separate task from 'Dollar Experiment Cycle' on purpose. That one runs a model
twice a day and costs tokens; this one is pure git, costs nothing, and should
run often. Keeping them apart means a wedged cycle cannot stop the syncing, and
sync noise cannot be mistaken for cycle activity.

REGISTERED 2026-08-10, but not by this script. `Register-ScheduledTask` returned
Access Denied on this machine for creating a new task, while modifying an
existing one worked fine. `schtasks.exe` created it without elevation:

    $cmd = '\"powershell.exe\" -NoProfile -NonInteractive -ExecutionPolicy Bypass -File \"C:\Users\stanl\Project Folder\Claude_Experiment\scripts\sync-repo.ps1\" -Quiet'
    schtasks.exe /Create /TN "Dollar Experiment Sync" /TR $cmd /SC HOURLY /F

then StartWhenAvailable was set with Set-ScheduledTask afterwards, which is
allowed. Note the backslash-escaped quotes: schtasks needs them and fails with
"Invalid argument/option" without them.

The at-logon trigger this script asks for also needs elevation and is NOT
registered. Hourly plus StartWhenAvailable covers the same ground a few minutes
slower: a laptop that slept through a cycle catches up at the next tick after
waking. If it is ever wanted properly, run this script from an elevated
PowerShell.

Remove it with:
    Unregister-ScheduledTask -TaskName 'Dollar Experiment Sync' -Confirm:$false
#>

$ErrorActionPreference = 'Stop'

$TaskName = 'Dollar Experiment Sync'
$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$Script = Join-Path $Repo 'scripts\sync-repo.ps1'

if (-not (Test-Path $Script)) { throw "sync-repo.ps1 not found at $Script" }

$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Script`" -Quiet" `
    -WorkingDirectory $Repo

# Hourly, starting five minutes from now, forever. Also at logon, so opening
# the laptop after it slept through a cycle pulls that cycle's work down before
# he looks at the folder.
$hourly = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) `
    -RepetitionInterval (New-TimeSpan -Hours 1)
$atLogon = New-ScheduledTaskTrigger -AtLogOn
$trigger = [Microsoft.Management.Infrastructure.CimInstance[]]@($hourly, $atLogon)

# Deliberately no WakeToRun: this is not worth waking a sleeping machine for.
# It catches up at the next hourly tick or at logon.
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -MultipleInstances IgnoreNew

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive -RunLevel Limited

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Output "removed existing task"
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal `
    -Description 'Keeps the newsroom repo and the DSR deploy clone in step with GitHub. Pure git, no model, no cost.' | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
$i = $t | Get-ScheduledTaskInfo
Write-Output "registered '$TaskName'"
Write-Output "  state:    $($t.State)"
Write-Output "  next run: $($i.NextRunTime)"
Write-Output "  when:     every hour, and at logon"
Write-Output "  log:      logs\sync.log"
