import os
import shutil

top_level = "/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/AIPs"


for root, dirs, files in os.walk(top_level):
    for file in files:
        if file == '.DS_Store':
            file_path = os.path.join(root, file)
            print(f"Removing {file_path}")
            os.remove(file_path)