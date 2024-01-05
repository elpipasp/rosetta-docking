import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import defaultdict

def extract_residue_number(parts, index):
    try:
        return int(parts[index])
    except ValueError:
        return None

# Parameters
contact_files = ['contacts_c2.txt', 'contacts_c4.txt', 'contacts_c1.txt', 'contacts_c5.txt']
titles = {'contacts_c2.txt': 'Cluster 2', 'contacts_c4.txt': 'Cluster 4',
          'contacts_c1.txt': 'Cluster 1', 'contacts_c5.txt': 'Cluster 5'}
bold_residues = {23, 38, 174, 178, 280, 283, 284, 286, 290, 306, 323, 302, 102, 309, 308, 305}

cbar_ticks = {
    'contacts_c2.txt': [1, 2, 3, 4, 5],
    'contacts_c4.txt': [1, 200, 400, 700, 948],
    'contacts_c1.txt': [1, 150, 150, 350, 517],
    'contacts_c5.txt': [1, 100, 200, 300, 400, 500, 660]
}

title_colors = {
    'contacts_c2.txt': 'grey',
    'contacts_c4.txt': 'cyan',
    'contacts_c1.txt': 'forestgreen',
    'contacts_c5.txt': 'magenta'
}
# Initialize dictionary for contact frequency
contact_frequency = {cluster: defaultdict(lambda: defaultdict(int)) for cluster in contact_files}
peptide_residues_in_contact = defaultdict(set)
receptor_residues_in_contact = defaultdict(set)

# Process contact files
for cluster_file in contact_files:
    with open(cluster_file, 'r') as file:
        for line in file:
            if line.startswith("Contacts in"):
                continue
            parts = line.split()
            if parts:
                peptide_residue = extract_residue_number(parts, 1)
                receptor_residue = extract_residue_number(parts, 5)
                if peptide_residue and receptor_residue:
                    peptide_residues_in_contact[cluster_file].add(peptide_residue)
                    receptor_residues_in_contact[cluster_file].add(receptor_residue)
                    contact_frequency[cluster_file][peptide_residue][receptor_residue] += 1

# Create matrices for heatmaps
heatmap_matrices = {}
for cluster_file in contact_files:
    peptide_residues_sorted = sorted(peptide_residues_in_contact[cluster_file])
    receptor_residues_sorted = sorted(receptor_residues_in_contact[cluster_file])
    matrix = np.zeros((len(peptide_residues_sorted), len(receptor_residues_sorted)))
    for i, pep_res in enumerate(peptide_residues_sorted):
        for j, rec_res in enumerate(receptor_residues_sorted):
            matrix[i, j] = contact_frequency[cluster_file][pep_res][rec_res]
    heatmap_matrices[cluster_file] = (matrix, peptide_residues_sorted, receptor_residues_sorted)

# Plotting with specific frequency bar ticks
fig = plt.figure(figsize=(20, 20))  # Large figure size
for idx, (cluster_file, (matrix, peptide_residues, receptor_residues)) in enumerate(heatmap_matrices.items()):
    ax = fig.add_subplot(2, 2, idx+1)
    mask = matrix == 0
    heatmap = sns.heatmap(matrix, ax=ax, cmap='viridis', annot=False, mask=mask, linewidths=.5, linecolor='black', cbar_kws={'label': 'Frequency'})
    ax.set_title(titles[cluster_file], fontweight='bold', fontsize=18)
    ax.set_ylabel('GnRH', fontweight='bold', fontsize=18) 
    ax.set_xlabel('GnRH1R', fontweight='bold', fontsize=18)
    ax.set_xticks(np.arange(len(receptor_residues)) + 0.5)
    ax.set_yticks(np.arange(len(peptide_residues)) + 0.5)

    # Setting x-tick labels with bold residues
    xtick_labels = [f'$\\mathbf{{{residue}}}$' if residue in bold_residues else str(residue) for residue in receptor_residues]
    ax.set_xticklabels(xtick_labels, rotation=90, fontsize=12)
    ax.set_yticklabels(peptide_residues, fontsize=12)
    cluster_title = titles[cluster_file]
    ax.set_title(cluster_title, fontweight='bold', fontsize=18, color=title_colors[cluster_file])

    # Adjusting the colorbar to have specific ticks
    cbar = ax.collections[0].colorbar
    cbar.set_ticks(cbar_ticks[cluster_file])  # Set custom ticks for each plot
    cbar.set_ticklabels([str(tick) for tick in cbar_ticks[cluster_file]])  # Set custom tick labels
    cbar.ax.set_ylabel('Frequency', fontweight='bold', fontsize=16)

# Removing the extra box
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(False)

plt.subplots_adjust(hspace=0.5, wspace=0.1)
plt.show()
