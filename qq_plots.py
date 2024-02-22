import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv("c1.txt", delim_whitespace=True, header=None, skiprows=1)
#filter data based on the specified conditions.
filtered_data = data[(data.iloc[:, 1] < -620) & (data.iloc[:, 6] < 0)]

columns_info = {
    1: ('Total Score (REU)', 'forestgreen'),
    6: ('ΔG Binding (REU)', 'blue'),
    9: ('ΔSASA (Å²)', 'grey')
}

plt.figure(figsize=(18, 6))
#loop through each column to perform Shapiro-Wilk tests and generate Q-Q plots.
for i, (column_index, (ylabel, color)) in enumerate(columns_info.items(), 1):
    column_data = filtered_data.iloc[:, column_index].dropna().astype(float)
    #perform Shapiro-Wilk Test.
    stat, p_value = stats.shapiro(column_data)
    normality = "Normal Gaussian Distribution" if p_value > 0.05 else "Not normal Gaussian Distribution"
    #create a subplot for each column's Q-Q plot.
    ax = plt.subplot(1, len(columns_info), i)
    stats.probplot(column_data, dist="norm", plot=plt)
    if i == 2: ax.set_title('Cluster 1', fontsize=20, fontweight='bold')
    ax.set_xlabel('Theoretical quantiles', fontsize=20, fontweight='bold', color='black')
    ax.set_ylabel(ylabel, fontsize=20, fontweight='bold', color='black')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    ax.get_lines()[0].set_color(color)
    ax.get_lines()[1].set_color('red')
    if i != 2: ax.set_title('')
    legend_labels = [
        f'{ylabel}',
        'Gaussian Distribution',
        f'p-value = {p_value:.3e}',
        f'Shapiro-Wilk Test: {stat:.3f}',
        normality
    ]
    handle_line = ax.get_lines()[0]
    handle_fit = ax.get_lines()[1]
    custom_handles = [handle_line, handle_fit] + [plt.Line2D([], [], color='none') for _ in range(3)]
    ax.legend(custom_handles, legend_labels, loc='upper left', fontsize=12, frameon=False)
plt.tight_layout()
plt.show()
