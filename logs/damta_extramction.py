import os
import re
import csv

def extract_stlb_miss_latency(file_path):
    """Extracts the STLB average miss latency from the text file."""
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'STLB AVERAGE MISS LATENCY:\s+([\d.]+) cycles', line)
            if match:
                return float(match.group(1))
    return None

def process_directory_for_latency(directory, file_pattern):
    """Processes the directory and collects STLB miss latency values for the specified file pattern."""
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file in file_pattern:
                file_path = os.path.join(root, file)
                latency_value = extract_stlb_miss_latency(file_path)
                if latency_value is not None:
                    # Collect the benchmark name and STLB miss latency value
                    benchmark_name = os.path.basename(root)
                    if benchmark_name not in results:
                        results[benchmark_name] = {}
                    results[benchmark_name][file] = latency_value
    return results

def combine_results(srrip_results, lru_results):
    """Combines the SRRIP and LRU results into a single dictionary."""
    combined_results = {}
    for benchmark in set(srrip_results.keys()).union(lru_results.keys()):
        combined_results[benchmark] = {
            'LRU': lru_results.get(benchmark, {}).get('lru.txt', 'N/A'),
            'SRRIP': srrip_results.get(benchmark, {}).get('srrip.txt', 'N/A'),
            'SRRIP_cost_aware_max': srrip_results.get(benchmark, {}).get('srrip_cost_aware_max.txt', 'N/A'),
            'SRRIP_cost_aware_min': srrip_results.get(benchmark, {}).get('srrip_cost_aware_min.txt', 'N/A')
        }
    return combined_results

def write_to_csv(results, output_file):
    """Writes the combined results to a CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header row
        csvwriter.writerow(['Benchmark', 'LRU Miss Latency', 'SRRIP Miss Latency', 
                            'SRRIP_cost_aware_max Miss Latency', 'SRRIP_cost_aware_min Miss Latency'])
        # Write data rows
        for benchmark, latencies in results.items():
            csvwriter.writerow([benchmark, latencies['LRU'], latencies['SRRIP'], 
                                latencies['SRRIP_cost_aware_max'], latencies['SRRIP_cost_aware_min']])

def main():
    # Define directories and file patterns
    logs_srrip_dir = 'logs_srrip'
    logs_dir = 'logs'
    srrip_files = {'srrip.txt', 'srrip_cost_aware_max.txt', 'srrip_cost_aware_min.txt'}
    lru_files = {'lru.txt'}

    # Process directories and gather STLB miss latency data
    srrip_results = process_directory_for_latency(logs_srrip_dir, srrip_files)
    lru_results = process_directory_for_latency(logs_dir, lru_files)

    # Combine the results into a single dictionary
    combined_results = combine_results(srrip_results, lru_results)

    # Write the combined results to a CSV file
    output_csv = 'stlb_miss_latency_results.csv'
    write_to_csv(combined_results, output_csv)
    print(f'Results written to {output_csv}')

if __name__ == '__main__':
    main()
