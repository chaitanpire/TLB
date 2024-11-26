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
trace_policy_latency = {trace: {policy: 0 for policy in policies} for trace in traces}
print(trace_policy_latency)
# Parse files in ./logs_srrip to extract latency values
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
                        if re.search("STLB AVERAGE MISS LATENCY:", line):
                            print(line)
                            latency = float(line.split()[-2])
                            trace_policy_latency[trace][policy] = latency
                            print(f"Trace {trace}, Policy {policy}, latency {latency}")
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found.")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Create the bar graph
bar_width = 0.1
x_indices = np.arange(len(traces))
colors = plt.cm.tab10.colors  # Use a colormap for distinct policy colors

plt.figure(figsize=(20, 6))
for i, policy in enumerate(policies):
    latency_values = [trace_policy_latency[trace][policy] for trace in traces]
    plt.bar(
        x_indices + i * bar_width,
        latency_values,
        bar_width,
        label=policy,
        color=colors[i % len(colors)],
    )

# Customize the plot
plt.xticks(x_indices + bar_width * (len(policies) - 1) / 2, traces, rotation=45)
plt.xlabel("Traces")
plt.ylabel("latency")
plt.title("latency Comparison Across Traces and Policies")
plt.legend(title="Policies")
plt.tight_layout()

# Show the plot
plt.show()

# save this dictionary to a file latency.csv
import csv

with open('latency.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Trace'] + policies)
    for trace in traces:
        writer.writerow([trace] + [trace_policy_latency[trace][policy] for policy in policies])

