import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from itertools import combinations

# Function to load data and extract the specified column with conditions
def load_data(file_path, column_index, condition_column_name, condition_value, total_score_condition):
    data = pd.read_csv(file_path, delim_whitespace=True)
    filtered_data = data[(data[condition_column_name] < condition_value) & (data.iloc[:, 1] < total_score_condition)]
    return filtered_data.iloc[:, column_index]

# Function to perform Mann-Whitney U test
def mann_whitney_test(data1, data2):
    _, p_value = mannwhitneyu(data1, data2, alternative='two-sided')
    return p_value

# Function to calculate p-values for all combinations of clusters
def calculate_p_values(file_names, cluster_names, column_index, condition_column_name, condition_value, total_score_condition):
    p_values = {}
    for i in range(len(file_names)):
        for j in range(i + 1, len(file_names)):
            cluster1 = load_data(file_names[i], column_index, condition_column_name, condition_value, total_score_condition)
            cluster2 = load_data(file_names[j], column_index, condition_column_name, condition_value, total_score_condition)
            p_value = mann_whitney_test(cluster1, cluster2)
            key = f"{cluster_names[i]} vs {cluster_names[j]}"
            p_values[key] = p_value
    return p_values

# Function to add p-value brackets and annotations
def add_p_value_brackets(ax, x1, x2, y, p_value, bracket_height=0.02):
    # Calculate bracket height based on the range of the y-axis
    bracket_height *= (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.plot([x1, x1], [y, y + bracket_height], color='black', lw=1.5)  # Left vertical line
    ax.plot([x1, x2], [y + bracket_height, y + bracket_height], color='black', lw=1.5)  # Horizontal line
    ax.plot([x2, x2], [y, y + bracket_height], color='black', lw=1.5)  # Right vertical line
    p_text = f"{p_value:.2e}" if p_value < 0.2 else f"{p_value:.4f}"
    ax.text((x1 + x2) / 2, y + bracket_height, p_text, ha='center', va='top', color='black')

    # Format p-value text
    p_text = f"{p_value:.2e}" if p_value < 0.2 else f"{p_value:.4f}"
    ax.text((x1 + x2) / 2, y + bracket_height, p_text, ha='center', va='top', color='black')

# Function to plot data with p-values
def plot_data_with_p_values(ax, column_index, ylabel, is_first_plot, is_last_plot, label_text, condition_column_name, condition_value, total_score_condition, y_coordinates):
    y_limits = []
    for file_name, label, position in zip(file_names, cluster_names, tick_positions):
        data = load_data(file_name, column_index, condition_column_name, condition_value, total_score_condition)
        x_position = position
        parts = ax.violinplot([data], positions=[x_position], showmedians=True, showextrema=False)
        color_mapping = {'2': 'forestgreen', '4': 'crimson', '1': 'grey', '5': 'cyan'}
        color = color_mapping.get(label, 'black')
        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_edgecolor('black')
            pc.set_alpha(0.7)
        ax.scatter([x_position] * len(data), data, color='black', alpha=0.7, s=10)
        parts['cmedians'].set_edgecolor('black')
        y_limits.append((data.min(), data.max()))

    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold', labelpad=5)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    ax.text(0.999, 0.009, label_text, transform=ax.transAxes, fontsize=18, fontweight='bold', ha='right', va='bottom')
    if not is_first_plot:
        ax.yaxis.labelpad = 10

    # Set specified y-limits
    min_y, max_y = min(y[0] for y in y_limits), max(y[1] for y in y_limits)
    ax.set_ylim(min_y - 0.1 * abs(max_y - min_y), max_y + 0.1 * abs(max_y - min_y))

    upper_ax = ax.twiny()
    upper_ax.set_xlim(ax.get_xlim())
    upper_ax.set_xticks(tick_positions)
    upper_ax.set_xticklabels([f"{load_data(file_name, column_index, condition_column_name, condition_value, total_score_condition).count()}" for file_name in file_names], fontsize=14, ha='center', rotation=0)
    upper_ax.set_xlabel("Population", fontsize=16, fontweight='bold', labelpad=14)

    # Calculate p-values and add brackets at specified y-coordinates
    p_values = calculate_p_values(file_names, cluster_names, column_index, condition_column_name, condition_value, total_score_condition)
    for ((cluster1, cluster2), y_coord) in zip(combinations(cluster_names, 2), y_coordinates):
        key = f"{cluster1} vs {cluster2}"
        if key in p_values:
            p_value = p_values[key]
            x1, x2 = tick_positions[cluster_names.index(cluster1)], tick_positions[cluster_names.index(cluster2)]
            add_p_value_brackets(ax, x1, x2, y_coord, p_value)
    ax.set_xlabel('Cluster', fontsize=16, fontweight='bold', labelpad=10)  # Add x-axis label to the current subplot

# File names and cluster names
file_names = ['c2.txt', 'c4.txt', 'c1.txt', 'c5.txt']
cluster_names = ['2', '4', '1', '5']
tick_positions = range(len(cluster_names))
tick_labels = [int(cluster) for cluster in cluster_names]

# Create subplots with reduced white space
fig, axes = plt.subplots(1, 3, figsize=(20, 10), sharex=True, sharey=False, gridspec_kw={'wspace': 0.5})

# Specify y-coordinates for each p-value line for each plot
specified_y_coordinates_plot1 = [-618, -614, -610, -606, -602]
specified_y_coordinates_plot2 = [1, 2.5, 4, 5.5, 7]
specified_y_coordinates_plot3 = [1800, 1850, 1900, 1950, 2000]

# Plot data for each subplot with specified y-coordinates for p-values
plot_data_with_p_values(axes[0], 1, "Total Score (REU)", True, False, '', 'dG_separated', 0, -620, specified_y_coordinates_plot1)
axes[0].set_ylim(-695, -595)  # Set y-limits for the first plot
plot_data_with_p_values(axes[1], 6, "ΔG Binding (REU)", False, False, '', 'dG_separated', 0, -620, specified_y_coordinates_plot2)
axes[1].set_ylim(-28, 8)  # Set y-limits for the second plot
plot_data_with_p_values(axes[2], 9, "ΔSASA (Å²)", False, True, '', 'dG_separated', 0, -620, specified_y_coordinates_plot3)
axes[2].set_ylim(900, 2050)  # Set y-limits for the third plot

plt.tight_layout()
plt.show()
