#to get names for tcl
import os

def create_txt_file_with_suffix(directory_path='./', prefix='c.5.', extension='.pdb'):
    #find all files with the specified prefix and extension in the directory
    pdb_files = [file for file in os.listdir(directory_path) if file.startswith(prefix) and file.endswith(extension)]

    #create a text file and write the PDB file names in one column with double quotes
    with open('pdb_files_with_suffix.txt', 'w') as file:
        for pdb_file in pdb_files:
            file.write(f'"{pdb_file}"\n')

    print(f'Text file "pdb_files_with_suffix.txt" created with {len(pdb_files)} file(s).')

current_directory = os.getcwd()
create_txt_file_with_suffix(current_directory, prefix='c.5.', extension='.pdb')
