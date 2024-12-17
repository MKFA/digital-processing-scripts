import os
from pathlib import Path
import shutil

def main():
    AIP_dir = Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/AIPs/hard_drives")
    for aip in os.listdir(AIP_dir):
        if aip == ".DS_Store":
            continue
        deaccession_csv = AIP_dir / aip / "reports" / "appraisal" / f"{aip}_deaccessions.csv"
        new_deaccession_csv = AIP_dir / aip / "reports" / "appraisal" / f"{aip}_deaccessions_adjusted.csv"


        if deaccession_csv.exists():

            with open(deaccession_csv, "r") as file:
                siegfried_line_count = 0
                for line in file:
                    siegfried_line_count += 1

            with open(new_deaccession_csv, "r") as file:
                other_line_count = 0
                for line in file:
                    other_line_count += 1
            
            if siegfried_line_count == other_line_count:
                shutil.move(deaccession_csv, f"/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/deletion_staging/{aip}_deaccessions_2.csv")
                print(f"Removed {deaccession_csv}")
                os.rename(new_deaccession_csv, new_deaccession_csv.parent / f"{aip}_deaccessions.csv")
            else: 
                print(f"Line counts do not match for {aip}")

main()
    

