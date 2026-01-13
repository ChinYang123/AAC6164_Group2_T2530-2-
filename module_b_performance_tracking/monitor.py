import psutil
import datetime

def get_report():
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    return f"--- System Report {time_str} ---\nCPU Usage: {cpu}%"

if __name__ == "__main__":
    print(get_report())
