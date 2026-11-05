\# Real-World File Automation



A Python and PowerShell automation project that organizes files, records activity, and generates weekly reports.



\## Problem



Manually organizing files is repetitive and time-consuming. Downloads and work folders can quickly become cluttered with documents, spreadsheets, images, archives, and other files.



\## Solution



This project automates file organization by:



\- Detecting file types

\- Moving files into category folders

\- Handling duplicate filenames safely

\- Supporting dry-run testing

\- Logging file activity

\- Generating weekly reports

\- Launching through PowerShell

\- Supporting scheduled execution with Windows Task Scheduler



\## Technologies



\- Python

\- PowerShell

\- JSON

\- CSV

\- Git

\- GitHub

\- Windows Task Scheduler

\- Microsoft Copilot



\## Project Structure



```text

Real-World-File-Automation/

├── config/

│   ├── file\_categories.json

│   └── settings.json

├── documentation/

├── logs/

├── powershell/

│   ├── run\_organizer.ps1

│   └── setup\_task.ps1

├── python/

│   ├── file\_organizer.py

│   └── weekly\_report.py

├── reports/

├── screenshots/

├── README.md

└── requirements.txt

