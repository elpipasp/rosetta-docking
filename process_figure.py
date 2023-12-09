import graphviz

# Create a new directed graph with the desired layout direction
graph = graphviz.Digraph('Process', format='png', engine='dot', graph_attr={'rankdir': 'TB'})

# Define the main steps with numbers next to each box
graph.node('1', '1\nInitial configuration\n~10 Å distance', color='#F4DDE6', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('2', '2\nForm membrane environment', color='#F4DDE6', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('3', '3\nMinimisation of initial configuration\nSelect the best scoring one as input for the next step', color='#F4DDE6', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('4', '4\nPrepack\nGenerate 10 structures and select the best scoring as input for the next step', color='#F4DDE6', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('5', '5\nGenerate template of random configurations around the binding pocket\nGenerate 100 structures\nSelect the 15 best scoring ones as inputs for docking', color='#F4DDE6', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('6', '6\nFlexPepDock\nGenerate 1,000 poses per template (total 15,000)', color='#D3E0EA', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('7', '7\nEnergy-based clustering\nInterfaceAnalyzer\nSelect 5 poses from the most populated and best scoring cluster as inputs for the next step', color='#D3E0EA', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('8', '8\nPrepack the 5 input structures\nGenerate 10 structures per input\nSelect the best scoring ones', color='#D3E0EA', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('9', '9\nGenerate 1,000 FlexPepDocks per input (total 5,000 poses)', color='#CADFCE', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('10', '10\nEnergy-based clustering\nInterfaceAnalyzer\nSelect the 3-best scoring models of the best scoring cluster\nMinimise the 3 models\nGenerate 100 minimised structures per input\nSelect the best scoring poses\nInterfaceAnalyzer', color='#CADFCE', style='filled', shape='box3d', fontname='Arial', fontsize='14')
graph.node('11', '11\nMD simulations of best Rosetta FlexPepDock models', color='#CADFCE', style='filled', shape='box3d', fontname='Arial', fontsize='14')

# Define the main steps with arrows
graph.edge('1', '2')
graph.edge('2', '3')
graph.edge('3', '4')
graph.edge('4', '5')
graph.edge('5', '6')

# Link processes 6 to 7 horizontally
graph.edge('6', '7')

# Create a subgraph for processes 8, 9, 10 above 7
with graph.subgraph() as s:
    s.attr(rank='same')  # Align processes 6, 7, 8, 9, 10 horizontally
    s.node('8', '8\nPrepack the 5 input structures\nGenerate 10 structures per input\nSelect the best scoring ones', color='#D3E0EA', style='filled', shape='box3d', fontname='Arial', fontsize='14')
    s.node('9', '9\nGenerate 1,000 FlexPepDocks for each of 5 inputs (total 5,000 poses)', color='#CADFCE', style='filled', shape='box3d', fontname='Arial', fontsize='14')
    s.node('10', '10\nEnergy-based clustering\nInterfaceAnalyzer\nSelect the best scoring 3 models out of the best scoring clusters\nMinimise the 3 models\nGenerate 100 structures for each\nSelect the best scoring poses\nInterfaceAnalyzer', color='#CADFCE', style='filled', shape='box3d', fontname='Arial', fontsize='14')

# Link process 7 to 8 horizontally
graph.edge('7', '8')

# Link process 8 to 9 horizontally
graph.edge('8', '9')

# Link process 9 to 10 horizontally
graph.edge('9', '10')

# Link process 10 to 11 horizontally
graph.edge('10', '11')

# Render the graph to a file
graph.render(filename='process_flowchart', cleanup=True, format='png')

print("Process flowchart generated successfully.")
