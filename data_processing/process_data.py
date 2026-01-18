import pandas as pd
import matplotlib.pyplot as plt
# Read system data
sys_df = pd.read_csv("../module_b_performance_tracking/logs/performance_report.csv")
avg_cpu = sys_df["cpu_percent"].mean()
max_cpu = sys_df["cpu_percent"].max()

# Read directory data
dir_df = pd.read_csv("../directory_monitor/file_monitor_log.csv")
created = (dir_df["event_type"] == "created").sum()
modified = (dir_df["event_type"] == "modified").sum()
deleted = (dir_df["event_type"] == "deleted").sum()

# Plot CPU usage
plt.plot(sys_df["timestamp"], sys_df["cpu_percent"])
plt.xlabel("Time")
plt.ylabel("CPU Usage (%)")
plt.title("CPU Usage Over Time")
plt.savefig("cpu_usage.png")
plt.close()
# Write report
with open("final_report.txt", "w") as f:
    f.write("System Monitoring Summary\n")
    f.write("-------------------------\n")
    f.write(f"Average CPU Usage: {avg_cpu:.2f}%\n")
    f.write(f"Maximum CPU Usage: {max_cpu:.2f}%\n\n")
    f.write("Directory Activity Summary\n")
    f.write("--------------------------\n")
    f.write(f"Files Created: {created}\n")
    f.write(f"Files Modified: {modified}\n")
    f.write(f"Files Deleted: {deleted}\n")

print("C module executed successfully")
