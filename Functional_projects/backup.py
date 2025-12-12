import os
import shutil
import datetime
import schedule
import time

source_directory = "C:\\Users\\kevin\\Documents\\Tech_with_Tim\\Functional_projects\\source_directory"
destination_directory = "C:\\Users\\kevin\\Documents\\Tech_with_Tim\\Functional_projects\\backup_directory"


def copy_folder_to_directory(src, dest):
    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))

    try:
        shutil.copytree(src, dest_dir)
        print(f"Backup of {src} completed successfully to {dest_dir}")
    except FileExistsError:
        print(f"Backup for today already exists at {dest_dir}.")


schedule.every().month.at("10:00").do(lambda: copy_folder_to_directory(
    src=source_directory, dest=destination_directory))

while True:
    schedule.run_pending()
    time.sleep(60)
# Note: To stop the script, you will need to manually terminate it (e.g., Ctrl+C in the terminal).
