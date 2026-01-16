# directory_monitor.py
# Student A - Directory Monitoring Module

import os
import time
import stat
import pwd
import grp
import csv  
from datetime import datetime

# Configuration
MONITORED_DIR = "test_folder"
POLL_INTERVAL = 3
CSV_FILE = "file_monitor_log.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "event_type", "filename", "details"])

def log_to_csv(event_type, filename, details):
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, event_type, filename, details])

def get_file_type(mode):
    if stat.S_ISREG(mode): return "regular file"
    elif stat.S_ISDIR(mode): return "directory"
    elif stat.S_ISLNK(mode): return "symbolic link"
    else: return "other"

def format_time(epoch_time):
    return datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")

def snapshot(directory):
    files = {}
    if not os.path.exists(directory): return {}
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.exists(item_path):
                st = os.lstat(item_path)
                files[item] = (st.st_size, st.st_mtime, st.st_mode)
    except Exception:
        pass
    return files

def extract_metadata(file_path):
    try:
        st = os.stat(file_path)
        return {
            "type": get_file_type(st.st_mode),
            "size": st.st_size,
            "owner": pwd.getpwuid(st.st_uid).pw_name
        }
    except:
        return None

if __name__ == "__main__":
    if not os.path.exists(MONITORED_DIR): os.makedirs(MONITORED_DIR)

    print(f"\n[INFO] Monitoring: {MONITORED_DIR}")
    print(f"[INFO] Logging to: {CSV_FILE}") 
    print("[INFO] Press Ctrl+C to stop...\n")

    prev = snapshot(MONITORED_DIR)

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            curr = snapshot(MONITORED_DIR)
            timestamp = datetime.now().strftime("%H:%M:%S")

            # 1. CREATED
            created = set(curr.keys()) - set(prev.keys())
            for f in created:
                print(f"[{timestamp}] [CREATED] {f}")
                meta = extract_metadata(os.path.join(MONITORED_DIR, f))
                details = f"Type: {meta['type']}, Size: {meta['size']}" if meta else "N/A"
                # --- 写入 CSV ---
                log_to_csv("CREATED", f, details)

            # 2. DELETED
            deleted = set(prev.keys()) - set(curr.keys())
            for f in deleted:
                print(f"[{timestamp}] [DELETED] {f}")
                log_to_csv("DELETED", f, "File removed")

            # 3. MODIFIED
            common = set(prev.keys()) & set(curr.keys())
            for f in common:
                if prev[f] != curr[f]:
                    print(f"[{timestamp}] [MODIFIED] {f}")
                    
                    old_size, old_time, old_mode = prev[f]
                    new_size, new_time, new_mode = curr[f]
                    
                    details = ""
                    if old_size != new_size:
                        details = f"Size: {old_size}->{new_size}"
                        print(f"   -> {details}")
                    elif old_mode != new_mode:
                        details = "Permissions changed"
                        print(f"   -> {details}")
                    else:
                        details = "Content/Time updated"
                        print(f"   -> {details}")
                    
                    log_to_csv("MODIFIED", f, details)

            prev = curr

    except KeyboardInterrupt:
        print("\n[INFO] Stopped.")
