import os
from pathlib import Path

def add_text_to_file_in_directory(directory, text_to_add):
    # Walk through the directory tree
    for dir in os.listdir(directory):
        if dir == '.DS_Store':
            continue 
        dir_path = Path(directory, dir)
        info_path = dir_path / f"reports/{dir}_processing.info"
        if info_path.exists():
            # Open the file in append mode and add the text
            with open(info_path, 'a', encoding='utf-8') as file:
                file.write(text_to_add + '\n')
            print(f"Text added to {info_path}")
        else:
            # Open the file in append mode and add the text
            with open(info_path, 'w', encoding='utf-8') as file:
                file.write(text_to_add + '\n')
            print(f"{info_path} created and text added")



directory_to_search = '/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/AIPs/hard_drives'
text_to_add = '''All item-level deaccession decisions are documented in the deaccession log stored in the reports directory of each AIP.

The initial round of appraisal was completed in early 2024 by MKFA Digital Archivist, Brock Stuessi. The technical appraisal process used DROID reports generated from the original hard drives and computers. The data in these reports was analyzed in a database to identify out of scope and duplicate files. Out of scope files were identified using file paths and file format identifications, including operating system files; software application files and metadata; commercial music recordings; digitization project images; and unidentified data and temporary files. Duplicate files were identified by checksum; the determination of which file to weed was achieved by grouping and ranking drives by record modification date, user accounts, and primary or backup status.

In the final months of 2024 Director of Archives, Mary Haberle, and Archivist, Lori Dedeyan, executed a final round of appraisal that removed data without research value from the archives. This process included the following categories of material: duplicates without contextual value; software application files, including temporary files, accounting software backups, and files related to Kelley Studio's FileMaker Pro database; commercial music recordings; and out of scope materials such as studio staff personal files, Mike Kelley Foundation for the Arts materials, and studio inventory materials created in the wake of Kelley's passing.'''

add_text_to_file_in_directory(directory_to_search, text_to_add)
