import pandas as pd
import matplotlib.pyplot as plt
# Read system data
sys_df = pd.read_csv("../module_b_performance_tracking/logs/performance_report.csv")
avg_cpu = sys_df["cpu_percent"].mean()
max_cpu = sys_df["cpu_percent"].max()
min_cpu = sys_df["cpu_percent"].min()
avg_mem = sys_df["memory_percent"].mean()
max_mem = sys_df["memory_percent"].max()

# Read directory data
dir_df = pd.read_csv("../directory_monitor/file_monitor_log.csv")
created = (dir_df["event_type"] == "CREATED").sum()
modified = (dir_df["event_type"] == "MODIFIED").sum()
deleted = (dir_df["event_type"] == "DELETED").sum()

# Plot CPU usage
plt.plot(sys_df["timestamp"], sys_df["cpu_percent"])
plt.xlabel("Time")
plt.ylabel("CPU Usage (%)")
plt.title("CPU Usage Over Time")
plt.savefig("cpu_usage.png")
plt.close()

# Plot Memory usage
plt.plot(sys_df["timestamp"], sys_df["memory_percent"])
plt.xlabel("Time")
plt.ylabel("Memory Usage (%)")
plt.title("Memory Usage Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("memory_usage.png")
plt.close()

# Plot Disk usage
plt.plot(sys_df["timestamp"], sys_df["disk_percent"])
plt.xlabel("Time")
plt.ylabel("Disk Usage (%)")
plt.title("Disk Usage Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("disk_usage.png")
plt.close()

# Write report
with open("final_report.txt", "w") as f:
    f.write("System Monitoring Summary\n")
    f.write("=========================\n\n")

    f.write("CPU Statistics\n")
    f.write("----------------\n")
    f.write(f"Minimum CPU Usage: {min_cpu:.2f}%\n")
    f.write(f"Average CPU Usage: {avg_cpu:.2f}%\n")
    f.write(f"Maximum CPU Usage: {max_cpu:.2f}%\n\n")

    f.write("Memory Statistics\n")
    f.write("------------------\n")
    f.write(f"Average Memory Usage: {avg_mem:.2f}%\n")
    f.write(f"Maximum Memory Usage: {max_mem:.2f}%\n\n")

    f.write("Directory Activity Summary\n")
    f.write("---------------------------\n")
    f.write(f"Files Created: {created}\n")
    f.write(f"Files Modified: {modified}\n")
    f.write(f"Files Deleted: {deleted}\n")

print("C module executed successfully")
