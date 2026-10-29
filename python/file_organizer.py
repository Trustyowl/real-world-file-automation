from pathlib import Path
import csv
from collections import Counter

LOG_FILE = Path(
    r"C:\Real-World-File-Automation\logs\file_activity.csv"
)

REPORT_FILE = Path(
    r"C:\Real-World-File-Automation\reports\weekly_report.txt"
)

category_counts = Counter()
status_counts = Counter()
total_files = 0

with open(LOG_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_files += 1
        category_counts[row["category"]] += 1
        status_counts[row["status"]] += 1

REPORT_FILE.parent.mkdir(exist_ok=True)

with open(REPORT_FILE, "w", encoding="utf-8") as report:
    report.write("WEEKLY FILE ORGANIZATION REPORT\n")
    report.write("=" * 32 + "\n\n")

    report.write(f"Total files processed: {total_files}\n\n")

    report.write("Files by category:\n")
    for category, count in category_counts.items():
        report.write(f"- {category}: {count}\n")

    report.write("\nStatus summary:\n")
    for status, count in status_counts.items():
        report.write(f"- {status}: {count}\n")

print("Weekly report created successfully.")