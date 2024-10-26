import matplotlib.pyplot as plt

# Initialize a list to store the differences of max and min values
max_min_diffs = []

# Read and process each line in the file
with open('trace1_srrip.txt', 'r') as file:
    for line in file:
        # Split the line into values, ignore the first value, and convert the rest to integers
        values = list(map(int, line.strip().split()[1:]))
        
        # Only process lines with at least 5 entries (excluding the first)
        if len(values) >= 5:
            # Calculate the difference between the max and min values
            max_min_diff = max(values) - min(values)
            
            # Append the difference to the list
            max_min_diffs.append(max_min_diff)

# Plotting the histogram of max-min differences
plt.figure(figsize=(10, 5))
plt.hist(max_min_diffs, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Difference between Max and Min values')
plt.ylabel('Frequency')
plt.title('Histogram of Max-Min Differences in Each Line')
plt.grid(True)
plt.show()
