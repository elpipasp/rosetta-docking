#from best scoring structures based on dG_separated score and contacts ranking, find the best candidates
import pandas as pd

def read_energy_file(filename):
    df_energy = pd.read_csv(filename, sep='\s+', skiprows=2)
    #extract the 'dG_separated' (index 6) and 'description' (index 44) columns
    df_energy = df_energy.iloc[:, [6, 44]]
    df_energy.columns = ['dG_separated', 'file_name']
    return df_energy

def read_ranking_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    #extract file names and number of contacts
    data = []
    for line in lines:
        parts = line.split(':')
        file_name = parts[0].strip('.pdb')  #remove .pdb extension
        contacts = int(parts[1].split()[0])
        data.append({'file_name': file_name, 'contacts': contacts})

    return pd.DataFrame(data)
#read and process the files
df_energy = read_energy_file('30_15_gr_seperated.txt')
df_ranking = read_ranking_file('pdb_ranking.txt')
#merge the dataframes on the file names
df_merged = pd.merge(df_energy, df_ranking, on='file_name', how='inner')
# sort by dG_separated (ascending) and contacts (descending)
df_sorted = df_merged.sort_values(by=['dG_separated', 'contacts'], ascending=[True, False])
# output the top structures
top_structures = df_sorted.head(100)  # Adjust the number as needed
#write output file
output_file = 'top_ranked_candidates.txt'
top_structures.to_csv(output_file, index=False, sep='\t')
print(f"Top structures have been saved to {output_file}.")
