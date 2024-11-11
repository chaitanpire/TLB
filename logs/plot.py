import matplotlib.pyplot as plt
import re

# Initialize a list to store the differences
first_min_diffs = []
start_processing = False  # Flag to start processing after "WARMPUP COMPLETE" line

# Read and process each line in the file
with open('logs_srrip/623.xalancbmk_s-700B.champsimtrace.xz/collisions.txt', 'r') as file:
    for line in file:
        # Trim whitespace and check for "WARMPUP COMPLETE" in a case-insensitive way
        if "warmpup complete" in line.strip().lower():
            start_processing = True
            continue  # Skip the "WARMPUP COMPLETE" line itself

        # Start processing lines after "WARMPUP COMPLETE"
        if start_processing:
            # Use regex to find all pairs of the form "address: value"
            pairs = re.findall(r'(\d+)\s*:\s*(\d+)', line.strip())
            if pairs:
                values = [int(value) for _, value in pairs]
            else:
                print("No valid pairs found.")
                continue

            # Only process lines with more than 1 value
            if len(values) > 1:
                # Get the first value and the minimum of the values
                first_value = values[0]
                min_value = min(values)
                
                # Calculate the difference
                diff = first_value - min_value
                print(f"First value: {first_value}, Min value: {min_value}, Difference: {diff}")  # Debugging output
                if diff:
                    first_min_diffs.append(diff)

# Check if there were any valid differences
if not first_min_diffs:
    print("No valid differences were found.")

# Define the bin width
bin_width = 20

# Calculate the number of bins based on the desired bin width
data_range = max(first_min_diffs) - min(first_min_diffs)
num_bins = int(data_range / bin_width)

# Plotting the histogram of the differences with the x-axis limited to 600
plt.figure(figsize=(10, 5))
plt.xlim(0, 600)
plt.hist(first_min_diffs, bins=num_bins, color='skyblue', edgecolor='black')
plt.xlabel('Difference between First Value and Min Value')
plt.ylabel('Frequency')
plt.title('Histogram of Differences (First Value - Min Value) in Each Line')
plt.grid(True)
plt.savefig('logs_srrip/623.xalancbmk_s-700B.champsimtrace.xz/histogram.png')

