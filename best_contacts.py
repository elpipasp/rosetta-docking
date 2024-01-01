#searches for literature contacts in the contacts files. then copies the relevant structures to a new directory.
import os
import shutil

# Target residue numbers
target_residues = {23, 38, 178, 174, 280, 283, 284, 286, 290, 306, 323, 302, 309, 308, 305, 102}

def find_and_copy_relevant_pdbs(contact_files, source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    relevant_pdbs = set()

    for contact_file in contact_files:
        with open(contact_file, 'r') as file:
            current_pdb = None
            for line in file:
                if line.startswith("Contacts in"):
                    # Extracting the filename without adding extra '.pdb'
                    current_pdb = line.split()[2].rstrip(':')
                    if not current_pdb.endswith(".pdb"):
                        current_pdb += ".pdb"
                elif current_pdb and any(str(residue) in line for residue in target_residues):
                    relevant_pdbs.add(current_pdb)

    for pdb in relevant_pdbs:
        source_path = os.path.join(source_dir, pdb)
        dest_path = os.path.join(dest_dir, pdb)
        if os.path.exists(source_path):
            shutil.copy(source_path, dest_path)
        else:
            print(f"File not found: {source_path}")

    return relevant_pdbs

# Parameters
contact_files = ['contacts_c2.txt', 'contacts_c4.txt', 'contacts_c1.txt', 'contacts_c5.txt']
source_directory = '.'  # Current directory
destination_directory = 'best_contacts'

# Process the files
relevant_pdbs = find_and_copy_relevant_pdbs(contact_files, source_directory, destination_directory)
print(f"Copied {len(relevant_pdbs)} PDB files to {destination_directory}")
