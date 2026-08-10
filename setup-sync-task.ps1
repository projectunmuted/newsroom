<#
Registers the hourly git sync so this PC and GitHub stay in step between cycles.

    powershell -File setup-sync-task.ps1

Separate task from 'Dollar Experiment Cycle' on purpose. That one runs a model
twice a day and costs tokens; this one is pure git, costs nothing, and should
run often. Keeping them apart means a wedged cycle cannot stop the syncing, and
sync noise cannot be mistaken for cycle activity.

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
