from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.cm import ScalarMappable

def extract_residue_number(part):
    try:
        return int(''.join(filter(str.isdigit, part)))
    except ValueError:
        return None

# Parameters
contact_files = ['contacts_c2.txt', 'contacts_c4.txt', 'contacts_c1.txt', 'contacts_c5.txt']
titles = {'contacts_c2.txt': 'Cluster 2', 'contacts_c4.txt': 'Cluster 4',
          'contacts_c1.txt': 'Cluster 1', 'contacts_c5.txt': 'Cluster 5'}
bold_residues = {23, 38, 174, 178, 280, 283, 284, 286, 290, 306, 323, 302, 102, 308, 309, 98}
title_colors = {
    'contacts_c2.txt': 'grey',
    'contacts_c4.txt': 'cyan',
    'contacts_c1.txt': 'forestgreen',
    'contacts_c5.txt': 'magenta'
}
# Initialize dictionaries
contact_frequency = {cluster: defaultdict(lambda: defaultdict(int)) for cluster in contact_files}
total_pdb_files_per_cluster = {cluster: 0 for cluster in contact_files}
peptide_residues_in_contact = defaultdict(set)
receptor_residues_in_contact = defaultdict(set)

# Process contact files
for cluster_file in contact_files:
    with open(cluster_file, 'r') as file:
        for line in file:
            if line.startswith("Contacts in"):
                total_pdb_files_per_cluster[cluster_file] += 1
                current_pdb = line.strip().split()[2]
                continue
            parts = line.split('-')
            if len(parts) == 2:
                peptide_residue = extract_residue_number(parts[0])
                receptor_residue = extract_residue_number(parts[1])
                if peptide_residue is not None and receptor_residue is not None:
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
    
    # Create a custom colormap for each heatmap
    custom_cmap = mpl.colors.ListedColormap(sns.color_palette("viridis", as_cmap=True)(np.linspace(0, 1, 256)))
    
    # Set 0 frequency values to white in the colormap
    custom_cmap.set_under(color='white')
    
    heatmap = sns.heatmap(matrix, ax=ax, cmap=custom_cmap, annot=False, cbar=False, linewidths=.5, linecolor='black',
                vmin=0, vmax=total_pdb_files_per_cluster[cluster_file], mask=matrix==0)
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
  
    # Annotate boxes with frequency < 100 and rotate by 90 degrees for frequency > 100
    for i in range(len(peptide_residues)):
        for j in range(len(receptor_residues)):
            value = contact_frequency[cluster_file][peptide_residues[i]][receptor_residues[j]]
            if value < 100:
                ax.text(j + 0.5, i + 0.5, str(value), ha='center', va='center', color='white', fontsize=6, fontweight='bold')
            elif value >= 100 and value <= 600:
                ax.text(j + 0.5, i + 0.5, str(value), ha='center', va='center', color='white', fontsize=6, fontweight='bold', rotation=90)
            elif value > 600:
                ax.text(j + 0.5, i + 0.5, str(value), ha='center', va='center', color='white', fontsize=6, fontweight='bold', rotation=90)

    # Removing the extra box
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(False)
    
    # Adding a custom colorbar to each plot
    max_freq = total_pdb_files_per_cluster[cluster_file]
    sm = ScalarMappable(cmap=custom_cmap, norm=plt.Normalize(vmin=0, vmax=max_freq))
    sm.set_array([])
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2.5%", pad=0.04)
    cbar = plt.colorbar(sm, cax=cax)
    cbar.set_label('Frequency', fontweight='bold', fontsize=12)
    cbar.set_ticks([0, max_freq / 4, max_freq / 2, 3 * max_freq / 4, max_freq])
    cbar.set_ticklabels(['0', f'{max_freq // 4}', f'{max_freq // 2}', f'{3 * max_freq // 4}', f'{max_freq}'])

plt.subplots_adjust(hspace=0.5, wspace=0.25)
plt.show()
