<#
Registers (or re-registers) the Windows Scheduled Task that runs one cycle of
the Dollar Experiment twice a day, at 2:00am and 10:00am local time.

    powershell -File setup-cycle-task.ps1

Deliberate choices:

- LogonType Interactive: runs only while the human is logged on. "Run whether user is
  logged on or not" needs a stored password, which I can't enter and wouldn't
  want stored anyway. A locked screen is still logged on, so this is compatible
  with waking from sleep.
- WakeToRun: wakes the machine to run the cycle (the human asked for this on
  2026-08-07). Two caveats worth knowing — it only wakes from *sleep*, never
  from full shutdown or hibernation, and Windows ignores wake timers when the
  power plan disables them, which is the default on battery for many laptops.
  See the note this script prints after registering.
- StartWhenAvailable: if the PC was off at fire time, run once at the next
  opportunity rather than silently skipping until the following window.
- ExecutionTimeLimit 1 hour: a wedged cycle gets killed rather than blocking
  every later one.

Remove it with:
    Unregister-ScheduledTask -TaskName 'Dollar Experiment Cycle' -Confirm:$false
#>

$ErrorActionPreference = 'Stop'

$TaskName = 'Dollar Experiment Cycle'
$Repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$Script = Join-Path $Repo 'run-cycle.ps1'

if (-not (Test-Path $Script)) { throw "run-cycle.ps1 not found next to this script ($Script)" }

$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$Script`"" `
    -WorkingDirectory $Repo

# Twice a day at fixed clock times, his call 2026-08-10, replacing an interval
# that drifted with whenever the task was last registered.
#
#   02:00 ET - after every game on the continent has finished, so grading has
#              real box scores rather than a game still in progress.
#   10:00 ET - hours before first pitch or kickoff, so a pick lands before the
#              game and a post has the whole day to breathe.
#
# Two is deliberately fewer than the old three. Three cycles a day produced
# three pieces about one team in a day, and the fix was fewer, better cycles.
# Adjust ad hoc when the calendar demands it, an early international kickoff
# being the obvious case: add a one-off trigger, do not reshape the daily two.
$morning = New-ScheduledTaskTrigger -Daily -At 2:00AM
$midday = New-ScheduledTaskTrigger -Daily -At 10:00AM
$trigger = [Microsoft.Management.Infrastructure.CimInstance[]]@($morning, $midday)

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -WakeToRun `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -MultipleInstances IgnoreNew

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Output "removed existing task"
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal `
    -Description 'Runs one autonomous cycle of the Dollar Experiment (see CYCLE.md). 2:00am and 10:00am daily, while logged on.' | Out-Null

$t = Get-ScheduledTask -TaskName $TaskName
$i = $t | Get-ScheduledTaskInfo
Write-Output "registered '$TaskName'"
Write-Output "  state:    $($t.State)"
Write-Output "  next run: $($i.NextRunTime)"
Write-Output "  when:     2:00am and 10:00am daily, wakes the machine from sleep"
Write-Output ""

# WakeToRun is only honoured if the active power plan allows wake timers. Report
# the truth rather than letting a silently-ignored setting look like it worked.
foreach ($ctx in @('AC', 'DC')) {
    $q = powercfg /query SCHEME_CURRENT SUB_SLEEP RTCWAKE 2>$null
    if (-not $q) { break }
}
$wake = powercfg /query SCHEME_CURRENT SUB_SLEEP RTCWAKE 2>$null
if ($wake) {
    $ac = ($wake | Select-String 'Current AC Power Setting Index:\s*(0x[0-9a-f]+)').Matches.Groups[1].Value
    $dc = ($wake | Select-String 'Current DC Power Setting Index:\s*(0x[0-9a-f]+)').Matches.Groups[1].Value
    $name = @{ '0x00000000' = 'Disabled'; '0x00000001' = 'Enabled'; '0x00000002' = 'Important events only' }
    Write-Output "Wake timers - plugged in: $($name[$ac]); on battery: $($name[$dc])"
    if ($ac -eq '0x00000000') {
        Write-Output "  WARNING: wake timers are DISABLED while plugged in, so the task will"
        Write-Output "  NOT wake this machine. Enable with:"
        Write-Output "    powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP RTCWAKE 1"
        Write-Output "    powercfg /setactive SCHEME_CURRENT"
    }
}
Write-Output ""
Write-Output "Note: waking works from sleep only - never from shutdown or hibernation."
