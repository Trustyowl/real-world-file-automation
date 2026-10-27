from pathlib import Path
import shutil
DRY_RUN = True

TEST_FOLDER = Path(r"C:\Automation-Test")

FILE_CATEGORIES = {
    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".xlsx": "Spreadsheets",
    ".csv": "Spreadsheets",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".zip": "Archives",
    ".mp4": "Videos",
    ".mp3": "Audio",
    ".exe": "Applications"
}

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

for file_path in TEST_FOLDER.iterdir():
    try:
        if file_path.is_file():

            extension = file_path.suffix.lower()
            category = FILE_CATEGORIES.get(extension, "Other")

            if category == "Other":
                print(f"Unknown file type: {file_path.name}")

            destination_folder = TEST_FOLDER / category
            destination_folder.mkdir(exist_ok=True)

            destination = destination_folder / file_path.name
            destination = get_unique_destination(destination)

            if DRY_RUN:
                print(f"Would move: {file_path.name} -> {category}")
            else:
                shutil.move(str(file_path), str(destination))
                print(f"Moved: {file_path.name} -> {category}")

    except Exception as error:
        print(f"Error processing {file_path.name}: {error}")