import csv
import os
import shutil
from pathlib import Path
import configparser
from datetime import datetime
import logging
import sys
import re

# helper functions 
def fTime():
    query_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return query_time

#setting script dir
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

#getting info from ini file
config_input = "disposition-config.ini"
config = configparser.ConfigParser()
config.sections()
config.read(config_input)

digital_id = config['VARIABLES']['digital_id']
AIP_path = Path(config['VARIABLES']['AIP_path'])
access_or_pres = config['VARIABLES']['access_or_pres']
reappraisal_csv = Path(config['VARIABLES']['reappraisal_csv'])


disposition_actions = {
    "Software": {"preservation-action": "keep",
                "access-action": "remove",},
    "Software - FMP": {"preservation-action": "remove",
                "access-action": "remove"},
    "Software - Temp": {"preservation-action": "remove",
                "access-action": "remove"},
    "Music": {"preservation-action": "remove",
                "access-action": "remove"},
    "Foundation": {"preservation-action": "remove",
                "access-action": "remove",
                "staging-location": Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/Staged files/MKFA")},
    "Legacy": {"preservation-action": "remove",
                "access-action": "remove",
                "staging-location": Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/Staged files/Deaccessioned AIPs - To Review/Legacy")},
    "Limited value": {"preservation-action": "remove",
                "access-action": "remove",
                "staging-location": Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/Staged files/Deaccessioned AIPs - To Review/Limited value")},
    "Photographs - Portfolio": {"preservation-action": "remove",
                "access-action": "remove",
                "staging-location": Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/Staged files/Deaccessioned AIPs - To Review/Photographs - Portfolio")},
    "Personal": {"preservation-action": "remove",
                "access-action": "remove",
                "staging-location": Path("/Volumes/MKFA/ARCHIVES STORAGE/Born_digital_processing/Staged files/Deaccessioned AIPs - To Review/Personal")},
    "Duplicate": {"preservation-action": "remove",
                "access-action": "remove"},
    "Duplicate - Downloads": {"preservation-action": "remove",
                "access-action": "remove"},
    "Duplicate - Recycler": {"preservation-action": "remove",
                "access-action": "remove"},
    "Duplicate - All Users": {"preservation-action": "keep",
                "access-action": "remove"}
}

#remove file_user
deaccession_headers = [ "id", "file_path", "file_name", "size", "mtime", "md5_hash", 
    "appraisal_decision", "puid", 
    "name", "mime_type", "extension", "version"]

disposition_headers = [
    "disposition", "filename", "filesize", "modified", "errors", "md5", 
    "namespace", "id", "format", "version", "mime", "class", "basis", "warning"
]


############    DISPOSITION FUNCTIONS     ################

#formatting paths with correct roots, either to server location or mounted disk images
def format_path(file_path, root):
    relative_path = Path(file_path.split("/original_files", 1)[-1].lstrip("/"))
    new_path = root / "original_files" / relative_path
    return new_path

def is_directory_empty(directory: Path) -> bool:
    # Check if the directory exists and is indeed a directory
    if directory.is_dir():
        # Check if the directory is empty
        return not any(directory.iterdir())  # Return True if empty, False otherwise
    else:
        raise ValueError(f"{directory} is not a valid directory")

# remove 
# delete files or move to a staging location
# make sure to handle MC files as exceptions correctly
def remove(file_path, storage_root,  staging_location=None):
    og_location = Path(format_path(file_path, storage_root))
    if og_location.exists():
        if staging_location:
            staging_path = Path(staging_location, digital_id, file_path.split("/original_files", 1)[-1][1:])
            os.makedirs(staging_path.parent, exist_ok=True)
            shutil.move(og_location, staging_path)
            print(f"{file_path} moved to {staging_location}")
            root_logger.info(f"{file_path} moved to {staging_location}")
            if is_directory_empty(og_location.parent):
                os.removedirs(og_location.parent)
                root_logger.info(f"{og_location.parent} directory removed.")
            return True
        else:
            os.remove(og_location)
            print(f"{file_path} removed")
            root_logger.info(f"{file_path} removed")
            if is_directory_empty(og_location.parent):
                os.removedirs(og_location.parent)
                root_logger.info(f"{og_location.parent} directory removed.")
            return True
    else:
        print(f"File not found at {og_location}")
        root_logger.error(f"File not found at {og_location}")
        return False


# add disposition action to log
def add_to_deaccession_log(file_path, disposition_action, size, checksum, modified, puid, format, mime_type, log_path):
    with open(log_path, "a") as log_csv:
        writer = csv.DictWriter(log_csv, fieldnames=deaccession_headers)
        writer.writerow({"file_path": file_path, "size": size, "md5_hash": checksum, "mtime": modified, "appraisal_decision": disposition_action, "puid": puid, "name": format, "mime_type": mime_type})
    
    return None

def create_deaccession_log(AIP_dir, digital_id):
    deaccession_log_path = Path(AIP_dir, f"reports/appraisal/{digital_id}_deaccessions.csv")
    if deaccession_log_path.exists():
        return deaccession_log_path
    else:
        deaccession_path_decision = input(f'''A deaccession log for {digital_id} was not found at {deaccession_log_path}\n
                                            Enter 1 if you would like to create a deaccession file at {deaccession_log_path}\n
                                            Enter 2 if you would like to stop the script. ''')
        if deaccession_path_decision == "1":
            os.makedirs(deaccession_log_path.parent, exist_ok=True)
            with open(deaccession_log_path, "w+") as deaccession_csv:
                writer = csv.writer(deaccession_csv)
                writer.writerow(deaccession_headers)
            return deaccession_log_path
        elif deaccession_path_decision == "2":
            sys.exit()



##########     GENERAL LOGGING     ############
# Set up logging
log_dir = Path(script_dir, "Logs")
log_file = log_dir / f"{digital_id}_{fTime()}.log"
root_logger = logging.getLogger("MainLogger")
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file, 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
root_logger.addHandler(handler)
root_logger.info("Log file for " + str(os.path.basename(__file__)))

##########      CSV PARSING      #############

# verify disposition entries in CSV
def verify_csv(reappraisal_csv_path):
    with open(reappraisal_csv_path, "r") as aip_csv:
        header = disposition_headers
        reader = csv.DictReader(aip_csv, fieldnames=header)
        next(reader)
        row_num = 1
        for row in reader:
            row_num += 1
            disposition_decision = row["disposition"]
            if disposition_decision in disposition_actions.keys():
                continue
            elif disposition_decision == '':
                continue
            else:
                raise ValueError(f"Unrecognized disposition value: {disposition_decision} in row {row_num}")

# parse AIP csv
def parse_csv(reappraisal_csv_path, type, root, deaccession_log_path):
    with open(reappraisal_csv_path, "r") as aip_csv:
        header = disposition_headers
        reader = csv.DictReader(aip_csv, fieldnames=header)
        next(reader)
        for row in reader:
            try:
                disposition_decision = row["disposition"]
                if disposition_decision in disposition_actions.keys():
                    disposition_executables = disposition_actions[disposition_decision]
                    access_action = disposition_executables['access-action']
                    preservation_action = disposition_executables['preservation-action']
                    if type == 'preservation':
                        action = preservation_action
                    else:
                        action = access_action
    
                    file_path = row["filename"]
    
                    if action == "remove":
                        if disposition_decision == "Personal" and "MC" not in file_path:
                            remove_result = remove(file_path, root)
                        elif "staging-location" in disposition_executables.keys():
                            staging = disposition_executables['staging-location']
                            remove_result = remove(file_path, root, staging_location=staging)
                        else:
                            remove_result = remove(file_path, root)
    
                        if remove_result:
                            if file_path.startswith("/p"):
                                file_path = re.sub(r'^\/p', '', file_path)
                            add_to_deaccession_log(file_path, disposition_decision, row['filesize'], row["md5"], row["modified"], row['id'], row['format'], row['mime'], deaccession_log_path)
                    
                    elif action == "keep":
                        continue
            except Exception as e:
                root_logger.error(f"Error: {e}")
      


def main():
    deaccession_log_path = create_deaccession_log(AIP_path, digital_id)
    verify_csv(reappraisal_csv)
    parse_csv(reappraisal_csv, access_or_pres, AIP_path, deaccession_log_path)

main()
