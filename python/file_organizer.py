from pathlib import Path
import csv
from datetime import datetime
import shutil
import json

DRY_RUN = True

TEST_FOLDER = Path(r"C:\Automation-Test")

LOG_FILE = Path(
    r"C:\Real-World-File-Automation\logs\file_activity.csv"
)

CONFIG_FILE = Path(
    r"C:\Real-World-File-Automation\config\file_categories.json"
)

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    FILE_CATEGORIES = json.load(file)


def get_unique_destination(destination):
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1


def log_action(
    filename,
    extension,
    source,
    destination,
    category,
    status
):
    LOG_FILE.parent.mkdir(exist_ok=True)

    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "filename",
                "extension",
                "source",
                "destination",
                "category",
                "status"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename,
            extension,
            source,
            destination,
            category,
            status
        ])


for file_path in TEST_FOLDER.iterdir():
    try:
        if file_path.is_file():

            extension = file_path.suffix.lower()

            category = FILE_CATEGORIES.get(
                extension,
                "Other"
            )

            if category == "Other":
                print(f"Unknown file type: {file_path.name}")

            destination_folder = TEST_FOLDER / category
            destination_folder.mkdir(exist_ok=True)

            destination = destination_folder / file_path.name
            destination = get_unique_destination(destination)

            if DRY_RUN:
                print(f"Would move: {file_path.name} -> {category}")

                log_action(
                    file_path.name,
                    extension,
                    str(file_path),
                    str(destination),
                    category,
                    "Dry Run"
                )

            else:
                shutil.move(
                    str(file_path),
                    str(destination)
                )

                print(f"Moved: {file_path.name} -> {category}")

                log_action(
                    file_path.name,
                    extension,
                    str(file_path),
                    str(destination),
                    category,
                    "Moved"
                )

    except Exception as error:
        print(f"Error processing {file_path.name}: {error}")