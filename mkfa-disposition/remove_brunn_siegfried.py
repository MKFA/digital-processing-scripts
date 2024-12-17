import os
from pathlib import Path
import shutil

def main():
    AIP_dir = Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/AIPs/hard_drives")
    for aip in os.listdir(AIP_dir):
        if aip == ".DS_Store":
            continue
        relative_siegfried = AIP_dir / aip / "reports" / f"{aip}_siegfried.csv"
        brunn_siegfried = AIP_dir / aip / "reports" / f"{aip}_brunn_reports" / "siegfried.csv"

        if brunn_siegfried.exists():

            with open(brunn_siegfried, "r") as file:
                siegfried_line_count = 0
                for line in file:
                    siegfried_line_count += 1

            with open(relative_siegfried, "r") as file:
                other_line_count = 0
                for line in file:
                    other_line_count += 1
            
            if siegfried_line_count == other_line_count:
                shutil.move(brunn_siegfried, f"/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/deletion_staging/{aip}_brunn_siegfried.csv")
                print(f"Removed {brunn_siegfried}")
            else: 
                print(f"Line counts do not match for {aip}")

main()
    

