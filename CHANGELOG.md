# Change log

## Project completion — 2026-11-06

- Removed fixed repository paths from Python and PowerShell entry points.
- Added command-line configuration and one-run preview/apply overrides.
- Made preview read-only and added configuration/destination validation.
- Added exclusive destination creation and source retention on copy failure.
- Preserved CSV compatibility and recorded actual numbered destinations.
- Changed weekly reports from all-time totals to a configurable trailing window.
- Added isolated safety tests and a Windows/Linux CI matrix.
- Improved launcher error propagation and optional scheduler configuration.
- Repaired Markdown and documented setup, verification, limitations and recovery.

New previews no longer log dry-run entries. Existing legacy entries remain supported by the reporting tool. Real moves use copy-then-delete and need additional disk space. Scheduling is not enabled automatically.
