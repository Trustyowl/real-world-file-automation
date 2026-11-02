\# Microsoft Copilot Usage



\## Overview



Microsoft Copilot was used as a development assistant while building this real-world automation project.



I used AI to help explain unfamiliar Python and PowerShell concepts, explore different approaches to problems, troubleshoot errors, and review possible improvements. I tested and reviewed suggestions before adding them to the project.



\## How Copilot Helped



\### File Organization



I used Copilot to better understand Python file-management tools such as pathlib and shutil.



The final automation identifies file extensions and determines which folder each file belongs in.



\### Duplicate Filename Protection



Problem:

A file could already exist in the destination folder with the same name.



Copilot helped me explore ways to prevent existing files from being overwritten.



Solution:

The program checks whether the destination filename already exists and generates a numbered filename when necessary.



Example:



report.pdf



report\_1.pdf



report\_2.pdf



\### Dry-Run Mode



Problem:

Automatically moving files while testing could accidentally change files I wanted to keep.



Copilot helped me understand how to create a dry-run mode.



Solution:

The program can display what it would move without actually moving the files.



Example:



Would move: new\_report.pdf -> Documents



\### Error Handling



Problem:

One unexpected file or error could stop the automation.



I used AI assistance to understand Python try/except error handling.



Solution:

Each file is processed safely so an error with one file does not stop the entire automation.



\### Activity Logging



I used AI assistance while designing a CSV log that records:



\- Timestamp

\- Filename

\- File extension

\- Source

\- Destination

\- Category

\- Status



This log is then used by the weekly report generator.



\### Debugging



During development, the file organizer script was accidentally replaced with weekly report code.



I identified the problem by reviewing the script contents and testing each component separately.



The organizer and weekly report were then separated into their correct Python files and tested individually.



\## Validation



AI-generated suggestions were not automatically accepted.



I reviewed the code, ran it in a test environment, checked the output, and corrected problems before considering a feature complete.



\## What I Learned



Using Copilot effectively still requires understanding the problem, testing the proposed solution, recognizing errors, and deciding whether a suggestion is appropriate.



AI helped speed up development, but testing and final implementation decisions remained part of my development process.

