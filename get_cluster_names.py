#create a file containing path of clustered pdb files. 
import os

def create_txt_file_with_suffix(directory_path='./', prefix='c.1.', extension='.pdb'):
    # Find all files with the specified prefix and extension in the directory
    pdb_files = [file for file in os.listdir(directory_path) if file.startswith(prefix) and file.endswith(extension)]

    # Create a text file and write the PDB file names in one column with double quotes
    with open('pdb_files_with_suffix.txt', 'w') as file:
        for pdb_file in pdb_files:
            file.write(f'"{pdb_file}"\n')

    print(f'Text file "pdb_files_with_suffix.txt" created with {len(pdb_files)} file(s).')

# Example usage
current_directory = os.getcwd()  # Get the current working directory
create_txt_file_with_suffix(current_directory, prefix='c.1.', extension='.pdb')

#output:

#   "c.1.120.pdb"
#"c.1.120.pdb"
#"c.1.175.pdb"
#"c.1.88.pdb"
#"c.1.101.pdb"
#"c.1.2.pdb"
#"c.1.180.pdb" etc copy this file into superimpose_.tcl to get superimposed structures on VMD
