import psutil
import datetime
import os
import time

def get_report():
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    boot_time = psutil.boot_time()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    idle_seconds = psutil.cpu_times().idle
    idle_str = str(datetime.timedelta(seconds=int(idle_seconds)))

    # --- v. Active Processes Statistics ---
    all_pids = psutil.pids()
    running_cnt = 0
    sleeping_cnt = 0
    for pid in all_pids:
        try:
            status = psutil.Process(pid).status()
            if status == psutil.STATUS_RUNNING: running_cnt += 1
            elif status == psutil.STATUS_SLEEPING: sleeping_cnt += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied): continue

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

    return report

if __name__ == "__main__":
    try:
        while True:
            print(get_report())
            print("Next update in 10 seconds... (Ctrl+C to stop)")
            time.sleep(10) 
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
