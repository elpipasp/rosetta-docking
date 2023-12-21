import os

def count_files_in_clusters(directory_path='./', num_clusters=84):
    cluster_sizes = {}

    for cluster_number in range(1, num_clusters + 1):
        cluster_pattern = f'c.{cluster_number}.'
        cluster_files = [file for file in os.listdir(directory_path) if cluster_pattern in file]
        file_count = len(cluster_files)
        cluster_sizes[cluster_number] = file_count

    # Sort clusters by file count in descending order
    sorted_clusters = sorted(cluster_sizes.items(), key=lambda x: x[1], reverse=True)

    with open('cluster_size.txt', 'w') as output_file:
        for cluster_number, file_count in sorted_clusters:
            output_file.write(f'Cluster {cluster_number}: {file_count} files\n')

    print('Cluster sizes written to "cluster_size.txt".')

# Example usage
current_directory = os.getcwd()  # Get the current working directory
count_files_in_clusters(current_directory, num_clusters=84)
