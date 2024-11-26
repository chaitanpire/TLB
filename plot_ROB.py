# parse all the files in the subdirectories in directory ./logs_srrip
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

for root, dirs, files in os.walk("./logs_srrip"):
    for file in files:
        x = []
        y = []
        if file.endswith("srrip.txt"):
            trace = root.split("/")[-1]
            print("Trace: ", trace)
            file_path = os.path.join(root, file)
            phrase = "Stall Caused by STLB for"
            phrase2 = "Number of misses for instr_id"
            with open(file_path, 'r') as f:
                print("File: ", file)
                for line in f:
                    if re.search(phrase, line): 
                        y.append(int(line.split()[-1]))
                    if re.search(phrase2, line):
                        x.append(int(line.split()[-1]))
            plt.hist(y, bins=100, label=trace, alpha=0.5)
            plt.xlabel("No. Stall Caused by the page")
            plt.ylabel("Frequency")
            plt.xlim(0, 20000)
            plt.savefig("./logs_srrip/" + trace + "/srrip_stall_hist.png")
            plt.clf()
            

            # filter x and y such that x is > 1
            y = [y[i] for i in range(len(y)) if x[i] > 1]
            x = [x[i] for i in range(len(x)) if x[i] > 1]
            y = np.array(y)
            x = np.array(x)
            plt.scatter(x, y/x, label=trace)
            plt.xlabel("Number of Misses")
            plt.ylabel("Average Stall Caused by this page")
            plt.savefig("./logs_srrip/" + trace + "/srrip_stall_vs_misses.png")
            plt.clf()
        if file.endswith("srrip_rob_pref_32.txt"):
            trace = root.split("/")[-1]
            print("Trace: ", trace)
            file_path = os.path.join(root, file)
            phrase = "Stall Caused by STLB for"
            phrase2 = "Number of misses for instr_id"
            with open(file_path, 'r') as f:
                print("File: ", file)
                for line in f:
                    if re.search(phrase, line): 
                        y.append(int(line.split()[-1]))
                    if re.search(phrase2, line):
                        x.append(int(line.split()[-1]))
            plt.hist(y, bins=100, label=trace, alpha=0.5)
            plt.xlabel("No. Stall Caused by the page")
            plt.ylabel("Frequency")
            plt.xlim(0, 20000)

            plt.savefig("./logs_srrip/" + trace + "/srrip_rob_pref_32_stall_hist.png")
            plt.clf()
            

            # filter x and y such that x is > 1
            y = [y[i] for i in range(len(y)) if x[i] > 1]
            x = [x[i] for i in range(len(x)) if x[i] > 1]
            y = np.array(y)
            x = np.array(x)
            plt.scatter(x, y/x, label=trace)
            plt.xlabel("Number of Misses")
            plt.ylabel("Average Stall Caused by this page")
            plt.savefig("./logs_srrip/" + trace + "/srrip_rob_pref_32_stall_vs_misses.png")
            plt.clf()
    
