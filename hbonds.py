import os
import numpy as np
import matplotlib.pyplot as plt
from Bio.PDB import PDBParser, NeighborSearch
import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable

parser = PDBParser(QUIET=True)

def is_hbond_donor(atom):
    return 'H' in atom.get_id()

def is_hbond_acceptor(atom):
    return atom.element in ('O', 'N')

def find_hbonds_between_chains(chain_donor, chain_acceptor):
    ns = NeighborSearch(list(chain_acceptor.get_atoms()))
    hbonds = set()  # Use a set to store unique hydrogen bonds
    for residue in chain_donor:
        for donor_atom in residue:
            if is_hbond_donor(donor_atom):
                acceptor_atoms = ns.search(donor_atom.coord, 3.5)
                for acceptor_atom in acceptor_atoms:
                    if is_hbond_acceptor(acceptor_atom):
                        hbonds.add((residue.get_id()[1], acceptor_atom.get_parent().get_id()[1]))
    return list(hbonds)

def plot_hbond_density(hbonds, title, ax, title_color, max_freq, bold_residues, fontweight='bold', fontsize=20):
    if not hbonds:
        print(f"No hydrogen bonds found for {title}")
        return

    num_ticks = 5

    cbar_ticks = {
        'Cluster 2': [1, 3, 5, 7, 10],
        'Cluster 4': [1, 250, 550, 800, 1093],
        'Cluster 1': [1, 200, 400, 600, 838],
        'Cluster 5': [1, 200, 450, 700, 947]
    }

    donors, acceptors = zip(*hbonds)
    donor_residues = sorted(set(donors))
    acceptor_residues = sorted(set(acceptors))
    hbond_freq = {}
    for d, a in hbonds:
        hbond_freq[(d, a)] = hbond_freq.get((d, a), 0) + 1

    matrix = np.full((len(acceptor_residues), len(donor_residues)), np.nan)
    for (d, a), freq in hbond_freq.items():
        matrix[acceptor_residues.index(a), donor_residues.index(d)] = freq
    
    cmap = plt.cm.viridis.copy()
    cmap.set_bad(color='white')
    cax_plot = ax.matshow(matrix, cmap=cmap, origin='lower', vmin=1, vmax=max_freq, aspect='auto')
    ax.set_xticks(range(len(donor_residues)))
    ax.set_yticks(range(len(acceptor_residues)))
    x_tick_labels = [f'{x:.0f}' for x in donor_residues]
    
    for i, label in enumerate(x_tick_labels):
        if int(label) in bold_residues:
            ax.xaxis.get_major_ticks()[i].label1.set_fontweight('bold')

    ax.set_xticklabels(x_tick_labels, fontsize=9)
    ax.set_yticklabels([f'{y:.0f}' for y in acceptor_residues], fontsize=10)
    ax.tick_params(axis='x', which='major', length=4, labelrotation=90)
    ax.tick_params(axis='y', which='major', length=4)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_position('bottom')
    ax.tick_params(axis='x', which='minor', bottom=False, length=6, labelrotation=90)
    ax.set_ylabel('GnRH', fontweight='bold', fontsize=14, labelpad=5)
    ax.yaxis.set_label_position('left')
    ax.tick_params(axis='y', which='minor', left=False, length=4)
    ax.set_xticks(np.arange(-.5, len(donor_residues), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(acceptor_residues), 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2.5%", pad=0.05)
    cbar_ticks_plot = cbar_ticks.get(title, [1, 2, 3, 4, 5])  # Get custom colorbar ticks for this plot
    cbar = plt.colorbar(cax_plot, cax=cax, aspect=40, pad=0.04, ticks=cbar_ticks_plot)
    cbar.set_label('Population', fontweight='bold', fontsize=12)
    cbar.set_ticklabels([str(int(tick)) for tick in cbar_ticks_plot])
    ax.set_xlabel('GnRH1R', fontweight='bold', fontsize=14, labelpad=5)
    ax.set_title(title, fontsize=fontsize, fontweight=fontweight, color=title_color, y=0.92, pad=20)

def calculate_max_frequency(pdb_files):
    return len(pdb_files)

pdb_files_path = '.' 
cluster_paths = ['*c.2.*pdb', '*c.4.*pdb', '*c.1.*pdb', '*c.5.*pdb']
cluster_titles = ['Cluster 2', 'Cluster 4', 'Cluster 1', 'Cluster 5']


title_colors = {
    'Cluster 2': 'grey',
    'Cluster 4': 'cyan',
    'Cluster 1': 'forestgreen',
    'Cluster 5': 'magenta'
}

bold_residues = {23, 38, 174, 178, 280, 283, 284, 286, 290, 306, 323, 302, 102, 308, 309, 98}

fig, axes = plt.subplots(2, 2, figsize=(20, 20))

for cluster_path, ax, cluster_title in zip(cluster_paths, axes.flatten(), cluster_titles):
    pdb_files = glob.glob(os.path.join(pdb_files_path, cluster_path))
    cluster_hbonds = []

    for pdb_file in pdb_files:
        structure = parser.get_structure('cluster', pdb_file)
        chain_A = structure[0]['A']
        chain_P = structure[0]['P']
        hbonds = find_hbonds_between_chains(chain_A, chain_P)
        cluster_hbonds.extend(hbonds)

    title_color = title_colors.get(cluster_title, 'black')  # Get the title color based on the cluster title
    max_freq = calculate_max_frequency(pdb_files)  # Calculate the maximum frequency for this cluster


    plot_hbond_density(cluster_hbonds, cluster_title, ax, title_color, max_freq, bold_residues, fontweight='bold', fontsize=14)
plt.subplots_adjust(hspace=0.5, wspace=0.2)
plt.show()
