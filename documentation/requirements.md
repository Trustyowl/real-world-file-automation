# Requirements and acceptance criteria

## Runtime

- Python 3.10 or newer; standard library only.
- Windows PowerShell 5.1+ for `.ps1` scripts.
- Windows Task Scheduler for optional recurring execution.
- Read/delete access to the chosen input files and write access to category directories and the chosen log/report locations.
- Available disk space for a copy of each file during its move.

The Python components are designed for Windows and Linux. CI is configured for Python 3.10, 3.12 and 3.13 on both platforms; a local test run does not establish that the remote CI matrix has passed.

## Functional acceptance criteria

| Requirement | Verification |
| --- | --- |
| Settings select source folder and mode | Configuration tests and CLI override test |
| Categories match extensions case-insensitively | Configuration normalization and uppercase extension test |
| Unknown extensions use Other | Organizer real-move test |
| Existing names retain their content | Collision and exclusive-creation race tests |
| Preview causes no writes | Snapshot-based preview test |
| Failed copy retains original | Simulated disk failure test |
| Errors do not stop unrelated files | Blocked category test |
| Nested files are not scanned | Nested directory test |
| Unsafe destinations fail | Category validation and destination link test |
| Actual moves are logged | CSV destination assertions |
| Weekly report excludes old/future rows | Fixed-time report boundary test |
| Missing logs are handled | Empty report test |
| Launcher and scheduling are optional | Explicit setup commands and WhatIf support |

## Verification command

```powershell
python -m unittest discover -s tests -v
```

Tests use temporary directories. They do not organize personal folders or register scheduled tasks. Actual scheduler registration requires an explicit operator action and appropriate account permissions.
