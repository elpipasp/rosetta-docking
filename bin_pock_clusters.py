import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_center_of_mass_from_pdb(pdb_file, chain_id):
    with open(pdb_file, 'r') as file:
        lines = file.readlines()
    coordinates = []
    for line in lines:
        if line.startswith('ATOM') and line[21] == chain_id:
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            coordinates.append((x, y, z))
    if not coordinates:
        raise ValueError(f"No coordinates found for chain {chain_id} in {pdb_file}")
    center_of_mass = np.mean(coordinates, axis=0)
    return center_of_mass
def get_binding_pocket_coords_and_sizes(pdb_file, chain_id, pocket_residues):
    with open(pdb_file, 'r') as file:
        lines = file.readlines()
    pocket_coords = {}
    for residue_number in pocket_residues:
        residue_atoms = []
        for line in lines:
            if line.startswith('ATOM') and line[21] == chain_id and int(line[22:26].strip()) == residue_number:
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                residue_atoms.append((x, y, z))
        if residue_atoms:
            pocket_coords[residue_number] = np.array(residue_atoms)
    return pocket_coords
def calculate_residue_sizes(pocket_coords):
    residue_sizes = {}
    for residue_number, coords in pocket_coords.items():
        size = np.std(coords, axis=0).mean()
        residue_sizes[residue_number] = size * 100
    return residue_sizes
def plot_binding_pocket(ax, binding_pocket_coords, residue_sizes, pocket_residues_info):
    for residue_number, coords in binding_pocket_coords.items():
        info = next((item for item in pocket_residues_info if item[0] == residue_number), None)
        if info:
            _, color, label = info
            size = residue_sizes[residue_number]
            center = coords.mean(axis=0)
            ax.scatter(*center, color=color, marker='o', s=size)
            ax.text(*center, '  ' + label, color=color, fontsize=9)
def plot_clusters(ax, cluster_files, label, color):
    first_file = True
    for cluster_file in cluster_files:
        cluster_coords = get_center_of_mass_from_pdb(cluster_file, 'P')
        if cluster_coords is not None:
            if first_file:
                ax.scatter(*cluster_coords, marker='o', label=label, color=color, s=50)
                first_file = False
            else:
                ax.scatter(*cluster_coords, marker='o', color=color, s=50)
directory = '/users/nkb19202/ROSETTA_af/flexpepdock/template/cluster_2/cl_tem/cluster/best_clusters/renumber/best_contacts/candidates'
cluster_files = {}
for cluster in [1, 2, 4, 5]:
    cluster_files[cluster] = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.pdb') and f'c.{cluster}.' in file]

pocket_residues_info = [
    (23, 'pink', 'L23'),
    (38, 'gold', 'R38'),
    (174, 'chocolate', 'Q174'),
    (178, 'violet', 'F178'),
    (280, 'gray', 'W280'),
    (283, 'limegreen', 'Y283'),
    (284, 'limegreen', 'Y284'),
    (286, 'pink', 'L286'),
    (290, 'limegreen', 'Y290'),
    (306, 'mediumturquoise', 'H306'),
    (323, 'limegreen', 'Y323'),
    (302, 'red', 'D302'),
    (102, 'goldenrod', 'N102'),
    (121, 'skyblue', 'K121'),
    (98, 'red', 'D98'),
]
pocket_residue_numbers = [residue_info[0] for residue_info in pocket_residues_info]
representative_pdb = '/users/nkb19202/ROSETTA_af/flexpepdock/template/cluster_2/cl_tem/cluster/best_clusters/renumber/best_contacts/candidates/c.5.314.pdb'
binding_pocket_coords = get_binding_pocket_coords_and_sizes(representative_pdb, 'A', pocket_residue_numbers)
residue_sizes = calculate_residue_sizes(binding_pocket_coords)
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
cluster_colors = ['green', 'grey', 'cyan', 'magenta']
cluster_labels = ['Cluster 1', 'Cluster 2', 'Cluster 4', 'Cluster 5']
for idx, (cluster, files) in enumerate(cluster_files.items()):
    plot_clusters(ax, files, cluster_labels[idx], cluster_colors[idx])
plot_binding_pocket(ax, binding_pocket_coords, residue_sizes, pocket_residues_info)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_title('Cluster COM relative to GnRH1R binding pocket')
# Rotate the plot to move x and y-axes to the bottom of the plot
ax.view_init(elev=-205, azim=230)
ax.legend(loc='lower center', bbox_to_anchor=(1, 0.85))
plt.show()
