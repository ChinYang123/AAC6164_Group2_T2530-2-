import psutil
import datetime

def get_report():
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent  
    disk = psutil.disk_usage('/').percent    
    
    report = f"--- System Status Report {time_str} ---\n"
    report += f"CPU Usage: {cpu}%\n"
    report += f"Memory Usage: {memory}%\n"
    report += f"Disk Usage: {disk}%\n"
    
    return report

if __name__ == "__main__":
    print(get_report())
