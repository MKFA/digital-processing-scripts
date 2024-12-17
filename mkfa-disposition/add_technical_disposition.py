import csv
import os
from pathlib import Path


def replace_scope_and_remove_user(input_file, output_file):
    column_to_remove = 'file_user'
    old_value = 'duplicate'
    new_value = 'Technical - duplicate'

    # Open the input and output files
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        
        # Define new fieldnames, excluding 'file_user' and 'file_type'
        new_fieldnames = [field for field in reader.fieldnames if field != column_to_remove and field != 'file_type']
        
        # Create a CSV writer to write the rows to the output file
        writer = csv.writer(outfile)
        writer.writerow(new_fieldnames)  # Write the header (fieldnames)
        
        # Write rows without the specified column
        for row in reader:
            # Remove 'file_user' and 'file_type' columns
            # row.pop(column_to_remove, None)
            # dispo_type = row.pop('file_type', None)  # Remove 'file_type' column
            
            # # Modify 'Technical' value based on dispo_type
            # if dispo_type:
            #     new_value_with_type = new_value + ' - ' + dispo_type
            # else:
            #     new_value_with_type = new_value
            
            # Replace occurrences of old_value ('scope') with the new value ('Technical')
            new_row = []
            for field in new_fieldnames:
                cell_value = row.get(field, '')  # Get the value of the current column
                if cell_value == old_value:
                    new_row.append(new_value)  # Replace with the modified value
                else:
                    new_row.append(cell_value)  # Otherwise keep the original value
            
            # Write the modified row
            writer.writerow(new_row)
        

def main():
    AIP_dir = Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/AIPs/hard_drives")
    for aip in os.listdir(AIP_dir):
        if aip == ".DS_Store":
            continue
        deaccession_csv = AIP_dir / aip / "reports" / "appraisal" / f"{aip}_deaccessions.csv"
        new_deaccession_csv = AIP_dir / aip / "reports" / "appraisal" / f"{aip}_deaccessions_adjusted.csv"

        if deaccession_csv.exists():
            print(f"Modifying deaccession csv for {aip}")
            replace_scope_and_remove_user(deaccession_csv, new_deaccession_csv)


main()