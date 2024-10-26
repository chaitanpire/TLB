import os
import re
import csv

def extract_cumulative_ipc(file_path):
    """Extracts the cumulative IPC from the text file."""
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'cumulative IPC: (\d+\.\d+)', line)
            if match:
                return float(match.group(1))
    return None

def process_srrip_directory(directory):
    """Processes the SRRIP directory to collect cumulative IPC values."""
    results = {}
    for root, _, files in os.walk(directory):
        benchmark_name = os.path.basename(root)
        if benchmark_name not in results:
            results[benchmark_name] = {'SRRIP IPC': None, 'SRRIP_max IPC': None, 'SRRIP_min IPC': None}

        for file in files:
            file_path = os.path.join(root, file)
            if file == 'srrip.txt':
                results[benchmark_name]['SRRIP IPC'] = extract_cumulative_ipc(file_path)
            elif file == 'srrip_cost_aware_max.txt':
                results[benchmark_name]['SRRIP_max IPC'] = extract_cumulative_ipc(file_path)
            elif file == 'srrip_cost_aware_min.txt':
                results[benchmark_name]['SRRIP_min IPC'] = extract_cumulative_ipc(file_path)
    return results

def process_lru_directory(directory, results):
    """Processes the LRU directory to collect cumulative IPC values and updates the results."""
    for root, _, files in os.walk(directory):
        benchmark_name = os.path.basename(root)
        for file in files:
            if file == 'lru.txt':
                file_path = os.path.join(root, file)
                if benchmark_name not in results:
                    results[benchmark_name] = {}
                results[benchmark_name]['LRU IPC'] = extract_cumulative_ipc(file_path)
    return results

def write_to_csv(results, output_file):
    """Writes the results to a CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Benchmark', 'SRRIP IPC', 'SRRIP_max IPC', 'SRRIP_min IPC', 'LRU IPC'])
        for benchmark, ipc_values in results.items():
            row = [
                benchmark,
                ipc_values.get('SRRIP IPC', 'N/A'),
                ipc_values.get('SRRIP_max IPC', 'N/A'),
                ipc_values.get('SRRIP_min IPC', 'N/A'),
                ipc_values.get('LRU IPC', 'N/A')
            ]
            csvwriter.writerow(row)

def main():
    # Define directories
    logs_srrip_dir = 'logs_srrip'
    logs_dir = 'logs'

    # Process directories and gather cumulative IPC data
    srrip_results = process_srrip_directory(logs_srrip_dir)
    all_results = process_lru_directory(logs_dir, srrip_results)

    # Write the results to a CSV file
    output_csv = 'cumulative_ipc_results.csv'
    write_to_csv(all_results, output_csv)
    print(f'Results written to {output_csv}')

if __name__ == '__main__':
    main()
