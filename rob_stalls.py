# parse all the files in the subdirectories in directory ./logs_srrip
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
def find_lines_with_phrase(file_path, phrase):
    matching_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if re.search(phrase, line):
                return line.split()

x = []
y = []

for root, dirs, files in os.walk("./logs_srrip"):
    for file in files:
        if file.endswith("srrip.txt"):
            trace = root.split("/")[-1]
            print("Trace: ", trace)
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                try: 
                    total_cycles = find_lines_with_phrase(file_path, "CPU 0 cumulative IPC:")[-1]
                    print("Total Cycles: ", total_cycles)
                     
                    rob_stalls_stlb = find_lines_with_phrase(file_path, "ROB Stall cycles")[-1]
                    print("STLB Miss ROB Stalls: ", rob_stalls_stlb)

                    print("% ROB Stalls due to STLB: ", float(rob_stalls_stlb)/float(total_cycles)*100)
                    line = find_lines_with_phrase(file_path, "STLB TOTAL")
                    print("STLB Total Access: ", line[3])
                    print("STLB Misses: ", line[7])
                    stlb_miss = int(line[7])
                    line = find_lines_with_phrase(file_path, "Number of ties")
                    print("Number of ties: ", line[-1])

                    print("STLB tie ratio: ", float(line[-1])/stlb_miss)
                    y.append(float(line[-1])/stlb_miss)
                    

                except:
                    print("Error in file: ", file)
                    continue
                print("\n")
plt.show()