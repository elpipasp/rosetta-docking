import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from itertools import combinations

def load_data(file_path, column_index, condition_column_name, condition_value, total_score_condition):
    data = pd.read_csv(file_path, delim_whitespace=True)
    filtered_data = data[(data[condition_column_name] < condition_value) & (data.iloc[:, 1] < total_score_condition)]
    return filtered_data.iloc[:, column_index]

def mann_whitney_test_with_effect(data1, data2):
    u_statistic, p_value = mannwhitneyu(data1, data2, alternative='two-sided')
    n1 = len(data1)
    n2 = len(data2)
    effect_size = 1 - (2 * u_statistic) / (n1 * n2)
    return p_value, effect_size

def calculate_p_values_and_effects(file_names, cluster_names, column_index, condition_column_name, condition_value, total_score_condition):
    results = {}
    for i in range(len(file_names)):
        for j in range(i + 1, len(file_names)):
            cluster1 = load_data(file_names[i], column_index, condition_column_name, condition_value, total_score_condition)
            cluster2 = load_data(file_names[j], column_index, condition_column_name, condition_value, total_score_condition)
            p_value, effect_size = mann_whitney_test_with_effect(cluster1, cluster2)
            key = f"{cluster_names[i]} vs {cluster_names[j]}"
            results[key] = {'p_value': p_value, 'effect_size': effect_size}
    return results

def add_p_value_brackets(ax, x1, x2, y, p_value, effect_size, bracket_height=0.02, text_y_offset=0.1, p_fontsize=14, es_fontsize=12, es_offset=0.1):
    bracket_height *= (ax.get_ylim()[1] - ax.get_ylim()[0])
    text_y_offset *= bracket_height
    ax.plot([x1, x1], [y, y + bracket_height], color='black', lw=1.5)
    ax.plot([x1, x2], [y + bracket_height, y + bracket_height], color='black', lw=1.5)
    ax.plot([x2, x2], [y, y + bracket_height], color='black', lw=1.5)

    midpoint = (x1 + x2) / 2

    # P-value above the bracket
    p_text = f"p={p_value:.2e}" if p_value < 0.001 else f"p={p_value:.4f}"
    ax.text(midpoint, y + bracket_height + text_y_offset, p_text, ha='center', va='bottom', color='black', fontsize=p_fontsize)

    # ES value below the horizontal line of the bracket with additional offset
    abs_effect_size = abs(effect_size)
    es_color = 'green' if abs_effect_size >= 0.3 else 'goldenrod' if abs_effect_size >= 0.1 else 'crimson'
    es_text = f"ES={effect_size:.2f}"
    # The ES text is placed lower by subtracting the additional es_offset
    ax.text(midpoint, y + bracket_height - (text_y_offset + es_offset), es_text, ha='center', va='top', color=es_color, fontsize=es_fontsize, fontweight='bold')

file_names = ['c2.txt', 'c4.txt', 'c1.txt', 'c5.txt']
cluster_names = ['2', '4', '1', '5']
violin_width = 6
tick_positions = [5, 15, 25, 35]

fig, axes = plt.subplots(1, 3, figsize=(20, 10), sharex=True, sharey=False, gridspec_kw={'wspace': 0.5})

specified_y_coordinates_plot1 = [-618, -608, -598, -588, -578, -568]
specified_y_coordinates_plot2 = [1, 6, 10, 14, 18, 22]
specified_y_coordinates_plot3 = [1800, 1910, 2020, 2130, 2240, 2350]

for ax, column_index, ylabel, specified_y_coordinates in zip(axes, [1, 6, 9], ["Total Score (REU)", "ΔG Binding (REU)", "ΔSASA (Å²)"], [specified_y_coordinates_plot1, specified_y_coordinates_plot2, specified_y_coordinates_plot3]):
    for file_name, label, position in zip(file_names, cluster_names, tick_positions):
        data = load_data(file_name, column_index, 'dG_separated', 0, -620)
        parts = ax.violinplot([data], positions=[position], widths=violin_width, showmedians=True, showextrema=False)
        color = {'2': 'grey', '4': 'cyan', '1': 'forestgreen', '5': 'magenta'}.get(label, 'black')
        for pc in parts['bodies']:
            pc.set_facecolor(color)
            pc.set_edgecolor('black')
            pc.set_alpha(0.7)
        ax.scatter([position] * len(data), data, color='black', alpha=0.7, s=10)
        parts['cmedians'].set_edgecolor('black')

    ax.set_ylabel(ylabel, fontsize=20, fontweight='bold', labelpad=5)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([int(cluster) for cluster in cluster_names], fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Setting custom y-limits for each plot
    if ylabel == "Total Score (REU)":
        ax.set_ylim(-689, -550)
    elif ylabel == "ΔG Binding (REU)":
        ax.set_ylim(-29, 29)
    elif ylabel == "ΔSASA (Å²)":
        ax.set_ylim(865, 2500)

    upper_ax = ax.twiny()
    upper_ax.set_xlim(ax.get_xlim())
    upper_ax.set_xticks(tick_positions)
    upper_ax.set_xticklabels([f"{load_data(file_name, column_index, 'dG_separated', 0, -620).count()}" for file_name in file_names], fontsize=16, ha='center', rotation=0)
    upper_ax.set_xlabel("Population", fontsize=20, fontweight='bold', labelpad=14)

    results = calculate_p_values_and_effects(file_names, cluster_names, column_index, 'dG_separated', 0, -620)
    for ((cluster1, cluster2), y_coord) in zip(combinations(cluster_names, 2), specified_y_coordinates):
        key = f"{cluster1} vs {cluster2}"
        if key in results:
            p_value = results[key]['p_value']
            effect_size = results[key]['effect_size']
            x1, x2 = tick_positions[cluster_names.index(cluster1)], tick_positions[cluster_names.index(cluster2)]
            add_p_value_brackets(ax, x1, x2, y_coord, p_value, effect_size)
    ax.set_xlabel('Cluster', fontsize=20, fontweight='bold', labelpad=10)  # Add x-axis label to the current
axes[1].set_yticks([0, -5, -10, -15, -20, -25])
axes[0].set_yticks([-620, -640, -660, -680])
axes[2].set_yticks([1800, 1600, 1400, 1200, 1000])
plt.tight_layout()
plt.show()
