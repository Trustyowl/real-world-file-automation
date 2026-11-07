[CmdletBinding()]
param(
    [string]$Python = 'python',
    [switch]$Apply,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
if ($Apply -and $DryRun) { throw 'Choose either -Apply or -DryRun.' }
$ProjectPath = Split-Path -Parent $PSScriptRoot
$Organizer = Join-Path $ProjectPath 'python\file_organizer.py'
$Report = Join-Path $ProjectPath 'python\weekly_report.py'
$ModeArgs = @()
if ($Apply) { $ModeArgs = @('--apply') }
if ($DryRun) { $ModeArgs = @('--dry-run') }
& $Python $Organizer @ModeArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if ($DryRun) {
    Write-Host 'Preview complete. No report written.'
    exit 0
}
& $Python $Report
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Automation complete.'
