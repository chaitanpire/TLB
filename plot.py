import matplotlib.pyplot as plt

# Initialize lists to store the computed averages
all_values_avg = []
top_3_values_avg = []

# Read and process each line in the file
with open('trace1_srrip.txt', 'r') as file:
    for line in file:
        # Split the line into values, ignore the first value, and convert the rest to integers
        values = list(map(int, line.strip().split()[1:]))
        
        # Only process lines with at least 5 entries (excluding the first)
        if len(values) >= 5:
            # Calculate the average of all values
            avg_all = sum(values) / len(values)
            
            # Calculate the average of the top 3 values
            avg_top_3 = sum(sorted(values, reverse=True)[:3]) / 3
            
            # Append the averages to respective lists
            all_values_avg.append(avg_all)
            top_3_values_avg.append(avg_top_3)

# Plotting
plt.figure(figsize=(10, 5))
plt.scatter(all_values_avg, top_3_values_avg, color='blue', label='Avg vs. Top 3 Avg')
plt.xlabel('Average of All Values')
plt.xlim(0, 400)
plt.ylabel('Average of Top 3 Values')
plt.ylim(0, 400)
plt.title('Average of All Values vs. Average of Top 3 Values')
plt.legend()
plt.grid(True)
plt.show()
