# directory_monitor.py
# Student A - Directory Monitoring Module (Commit 2 - Basic Scanning + Metadata)

import os
import stat
import pwd
import grp
from datetime import datetime

MONITORED_DIR = "directory_monitor/test_dir"

def get_file_type(mode):
    if stat.S_ISREG(mode):
        return "regular file"
    elif stat.S_ISDIR(mode):
        return "directory"
    elif stat.S_ISLNK(mode):
        return "symbolic link"
    else:
        return "other"

def format_time(epoch_time):
    return datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")

def extract_metadata(file_path):
    st = os.stat(file_path)

    file_name = os.path.basename(file_path)
    file_type = get_file_type(st.st_mode)
    file_size = st.st_size

    owner = pwd.getpwuid(st.st_uid).pw_name
    group = grp.getgrgid(st.st_gid).gr_name

    permissions = stat.filemode(st.st_mode)

    access_time = format_time(st.st_atime)
    modify_time = format_time(st.st_mtime)
    create_time = format_time(st.st_ctime)  # Linux: ctime = metadata change time

    return {
        "filename": file_name,
        "file_type": file_type,
        "file_size": file_size,
        "owner": owner,
        "group": group,
        "permissions": permissions,
        "access_time": access_time,
        "modify_time": modify_time,
        "create_time": create_time
    }

def scan_directory(directory):
    print(f"\n[INFO] Scanning directory: {directory}\n")

    if not os.path.exists(directory):
        print("[ERROR] Directory does not exist.")
        return

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isfile(item_path) or os.path.isdir(item_path):
            meta = extract_metadata(item_path)

            print("----- FILE METADATA -----")
            for k, v in meta.items():
                print(f"{k}: {v}")
            print("-------------------------\n")

if __name__ == "__main__":
    scan_directory(MONITORED_DIR)
