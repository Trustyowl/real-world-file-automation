# Troubleshooting

## Python is not found or the Store alias opens

Use `python --version` to check the executable. Install Python if needed, or provide a known executable path with the launcher's `-Python` argument. For direct PowerShell execution of a quoted path, use `& 'C:\Path To Python\python.exe' .\python\file_organizer.py --dry-run`.

## Configuration error

Check JSON commas, quotes, and escaped Windows backslashes. Use a real boolean for `dry_run`. Create the input directory before running. Category values must be one valid folder name, such as `Documents`; `../Documents`, nested paths and Windows device names are rejected. Relative input paths start from the settings file's directory.

## Preview did not create folders or a log

This is expected. Preview prints planned actions and does not write. Use `--apply` for one real run while keeping saved settings in dry-run mode. If no source files are listed, the folder may already be organized; existing category directories are not scanned recursively.

## File could not move

Close applications using it and check permissions and free space. A category name may already be occupied by a file, or a destination directory may be a link. The organizer continues with other files and returns code 1. Inspect the error and source/destination before retrying. Do not delete a category's existing files to resolve a conflict.

## File moved but logging failed

The file may already be in its printed destination. Check that location before rerunning. Correct permissions on the log directory or pass a writable `--log` path. The log is an audit aid, not a transaction journal or backup.

## Report count is lower than expected

The default report includes only the last seven days, using local computer time. Older and future timestamps are excluded. Malformed rows are counted and skipped. Use `--days 30` for a longer window. New previews do not append rows; only older logs contain dry-run entries.

## Scheduled task fails

Run the launcher manually with the same Python path and user account. Check Task Scheduler history, logon requirements, permissions, and the saved settings. Use `setup_task.ps1 -WhatIf` to preview registration. Existing tasks are not replaced automatically; inspect them before removal or deliberate re-registration. This project does not bypass system execution policy.
