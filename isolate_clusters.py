#isolate structures of best clusters that satisfly the conditions <-620, <0
import os
import pandas as pd
import shutil

def get_pdb_files_to_copy(data_file, total_score_index, dg_separated_index, pdb_file_index):
    data = pd.read_csv(data_file, delim_whitespace=True)
    filtered_data = data[(data.iloc[:, total_score_index] < -620) & (data.iloc[:, dg_separated_index] < 0)]
    pdb_files = [f"{filename}.pdb" for filename in filtered_data.iloc[:, pdb_file_index]]
    return pdb_files

def copy_pdb_files(data_files, source_directory, destination_directory, total_score_index, dg_separated_index, pdb_file_index):
    count_dict = {}
    for data_file in data_files:
        pdb_files = get_pdb_files_to_copy(os.path.join(source_directory, data_file), total_score_index, dg_separated_index, pdb_file_index)
        count_dict[data_file] = len(pdb_files)

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        for file in pdb_files:
            source_file = os.path.join(source_directory, file)
            destination_file = os.path.join(destination_directory, file)
            print(f"Attempting to copy: {source_file}")  # Debugging print
            if os.path.exists(source_file):
                shutil.copy(source_file, destination_file)
            else:
                print(f"File not found: {source_file}")

    for data_file, count in count_dict.items():
        print(f"Copied {count} structures from {data_file}")

data_files = ['c2.txt', 'c4.txt', 'c1.txt', 'c5.txt']
source_directory = '.' 
destination_directory = 'best_clusters'
total_score_index = 1
dg_separated_index = 6
pdb_file_index = 44

copy_pdb_files(data_files, source_directory, destination_directory, total_score_index, dg_separated_index, pdb_file_index)
