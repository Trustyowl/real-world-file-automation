$TaskName = "RealWorldFileAutomation"

$ProjectPath = "C:\Real-World-File-Automation"

$PowerShellScript = Join-Path `
    $ProjectPath `
    "powershell\run_organizer.ps1"

$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File `"$PowerShellScript`""

$Trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Friday `
    -At 6:00PM

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Description "Runs the file organizer and weekly report every Friday."