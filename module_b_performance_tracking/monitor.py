import psutil
import datetime
import os
import time
<<<<<<< HEAD
import csv

def get_report():
    now_dt = datetime.datetime.now()
    time_display = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    time_csv = now_dt.strftime("%Y-%m-%d %H:%M")

    cpu_pct = psutil.cpu_percent(interval=1)
    load_1, load_5, load_15 = psutil.getloadavg()

    mem = psutil.virtual_memory()
    m_total, m_used, m_avail = mem.total/(1024**3), mem.used/(1024**3), mem.available/(1024**3)

    disk = psutil.disk_usage('/')
    d_total, d_used, d_free = disk.total/(1024**3), disk.used/(1024**3), disk.free/(1024**3)

=======

def get_report():
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
<<<<<<< HEAD

    # --- i. CPU Metrics ---
    cpu_pct = psutil.cpu_percent(interval=1)
    load_1, load_5, load_15 = psutil.getloadavg()

    # --- ii. Memory Metrics ---
    mem = psutil.virtual_memory()
    m_total, m_used, m_avail = mem.total/(1024**3), mem.used/(1024**3), mem.available/(1024**3)

    # --- iii. Disk Metrics ---
    disk = psutil.disk_usage('/')
    d_total, d_used, d_free = disk.total/(1024**3), disk.used/(1024**3), disk.free/(1024**3)

    # --- iv. System Uptime & Idle Time ---
>>>>>>> 42e410159ce9a7c26b5edb8ccc3d7d96e1fa70de
    boot_time = psutil.boot_time()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    idle_seconds = psutil.cpu_times().idle
    idle_str = str(datetime.timedelta(seconds=int(idle_seconds)))

<<<<<<< HEAD
=======
    # --- v. Active Processes Statistics ---
>>>>>>> 42e410159ce9a7c26b5edb8ccc3d7d96e1fa70de
    all_pids = psutil.pids()
    running_cnt = 0
    sleeping_cnt = 0
    for pid in all_pids:
        try:
            status = psutil.Process(pid).status()
            if status == psutil.STATUS_RUNNING: running_cnt += 1
            elif status == psutil.STATUS_SLEEPING: sleeping_cnt += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied): continue

<<<<<<< HEAD
    top_cpu = sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda x: x.info['cpu_percent'], reverse=True)[:3]
    top_mem = sorted(psutil.process_iter(['name', 'memory_percent']), key=lambda x: x.info['memory_percent'], reverse=True)[:3]


    report_text = f"\n{'='*20} SYSTEM REPORT ({time_display}) {'='*20}\n"
    report_text += f"i. CPU Metrics:\n   - Usage: {cpu_pct}% | Load: {load_1:.2f}, {load_5:.2f}, {load_15:.2f} | Running: {running_cnt}\n"
    report_text += f"ii. Memory:\n   - Total: {m_total:.2f}GB | Used: {m_used:.2f}GB | Available: {m_avail:.2f}GB | {mem.percent}%\n"
    report_text += f"iii. Disk:\n   - Total: {d_total:.2f}GB | Used: {d_used:.2f}GB | Free: {d_free:.2f}GB | {disk.percent}%\n"
    report_text += f"iv. Uptime:\n   - Total: {str(uptime).split('.')[0]} | Idle: {idle_str}\n"
    report_text += f"v. Processes:\n   - Total: {len(all_pids)} | Running vs Sleeping: {running_cnt}/{sleeping_cnt}\n"
    report_text += f"   - Top 3 CPU: {', '.join([p.info['name'] for p in top_cpu])}\n"
    report_text += f"   - Top 3 Mem: {', '.join([p.info['name'] for p in top_mem])}\n"


    csv_row = [time_csv, cpu_pct, mem.percent, disk.percent]

    return report_text, csv_row

def save_to_csv(data_row, filename="logs/performance_report.csv"):
    os.makedirs("logs", exist_ok=True)
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'cpu_percent', 'memory_percent', 'disk_percent'])
        writer.writerow(data_row)
=======
    # Get Top 3
    top_cpu = sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda x: x.info['cpu_percent'], reverse=True)[:3]
    top_mem = sorted(psutil.process_iter(['name', 'memory_percent']), key=lambda x: x.info['memory_percent'], reverse=True)[:3]

    report = f"\n{'='*20} SYSTEM REPORT ({time_str}) {'='*20}\n"

    report += f"i. CPU Metrics:\n"
    report += f"   - Usage: {cpu_pct}%\n"
    report += f"   - Load Average (1, 5, 15 min): {load_1:.2f}, {load_5:.2f}, {load_15:.2f}\n"
    report += f"   - Number of running processes: {running_cnt}\n\n"

    report += f"ii. Memory Metrics:\n"
    report += f"   - Total: {m_total:.2f}GB | Used: {m_used:.2f}GB | Available: {m_avail:.2f}GB\n"
    report += f"   - Usage Percentage: {mem.percent}%\n\n"

    report += f"iii. Disk Metrics (Root Partition):\n"
    report += f"   - Total: {d_total:.2f}GB | Used: {d_used:.2f}GB | Free: {d_free:.2f}GB\n"
    report += f"   - Usage Percentage: {disk.percent}%\n\n"

    report += f"iv. System Uptime:\n"
    report += f"   - Total Uptime: {str(uptime).split('.')[0]}\n"
    report += f"   - System Idle Time: {idle_str}\n\n"

    report += f"v. Active Processes:\n"
    report += f"   - Total processes: {len(all_pids)}\n"
    report += f"   - Running vs. Sleeping: {running_cnt} Running, {sleeping_cnt} Sleeping\n"
    report += f"   - Top 3 by CPU: {', '.join([p.info['name'] for p in top_cpu])}\n"
    report += f"   - Top 3 by Memory: {', '.join([p.info['name'] for p in top_mem])}\n"

=======
    
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    load_1, load_5, load_15 = psutil.getloadavg()
    
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    
    process_count = len(psutil.pids())
    
    report = f"--- System Status Report {time_str} ---\n"
    report += f"Uptime: {str(uptime).split('.')[0]}\n"
    report += f"Load Average: {load_1}, {load_5}, {load_15}\n"
    report += f"Total Processes: {process_count}\n"
    report += f"CPU: {cpu}% | Mem: {mem}% | Disk: {disk}%\n"
    
>>>>>>> 67666c9c71d4fa9ec9ee53f389048aaa0011e835
    return report
>>>>>>> 42e410159ce9a7c26b5edb8ccc3d7d96e1fa70de

if __name__ == "__main__":
    try:
        while True:
<<<<<<< HEAD
            display_info, csv_data = get_report()

            print (display_info)

            save_to_csv(csv_data)

            print("Data saved to CSV. Next update in 10 seconds... (Ctrl+C to stop)")
            time.sleep(10) 
    except KeyboardInterrupt:
        print("\nMonitoring stopped. Log file is at: logs/performance_report.csv")
=======
            print(get_report())
            print("Next update in 10 seconds... (Ctrl+C to stop)")
            time.sleep(10) 
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
>>>>>>> 42e410159ce9a7c26b5edb8ccc3d7d96e1fa70de
