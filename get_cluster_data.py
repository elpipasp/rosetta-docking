import re
from collections import defaultdict

input_file_path = 'cluster_InterfaceAnalyzer.csv'
cluster_pattern = re.compile(r'c\.(\d+)\.(\d+)')
cluster_data = defaultdict(list)

with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

#extract and store the header line
header_line = lines[1]
header_line = header_line.replace('\n', '')

current_cluster = None
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

for cluster_number, data in cluster_data.items():
    output_file_path = f'c{cluster_number}.dat'
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(data)
    print(f'Data for Cluster {cluster_number} written to {output_file_path}')
