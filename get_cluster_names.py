#create a file containing path of clustered pdb files. 
import os

def create_txt_file_with_suffix(directory_path='./', prefix='c.1.', extension='.pdb'):
    pdb_files = [file for file in os.listdir(directory_path) if file.startswith(prefix) and file.endswith(extension)]

    with open('pdb_files_with_suffix.txt', 'w') as file:
        for pdb_file in pdb_files:
            file.write(f'"{pdb_file}"\n')

    print(f'Text file "pdb_files_with_suffix.txt" created with {len(pdb_files)} file(s).')

current_directory = os.getcwd()
create_txt_file_with_suffix(current_directory, prefix='c.1.', extension='.pdb')

#output:

#   "c.1.120.pdb"
#"c.1.120.pdb"
#"c.1.175.pdb"
#"c.1.88.pdb"
#"c.1.101.pdb"
#"c.1.2.pdb"
#"c.1.180.pdb" etc copy this file into superimpose_.tcl to get superimposed structures on VMD
