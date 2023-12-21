import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data and extract the specified column
def load_data(file_path, column_index):
    data = pd.read_csv(file_path, skiprows=1, delim_whitespace=True)
    return data[data.columns[column_index]]

# File paths and labels
file_names = [
    'score_cluster_15.dat',
    'score_cluster_1.dat',
    'score_cluster_238.dat',
    'score_cluster_30.dat',
    'score_cluster_59.dat',
    'score_cluster_12.dat',
    'score_cluster_120.dat',
    'score_cluster_31.dat',
    'score_cluster_366.dat',
    'score_cluster_18.dat',
    'score_cluster_29.dat',
    'score_cluster_44.dat',
    'score_cluster_10.dat',
    'score_cluster_153.dat',
    'score_cluster_442.dat',
    'score_cluster_7.dat',
    'score_cluster_48.dat',
    'score_cluster_34.dat',
    'score_cluster_58.dat',
    'score_cluster_53.dat',
    'score_cluster_378.dat',
    'score_cluster_51.dat',
    'score_cluster_17.dat',
    'score_cluster_56.dat',
    'score_cluster_2.dat',
    'score_cluster_8.dat',
    'score_cluster_134.dat',
    'score_cluster_42.dat',
    'score_cluster_63.dat',
    'score_cluster_430.dat',
    'score_cluster_193.dat',
    'score_cluster_312.dat',
    'score_cluster_4.dat',
    'score_cluster_393.dat',
    'score_cluster_52.dat',
    'score_cluster_323.dat',
    'score_cluster_351.dat',
    'score_cluster_54.dat',
    'score_cluster_106.dat',
    'score_cluster_509.dat',
    'score_cluster_90.dat',
    'score_cluster_6.dat',
    'score_cluster_310.dat',
]

labels = [name.split('_')[-1].split('.')[0] for name in file_names]

# Create a subplot with reduced white space
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 15), sharex=True, gridspec_kw={'hspace': 0.05})

# Load data and create a DataFrame
def plot_data(ax, column_index, ylabel, is_first_plot=False, is_last_plot=False, label_text=''):
    combined_data = pd.DataFrame({label: load_data(file_name, column_index) for file_name, label in zip(file_names, labels)})
    combined_data.columns = [label.replace('.dat', '') for label in combined_data.columns]

    # Set color palette for violin plot
    label_colors = {
        '15': 'forestgreen',
        '238': 'forestgreen',
        '30': 'forestgreen',
        '31': 'forestgreen',
        '366': 'forestgreen',
        '29': 'forestgreen',
        '44': 'forestgreen',
        '442': 'forestgreen',
        '7': 'forestgreen',
        '48': 'forestgreen',
        '34': 'forestgreen',
        '58': 'forestgreen',
        '53': 'forestgreen',
        '51': 'forestgreen',
        '56': 'forestgreen',
        '134': 'forestgreen',
        '430': 'forestgreen',
        '393': 'forestgreen',
        '323': 'forestgreen',
        '351': 'forestgreen',
        '54': 'forestgreen',
        '509': 'forestgreen',
        '310': 'forestgreen',
        '2': 'grey',
        '193': 'grey',
        '52': 'grey',
        '106': 'grey',
        '90': 'grey',
        '1': 'crimson',
        '59': 'crimson',
        '12': 'crimson',
        '120': 'crimson',
        '18': 'crimson',
        '10': 'crimson',
        '153': 'crimson',
        '53': 'crimson',
        '17': 'crimson',
        '8': 'crimson',
        '42': 'crimson',
        '63': 'crimson',
        '312': 'crimson',
        '4': 'crimson',
        '6': 'crimson',
        '378': 'crimson',
    }

    # Map label colors to the corresponding labels in the DataFrame
    label_colors_mapping = [label_colors[label] for label in combined_data.columns]

    # Plot violin plot with custom colors
    sns.violinplot(data=combined_data, palette=label_colors_mapping, ax=ax)

    # Plot strip plot with the same custom colors
    sns.stripplot(data=combined_data, jitter=True, marker='o', palette=label_colors_mapping, alpha=0.7, ax=ax)

    # Customize axis labels and ticks
    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold', labelpad=5)

    # Increase font size of tick labels for both x and y axes
    ax.tick_params(axis='both', which='major', labelsize=10)

    if is_first_plot:
        # Add upper x-axis with the number of data points in each cluster
        upper_data_points = combined_data.count()
        upper_labels = upper_data_points.tolist()
        upper_ax = ax.twiny()
        upper_ax.set_xlim(ax.get_xlim())
        upper_ax.set_xticks([tick for tick in ax.get_xticks()])
        upper_ax.set_xticklabels([f"{label}" for label in upper_labels], fontsize=10, ha='center', rotation=0)  # Move labels to the right
        upper_ax.set_xlabel("Population", fontsize=16, fontweight='bold', labelpad=10)
        upper_ax.set_xlim(ax.get_xlim())  # Set the upper x-axis limits to match the lower x-axis

    # Remove x ticks in the first and second plots
    if not is_last_plot:
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    for tick in ax.get_xticklabels():
        tick.set_rotation(0)

    # Add grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Add label to lower right corner
    ax.text(0.999, 0.009, label_text, transform=ax.transAxes, fontsize=18, fontweight='bold', ha='right', va='bottom')

# Plot the data for each subplot
plot_data(ax1, 1, "Total Score (REU)", is_first_plot=True, label_text='A')
plot_data(ax2, 6, "ΔG Binding (REU)", label_text='B')
plot_data(ax3, 8, "ΔSASA (Å²)", is_last_plot=True, label_text='C')

# Add lower x-axis label
ax3.set_xlabel("Cluster", fontsize=16, fontweight='bold', labelpad=5)

# Save the plot
plt.tight_layout()
plt.show()
