import matplotlib.pyplot as plt
total_scores = [5, 4, 1]
descriptions = ['ROS-1', 'ROS-2', 'ROS-3']
plt.figure(figsize=(4, 6))
bar_width = 0.01  
gap_width = 0.001  
bar_positions = [(i * (bar_width + gap_width)) + (gap_width + bar_width / 2) for i in range(len(total_scores))]
bars = plt.bar(bar_positions, total_scores, width=bar_width, color=['magenta', 'green', 'cyan'])
for bar in bars:
    yval = bar.get_height()
plt.xlim(0, max(bar_positions) + bar_width - 0.004)
plt.ylabel('Contacts', fontsize=14, fontweight='bold')
plt.xticks(bar_positions, descriptions, fontweight='bold', fontsize=14)
plt.xlabel('')
plt.tight_layout()
plt.show()

