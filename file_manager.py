
import shutil
import logging

from pathlib import Path

logging.basicConfig(
    filename="file_manager.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def organize_files(folder_path):
    folder = Path(folder_path)
    logging.info(f"Starting organization: {folder}")

    if not folder.exists():
        print("Folder does not exist!")
        return

    if not folder.is_dir():
        print("This path is not a folder!")
        return

    # Chỉ lấy file trực tiếp trong thư mục gốc
    files=[item for item in folder.iterdir() if item.is_file()]

    print("\n===== PREVIEW =====")

    for file in files:
        category = classify_file(file)
        print (f"{file.name} -> {category}")

    confirm = input("\nMove these files? (yes/no): ")

    if confirm.lower() != "yes":
        print("Operation cancelled!")
        return

    for file in files:
        category = classify_file(file)

        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        destination = destination_folder / file.name

        # Không ghi đè file trùng tên
        if destination.exists():
            print(f"Skipped: {file.name} (already exist)")
            logging.warning(f"Dupocate file skipped: {file.name}")
            continue
        try:
            shutil.move(str(file),str(destination))

            print(f"Moved: {file.name} -> {category}")
            logging.info(f"Moved: {file.name} -> {category}")

        except FileNotFoundError:
            print(f"File not found: {file.name}")
            logging.error(f"File not found: {file}")

        except PermissionError:
            print(f"Permisson denied: {file.name}")
            logging.error(f"Permisson denied: {file}")

        except OSError as error:
            print(f"Cannot move {file.name}: {error}")
            logging.exception(f"Failed to move: {file}")


    print("\nOrganization completed!")
    logging.info("Organization completed")


def scan_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist!")
        return

    if not folder.is_dir():
        print("This path is not a folder!")
        return

    files = [item for item in folder.iterdir() if item.is_file()]

    print(f"\nScanning folder: {folder}")
    print(f"Total files: {len(files)}")

    for file in files:
        category = classify_file(file)
        print(f"{file.name} - {file.suffix} - {category}")

    # Thống kê số lượng file theo nhóm
    statistics = count_files(files)

    print("\n===== FILE STATISTICS =====")

    for category, total in statistics.items():
        print(f"{category}: {total}")

def get_file_extension(file_path):
        file = Path(file_path)
        return file.suffix.lower()
    
def classify_file(file_path):
    extension = get_file_extension(file_path)

    categories = {
        "Documents": [".pdf", ".docx", ".txt"],
        "Images": [".jpg", ".jpeg", ".png"],
        "Videos": [".mp4", ".mkv", ".avi"],
        "Spreadsheets": [".xlsx", ".xls", ".csv"]
    }

    for category, extensions in categories.items():
        if extension in extensions:
            return category

    return "Others"

def count_files(files):
    result = {}

    for file in files:
        category = classify_file(file)

        if category not in result:
            result[category] = 0

        result[category] += 1

    return result



if __name__ == "__main__":
    path = input("Enter folder path: ")
    organize_files(path)
