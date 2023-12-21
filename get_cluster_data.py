import re
from collections import defaultdict

# Input file path
input_file_path = 'cluster_InterfaceAnalyzer.csv'

# Define a regular expression pattern to extract cluster information from the description column
cluster_pattern = re.compile(r'c\.(\d+)\.(\d+)')

# Dictionary to store data for each cluster
cluster_data = defaultdict(list)

# Read data from the input file
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

# Extract and store the header line
header_line = lines[1]  # Assuming the header line is at index 1
header_line = header_line.replace('\n', '')  # Remove the newline character

# Initialize variables to track the current cluster
current_cluster = None

# Parse data and store it in the dictionary
for line in lines:
    if line.startswith('SCORE:'):
        match = cluster_pattern.search(line)
        if match:
            cluster_number = int(match.group(1))
            # Update the current cluster if it changes
            if current_cluster != cluster_number:
                current_cluster = cluster_number
                # Include the header line in the current cluster
                cluster_data[current_cluster].append(header_line)
            cluster_data[current_cluster].append(line)

# Write data for each cluster to a separate file
for cluster_number, data in cluster_data.items():
    output_file_path = f'c{cluster_number}.dat'
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(data)
    print(f'Data for Cluster {cluster_number} written to {output_file_path}')
