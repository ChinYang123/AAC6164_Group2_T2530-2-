# directory_monitor.py
# Student A - Directory Monitoring Module

import os
import time
import stat
import pwd
import grp
from datetime import datetime

# Configuration
MONITORED_DIR = "test_folder"
POLL_INTERVAL = 3

def get_file_type(mode):
    """Helper to translate mode bits to human-readable file type."""
    if stat.S_ISREG(mode):
        return "regular file"
    elif stat.S_ISDIR(mode):
        return "directory"
    elif stat.S_ISLNK(mode):
        return "symbolic link"
    else:
        return "other"

def format_time(epoch_time):
    """Convert timestamp to readable string."""
    return datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")

def snapshot(directory):
    """
    Scans the directory and returns a state dictionary.
    Key: Filename
    Value: Tuple (Size, Modification Time, Mode/Permissions)
    """
    files = {}
    if not os.path.exists(directory):
        return {}
        
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            # Use lstat to correctly handle symbolic links
            if os.path.exists(item_path):
                st = os.lstat(item_path)
                # Store tuple: (size, mtime, mode) for comparison
                files[item] = (st.st_size, st.st_mtime, st.st_mode)
    except Exception as e:
        print(f"[Error] Snapshot failed: {e}")
        
    return files

def extract_metadata(file_path):
    """
    Extracts detailed metadata for Assignment Requirement A.iv.
    Returns a dictionary or None if file missing.
    """
    try:
        st = os.stat(file_path)
        file_name = os.path.basename(file_path)
        
        try:
            owner = pwd.getpwuid(st.st_uid).pw_name
            group = grp.getgrgid(st.st_gid).gr_name
        except KeyError:
            owner = str(st.st_uid)
            group = str(st.st_gid)
            
        return {
            "filename": file_name,
            "type": get_file_type(st.st_mode),
            "size": st.st_size,
            "owner": owner,
            "group": group,
            "permissions": stat.filemode(st.st_mode),
            "created": format_time(st.st_ctime),
            "modified": format_time(st.st_mtime)
        }
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    # Ensure directory exists
    if not os.path.exists(MONITORED_DIR):
        os.makedirs(MONITORED_DIR)

    print(f"\n[INFO] Directory Monitor Running on: {MONITORED_DIR}")
    print("[INFO] Press Ctrl+C to stop...\n")

    # Initial snapshot
    prev = snapshot(MONITORED_DIR)

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            curr = snapshot(MONITORED_DIR)
            timestamp = datetime.now().strftime("%H:%M:%S")

            # --- 1. DETECT CREATION ---
            created = set(curr.keys()) - set(prev.keys())
            for f in created:
                print(f"[{timestamp}] [CREATED] {f}")
                # Log metadata for new files (Requirement A.iv)
                meta = extract_metadata(os.path.join(MONITORED_DIR, f))
                if meta:
                    print(f"   Details: {meta['type']}, {meta['size']} bytes, Owner: {meta['owner']}")

            # --- 2. DETECT DELETION ---
            deleted = set(prev.keys()) - set(curr.keys())
            for f in deleted:
                print(f"[{timestamp}] [DELETED] {f}")

            # --- 3. DETECT MODIFICATION (With Old vs New Values) ---
            common_files = set(prev.keys()) & set(curr.keys())
            for f in common_files:
                # If the tuple (size, time, mode) has changed
                if prev[f] != curr[f]:
                    print(f"[{timestamp}] [MODIFIED] {f}")
                    
                    # Unpack tuple to compare specific fields
                    old_size, old_time, old_mode = prev[f]
                    new_size, new_time, new_mode = curr[f]
                    
                    # Check Size
                    if old_size != new_size:
                        print(f"   -> Size change: {old_size} bytes -> {new_size} bytes")
                    
                    # Check Time
                    if old_time != new_time:
                        print(f"   -> Modified at: {format_time(new_time)}")
                        
                    # Check Permissions
                    if old_mode != new_mode:
                        print(f"   -> Permissions changed")

            # Update state for next loop
            prev = curr
            
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped.")
