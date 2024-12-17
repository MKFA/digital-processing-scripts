import os
from pathlib import Path
import shutil

def main():
    AIP_dir = Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/AIPs/magnetic_media")
    for aip in os.listdir(AIP_dir):
        if aip == ".DS_Store":
            continue
        for root, dirs, files in os.walk(os.path.join(AIP_dir, aip)):
            for file in files:
                if file.startswith("filestoreview"):
                    file_path = os.path.join(root, file)
                    shutil.move(file_path, f"/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/deletion_staging/{aip}_{file}")
                    print(f"{file} removed from {aip}")


main()