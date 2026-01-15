# directory_monitor.py
# Student A - Directory Monitoring Module

import os
import time
import stat
import pwd
import grp
from datetime import datetime

MONITORED_DIR = "test_folder"

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

def snapshot(directory):
    files = {}
    if not os.path.exists(directory):
        return {}
        
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.exists(item_path):
                st = os.lstat(item_path)
                # 关键：存储 (大小, 修改时间, 权限) 用于比对
                files[item] = (st.st_size, st.st_mtime, st.st_mode)
    except Exception as e:
        print(f"[Error] Snapshot failed: {e}")
        
    return files

def extract_metadata(file_path):
    try:
        st = os.stat(file_path)
        file_name = os.path.basename(file_path)
        file_type = get_file_type(st.st_mode)
        
        try:
            owner = pwd.getpwuid(st.st_uid).pw_name
            group = grp.getgrgid(st.st_gid).gr_name
        except KeyError:
            owner = str(st.st_uid)
            group = str(st.st_gid)
            
        permissions = stat.filemode(st.st_mode)
        create_time = format_time(st.st_ctime)

        return {
            "filename": file_name,
            "type": file_type,
            "size": st.st_size,
            "owner": owner,
            "permissions": permissions,
            "created": create_time
        }
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    if not os.path.exists(MONITORED_DIR):
        os.makedirs(MONITORED_DIR)

    print(f"\n[INFO] Monitoring started for: {MONITORED_DIR}")
    prev = snapshot(MONITORED_DIR)

    try:
        while True:
            time.sleep(3)
            curr = snapshot(MONITORED_DIR)
            timestamp = datetime.now().strftime("%H:%M:%S")

            # 1. 新建 (Created)
            created = set(curr.keys()) - set(prev.keys())
            for f in created:
                print(f"[{timestamp}] [CREATED] {f}")
                meta = extract_metadata(os.path.join(MONITORED_DIR, f))
                if meta:
                    print(f"   Type: {meta['type']}, Size: {meta['size']} bytes, Owner: {meta['owner']}")

            # 2. 删除 (Deleted)
            deleted = set(prev.keys()) - set(curr.keys())
            for f in deleted:
                print(f"[{timestamp}] [DELETED] {f}")

            # 3. 修改 (Modified) - 本次提交新增的核心功能
            common_files = set(prev.keys()) & set(curr.keys())
            for f in common_files:
                # 对比旧快照和新快照的信息是否一致
                if prev[f] != curr[f]:
                    print(f"[{timestamp}] [MODIFIED] {f}")
                    # 这里暂时只提示修改，具体改了什么下个版本再细化

            prev = curr
            
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped.")
