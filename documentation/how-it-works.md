# How the automation works

## Organizer

Importing the module has no side effects. The command-line entry point loads JSON, validates the mode and source directory, normalizes extension mappings, and rejects category names containing traversal, separators, reserved Windows devices, or invalid filename characters.

The organizer snapshots the source directory's immediate children in filename order. It skips directories, symbolic links, detected junctions, and the configured log file itself. The extension selects a category, with `Other` as the fallback. It rejects destination directories that are links or resolve outside the source folder.

Preview computes and prints destinations without creating any directories or activity logs. Apply creates the category folder, opens a new destination exclusively, copies the data, flushes it, copies filesystem metadata, and only then deletes the source. If a destination appears concurrently, it retries with a numbered filename. If copying fails, it removes its partial destination and keeps the source.

Successful moves append a CSV row with timestamp, original filename, extension, source, actual destination, category, and status. A log failure is reported as an error even if the file has already moved; inspect the destination before retrying. Per-file errors do not stop subsequent files, but cause a nonzero exit code.

## Reporting

The report reads the existing CSV format, accepting both the earlier space-separated timestamps and ISO timestamps. It includes only entries within the requested trailing number of days. It counts categories and statuses, skips malformed rows with a visible count, and rejects invalid column headers. Missing logs yield an empty report. Report timestamps use naive local computer time; timezone-aware imported timestamps are treated as malformed.

## Windows integration

The launcher derives the repository root from its own location, invokes the selected Python executable, checks exit codes, and produces a report after success. Explicit preview skips report creation. The scheduler resolves the Python executable at registration time, sets a working directory, avoids overlapping scheduled instances, and supports PowerShell's `-WhatIf` preview.

## Practical limits

- Use one process and a stable input folder. There is no directory-wide lock or protection against hostile filesystem changes during a run.
- Exclusive creation protects an existing destination from overwrite; copy-then-delete is not an atomic rename. A power loss can leave a partial output or duplicate source. Inspect files after an interrupted run.
- Copying requires spare disk space. Metadata preservation depends on the operating system; alternate streams, ACLs and special filesystem objects are not guaranteed.
- An actively edited source can change while being copied. Close editing applications first.
- Links and detected junctions are skipped, but this is not a filesystem security boundary against an adversary replacing paths concurrently.
- Logs and reports are operational outputs and are ignored by Git. Logs are not rotated automatically.
- There is no undo command. To reverse a move, inspect the recorded source/destination and move the file back only after checking for conflicts.
