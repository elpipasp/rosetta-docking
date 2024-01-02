#from best scoring structures based on dG_separated score and contacts ranking, find the best candidates


import pandas as pd

def read_energy_file(filename):
    # Read the energy file, skipping the initial lines
    df_energy = pd.read_csv(filename, sep='\s+', skiprows=2)
    # Extract the 'dG_separated' (index 6) and 'description' (index 44) columns
    df_energy = df_energy.iloc[:, [6, 44]]
    # Rename the columns for clarity
    df_energy.columns = ['dG_separated', 'file_name']
    return df_energy

def read_ranking_file(filename):
    # Read the ranking file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract file names and number of contacts
    data = []
    for line in lines:
        parts = line.split(':')
        file_name = parts[0].strip('.pdb')  # Remove '.pdb' extension
        contacts = int(parts[1].split()[0])
        data.append({'file_name': file_name, 'contacts': contacts})

    return pd.DataFrame(data)

# Read and process the files
df_energy = read_energy_file('30_15_gr_seperated.txt')
df_ranking = read_ranking_file('pdb_ranking.txt')

# Merge the dataframes on the file names
df_merged = pd.merge(df_energy, df_ranking, on='file_name', how='inner')

# Sort by dG_separated (ascending) and contacts (descending)
df_sorted = df_merged.sort_values(by=['dG_separated', 'contacts'], ascending=[True, False])

# Output the top structures
top_structures = df_sorted.head(100)  # Adjust the number as needed

# Write the results to an output file
output_file = 'top_ranked_candidates.txt'
top_structures.to_csv(output_file, index=False, sep='\t')

print(f"Top structures have been saved to {output_file}.")
