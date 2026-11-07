# Usage guide

## Configure

Create a dedicated folder, for example `C:\Automation-Test`. Set `config/settings.json`:

```json
{
  "dry_run": true,
  "test_folder": "C:\\Automation-Test"
}
```

The example file can be copied for a new installation. Relative input folders resolve against the settings file's directory. The source directory must already exist. `dry_run` must be the JSON boolean `true` or `false`, not a quoted string.

Edit `config/file_categories.json` to map dotted extensions to single folder names. `.PDF` and `.pdf` match identically; duplicate normalized keys are rejected. Unknown extensions and files without extensions go to `Other`.

## Preview and apply

From the repository root:

```powershell
python .\python\file_organizer.py --dry-run
python .\python\file_organizer.py --apply
```

The flags override saved mode for one run. Without a flag, the saved `dry_run` value applies. The flags cannot be combined. Preview does not write anything. Subdirectories and links are skipped.

Custom input configuration and output log:

```powershell
python .\python\file_organizer.py --settings C:\Demo\settings.json --categories .\config\file_categories.json --log C:\Demo\activity.csv --dry-run
```

For conflicting names, `report.pdf` becomes `report_1.pdf`, then `report_2.pdf`. Check the printed full destination or activity log to see the actual filename.

## Reports

```powershell
python .\python\weekly_report.py
python .\python\weekly_report.py --days 30 --log .\logs\file_activity.csv --output .\reports\monthly.txt
```

The default window is the previous seven days through the current local time, inclusive. Missing logs produce an empty report. Invalid headers fail; malformed rows are counted and skipped. Old and future entries are excluded. Legacy dry-run log entries are counted separately; new previews do not log.

## PowerShell launcher

```powershell
.\powershell\run_organizer.ps1 -DryRun
.\powershell\run_organizer.ps1 -Apply
.\powershell\run_organizer.ps1 -Python 'C:\Path To Python\python.exe' -DryRun
```

Explicit `-DryRun` skips the report so the entire launcher preview is read-only. With no mode flag, the saved configuration applies and a report is generated afterward. A failed organizer prevents report generation and propagates its exit code.

## Optional weekly task

```powershell
.\powershell\setup_task.ps1 -Python python -WhatIf
.\powershell\setup_task.ps1 -Python python
Get-ScheduledTask -TaskName RealWorldFileAutomation
Unregister-ScheduledTask -TaskName RealWorldFileAutomation
```

The default is Friday at 6 PM in the computer's local time. Use `-Day Monday -At '09:00'` to customize it. The task uses saved settings and does not force real moves. Keep `dry_run: true` until you intentionally want recurring real organization. Registration does not overwrite an existing task. The default task principal is the registering user; check Task Scheduler's login and permission requirements before relying on unattended execution. Setup does not install Python or change execution policy.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Successful run, including an empty input folder |
| 1 | Organizer processed the folder but one or more file operations failed |
| 2 | Invalid arguments, configuration, inaccessible input, or report failure |

Run `python -m unittest discover -s tests -v` before publishing changes. Tests create their own temporary files and do not require your configured folder.
