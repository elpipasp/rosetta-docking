import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

file_path = '/users/nkb19202/ROSETTA_af/flexpepdock/template/cluster_2/cl_tem/cluster/best_clusters/renumber/best_contacts/candidates/2top_ranked_candidates.txt'
data = pd.read_csv(file_path, sep='\t')

fig, ax = plt.subplots()

def assign_color(x):
    if 'c.1.' in x:
        return 'green'
    elif 'c.4.' in x:
        return 'cyan'
    elif 'c.5.' in x:
        return 'magenta'
    else:
        return 'gray'  

colors = data['file_name'].apply(assign_color)

ax.bar(data['file_name'], data['dG_separated'], color=colors, alpha=0.7)

ax.bar(data['file_name'], data['contacts'], color='gray', alpha=0.5)

ax.set_xlabel('Pose', fontsize=12, fontweight='bold')
ax.set_ylabel('ΔG Binding (REU)                                        Contacts', fontsize=10, fontweight='bold')
plt.title('Candidate selection', fontsize=12, fontweight='bold')
legend_labels = ['Cluster 1', 'Cluster 4', 'Cluster 5']
legend_colors = ['green', 'cyan', 'magenta']
legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(legend_colors, legend_labels)]
plt.xticks([]) 
plt.yticks([-24, -23, -22, -21, -20, 1, 2, 3, 4, 5]) 
ax.axhline(0, color='black', linewidth=1)
plt.legend(handles=legend_patches, loc='lower right', fontsize=8)
plt.tight_layout()
plt.show()
