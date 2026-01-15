import psutil
import datetime

def get_report():
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
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
    
    return report

if __name__ == "__main__":
    print(get_report())
