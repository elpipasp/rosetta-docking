#copies the pdb files with the most literature contacts and ranks them while pasting them in new directory
import os
import shutil

# Target residue numbers
target_residues = {23, 38, 178, 174, 280, 283, 284, 286, 290, 306, 323, 302, 309, 308, 305, 102}
contact_files = ['contacts_c2.txt', 'contacts_c4.txt', 'contacts_c1.txt', 'contacts_c5.txt']
pdb_contact_count = {}

# Process contact files
for file_name in contact_files:
    with open(file_name, 'r') as file:
        current_pdb = ''
        for line in file:
            if line.startswith("Contacts in"):
                current_pdb = line.split()[2].strip(':')
            else:
                parts = line.split()
                if parts and int(parts[5]) in target_residues:
                    pdb_contact_count[current_pdb] = pdb_contact_count.get(current_pdb, 0) + 1

# Sort PDB files by the number of contacts
sorted_pdbs = sorted(pdb_contact_count.items(), key=lambda x: x[1], reverse=True)

# Create candidates directory
candidates_dir = 'candidates'
os.makedirs(candidates_dir, exist_ok=True)

# Move top PDB files to candidates directory and write to a ranking file
ranking_file = 'pdb_ranking.txt'
with open(ranking_file, 'w') as rank_file:
    for pdb, count in sorted_pdbs:
        shutil.copy(pdb, os.path.join(candidates_dir, pdb))
        rank_file.write(f"{pdb}: {count} contacts\n")

print(f"PDB files ranked and copied to {candidates_dir}. Ranking saved in {ranking_file}.")
