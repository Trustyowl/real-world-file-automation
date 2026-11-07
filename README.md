# Real-World File Automation

A Python and PowerShell tool that organizes a folder by extension, protects existing filenames, records successful moves, and produces a seven-day activity report.

## Quick start

Requires Python 3.10+; no third-party Python packages. Windows PowerShell 5.1+ is needed only for the Windows launcher and scheduler.

1. Clone the repository and create a dedicated test folder.
2. Edit `config/settings.json` so `test_folder` points to that folder. Keep `dry_run` set to `true`.
3. Run a preview from the repository:

```powershell
python .\python\file_organizer.py --dry-run
```

4. Review the printed destinations, then explicitly apply:

```powershell
python .\python\file_organizer.py --apply
python .\python\weekly_report.py
```

`--apply` does not change saved settings. A preview writes no folders, logs, or reports. Successful real moves are recorded in `logs/file_activity.csv`; the report is written to `reports/weekly_report.txt`.

## Features

- JSON extension mappings; case-insensitive matching and an `Other` fallback.
- Processes only immediate child files, leaving nested directories alone.
- Duplicate names receive `_1`, `_2`, etc.; exclusive output creation prevents overwriting a file that appears between the check and copy.
- Rejects unsafe category names and skips symbolic links and detected Windows junctions.
- Reports errors per file and returns a failing exit code when any file fails.
- Seven-day reports distinguish successful moves from preview entries in older logs.
- PowerShell launcher works from any current directory; optional weekly scheduling supports `-WhatIf`.
- Automated tests run in temporary folders and in a Windows/Linux CI matrix.

## Verify

```powershell
python -m unittest discover -s tests -v
```

## Structure

```text
config/                  Settings and extension mappings
python/file_organizer.py  Organizer and command-line interface
python/weekly_report.py   Activity report generator
powershell/              Windows launcher and optional task registration
tests/                   Isolated behavior and safety tests
documentation/           Usage, architecture, requirements, troubleshooting
```

## Documentation

- [Usage and scheduling](documentation/usage-guide.md)
- [How it works and limitations](documentation/how-it-works.md)
- [Requirements and acceptance criteria](documentation/requirements.md)
- [Troubleshooting](documentation/troubleshooting.md)
- [Project completion checklist](documentation/project-plan.md)
- [Change log](CHANGELOG.md)
- [AI assistance](documentation/copilot-usage.md)

This is a portfolio project, not a backup system. Use a dedicated folder, inspect the preview, and keep backups of valuable files. Run one organizer at a time against files that are not being edited. Moves use copy-then-delete, so they temporarily need additional disk space and are not crash-atomic.
