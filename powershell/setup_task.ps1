[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$TaskName = 'RealWorldFileAutomation',
    [string]$Python = 'python',
    [ValidateSet('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')]
    [string]$Day = 'Friday',
    [datetime]$At = '18:00'
)
$ErrorActionPreference = 'Stop'
$ProjectPath = Split-Path -Parent $PSScriptRoot
$Script = Join-Path $PSScriptRoot 'run_organizer.ps1'
$PythonPath = (Get-Command $Python -CommandType Application -ErrorAction Stop).Source
if ($Script.Contains('"') -or $PythonPath.Contains('"')) { throw 'Paths must not contain quotes.' }
$Arguments = "-NoProfile -NonInteractive -File `"$Script`" -Python `"$PythonPath`""
$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $Arguments -WorkingDirectory $ProjectPath
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Day -At $At
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew
if ($PSCmdlet.ShouldProcess($TaskName, 'Register weekly file organizer task')) {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings `
        -Description 'Organizes the configured folder and creates a seven-day activity report.'
}
