\# How the Automation Works



\## Overview



This project automates repetitive file organization using Python and PowerShell.



The automation scans a selected folder, determines each file's type, assigns it to a category, records the activity, and generates a summary report.



\## Workflow



1\. PowerShell launches the automation.

2\. Python reads automation settings from JSON configuration files.

3\. The organizer scans the configured folder.

4\. Each file extension is checked against the category configuration.

5\. Known files are assigned to categories such as Documents, Images, or Spreadsheets.

6\. Unknown files are assigned to the Other category.

7\. Duplicate filename protection prevents existing files from being overwritten.

8\. Dry-run mode can preview actions without moving files.

9\. Each processed file is written to the activity log.

10\. The weekly report script reads the activity log.

11\. A summary report is generated showing file categories and processing results.

12\. Windows Task Scheduler can be used to run the process automatically.



\## Main Components



\### file\_organizer.py



Responsible for:



\- Scanning files

\- Detecting extensions

\- Choosing categories

\- Creating destination folders

\- Handling duplicate filenames

\- Moving files

\- Logging actions

\- Handling errors



\### weekly\_report.py



Responsible for:



\- Reading the activity log

\- Counting processed files

\- Summarizing file categories

\- Summarizing successful moves and dry runs

\- Identifying the most common category

\- Creating the weekly report



\### run\_organizer.ps1



Runs the Python automation and report generator from PowerShell.



\### setup\_task.ps1



Provides a Windows Task Scheduler configuration for automatically running the automation every Friday.



\## Safety Features



The project includes:



\- Dry-run mode

\- Duplicate filename protection

\- Separate test environment

\- Error handling

\- Activity logging



These features allow the automation to be tested safely before using it on real files.

