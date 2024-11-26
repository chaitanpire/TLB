import os
import re
import numpy as np
import matplotlib.pyplot as plt

# Make a list of names of trace files from the directory ./traces
traces = []
for root, dirs, files in os.walk("./logs_srrip"):
    for dir in dirs:
        if dir.endswith(".xz"):
            traces.append(dir)  # Remove ".xz" extension for better matching

traces.sort()
# Make a list of all policies from the directory ./logs_srrip/429.mcf-22B.champsimtrace.xz
policies = []
policy_dir = "./logs_srrip/429.mcf-184B.champsimtrace.xz"
for root, dirs, files in os.walk(policy_dir):
    for file in files:
        if file.endswith(".txt"):
            policies.append(file[:-4])  # Remove ".txt" extension
policies.sort()

print(f"Traces: {traces}")
print(f"Policies: {policies}")
# Prepare data for the bar graph
trace_policy_speedup = {trace: {policy: 0 for policy in policies} for trace in traces}
print(trace_policy_speedup)
# Parse files in ./logs_srrip to extract speedup values
for root, dirs, files in os.walk("./logs_srrip"):
    for dir in dirs:
        trace = dir
        print(f"Trace: {trace}")
        try:
            for policy in policies:
                file_path = os.path.join(root, dir, policy + ".txt")
            
                with open(file_path, 'r') as f:
                    print(f"Reading {file_path}")
                    for line in f:
                        if re.search("CPU 0 cumulative", line):
                            print(line)
                            speedup = float(line.split()[-1])
                            trace_policy_speedup[trace][policy] = speedup
                            print(f"Trace {trace}, Policy {policy}, speedup {speedup}")
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found.")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Create the bar graph
bar_width = 0.1
x_indices = np.arange(len(traces))
colors = plt.cm.tab10.colors  # Use a colormap for distinct policy colors

# divide all speed up values by the speed up value of the lru policy

for trace in traces:
    for policy in policies:
        if policy != 'lru':
            trace_policy_speedup[trace][policy] = trace_policy_speedup[trace][policy] / trace_policy_speedup[trace]['lru']
    trace_policy_speedup[trace]['lru'] = 1

plt.figure(figsize=(20, 6))
for i, policy in enumerate(policies):
    speedup_values = [trace_policy_speedup[trace][policy] for trace in traces]
    plt.bar(
        x_indices + i * bar_width,
        speedup_values,
        bar_width,
        label=policy,
        color=colors[i % len(colors)],
    )

# Customize the plot
plt.xticks(x_indices + bar_width * (len(policies) - 1) / 2, traces, rotation=45)
plt.xlabel("Traces")
plt.ylabel("speedup")
plt.ylim(0.99, 1.01)
plt.title("speedup Comparison Across Traces and Policies")
plt.legend(title="Policies")
plt.tight_layout()

# Show the plot
plt.show()

# save this dictionary in speedup.csv, such that the rows correpond to trace file and columns correspond to policies

import csv
with open('speedup.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Trace'] + policies)
    for trace in traces:
        writer.writerow([trace] + [trace_policy_speedup[trace][policy] for policy in policies])
