import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data and extract the specified column
def load_data(file_path, column_index, condition_column_name, condition_value):
    data = pd.read_csv(file_path, delim_whitespace=True)

    # Apply the condition to filter data
    filtered_data = data[data[condition_column_name] < condition_value]

    return filtered_data[data.columns[column_index]]

# New file names
file_names = [
    'c2.txt',
    'c17.txt',
    'c21.txt',
    'c18.txt',
    'c14.txt',
    'c16.txt',
    'c10.txt',
    'c6.txt',
    'c11.txt',
    'c7.txt',
    'c8.txt',
    'c5.txt',
    'c3.txt',
    'c1.txt',
    'c9.txt',
    'c4.txt',
]

labels = [name.split('.')[0][1:] for name in file_names]

# Create a subplot with reduced white space
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(20, 10), sharex=True, gridspec_kw={'hspace': 0.05})

# Plot the data for each subplot
def plot_data(ax, column_index, ylabel, is_first_plot=False, is_last_plot=False, label_text='', condition_column_name=None, condition_value=None):
    combined_data = pd.DataFrame({label: load_data(file_name, column_index, condition_column_name, condition_value) for file_name, label in zip(file_names, labels)})
    combined_data.columns = [label.replace('.txt', '') for label in combined_data.columns]

    # Set color palette for violin plot
    if is_first_plot:
        palette = ['forestgreen'] * len(combined_data.columns)
    elif is_last_plot:
        palette = ['grey'] * len(combined_data.columns)
    else:
        palette = ['crimson'] * len(combined_data.columns)

    # Plot violin plot with custom colors
    sns.violinplot(data=combined_data, palette=palette, ax=ax)

    # Plot strip plot with the same custom colors
    sns.stripplot(data=combined_data, jitter=True, marker='o', palette=palette, alpha=0.7, ax=ax)

    # Customize axis labels and ticks
    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold', labelpad=5)

    # Increase font size of tick labels for both x and y axes
    ax.tick_params(axis='both', which='major', labelsize=14)

    if is_first_plot:
        # Add upper x-axis with the number of data points in each cluster
        upper_data_points = combined_data.count()
        upper_labels = upper_data_points.tolist()
        upper_ax = ax.twiny()
        upper_ax.set_xlim(ax.get_xlim())
        upper_ax.set_xticks([tick for tick in ax.get_xticks()])
        upper_ax.set_xticklabels([f"{label}" for label in upper_labels], fontsize=14, ha='center', rotation=0)  # Move labels to the right
        upper_ax.set_xlabel("Population", fontsize=16, fontweight='bold', labelpad=14)
        upper_ax.set_xlim(ax.get_xlim())  # Set the upper x-axis limits to match the lower x-axis

    # Remove x ticks in the first and second plots
    if not is_last_plot:
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    for tick in ax.get_xticklabels():
        tick.set_rotation(0)

    # Add grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Add label to the lower right corner
    ax.text(0.999, 0.009, label_text, transform=ax.transAxes, fontsize=18, fontweight='bold', ha='right', va='bottom')

# Plot the data for each subplot with the condition
plot_data(ax1, 1, "Total Score (REU)", is_first_plot=True, is_last_plot=False, condition_column_name='dG_separated', condition_value=0)
plot_data(ax2, 6, "ΔG Binding (REU)", is_first_plot=False, is_last_plot=False, condition_column_name='dG_separated', condition_value=0)
plot_data(ax3, 9, "ΔSASA (Å²)", is_first_plot=False, is_last_plot=True, condition_column_name='dG_separated', condition_value=0)

# Add a lower x-axis label
ax3.set_xlabel("Cluster", fontsize=16, fontweight='bold', labelpad=5)

# Save the plot
plt.tight_layout()
plt.show()
