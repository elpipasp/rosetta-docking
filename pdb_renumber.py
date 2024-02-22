#renumbers all pdb files to original numbering and make a new directory for them. 
import os
from Bio import PDB

def renumber_pdb(input_file, output_file, chain_a_start, chain_p_start):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('struct', input_file)

    #step 1: Assign temporary unique identifiers
    temp_id = 10000
    for model in structure:
        for chain in model:
            for residue in chain.get_unpacked_list():
                if residue.id[0] == ' ':
                    residue.id = (' ', temp_id, ' ')
                    temp_id += 1

    #step 2: Assign final residue numbers
    for model in structure:
        for chain in model:
            if chain.id == 'A':
                #renumber Chain A
                residue_num = chain_a_start
                for residue in chain.get_unpacked_list():
                    residue.id = (' ', residue_num, ' ')
                    residue_num += 1
            elif chain.id == 'P':
                #renumber Chain P
                residue_num = chain_p_start
                for residue in chain.get_unpacked_list():
                    residue.id = (' ', residue_num, ' ')
                    residue_num += 1

    io = PDB.PDBIO()
    io.set_structure(structure)
    io.save(output_file)

source_directory = '.' 
destination_directory = 'renumber'
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

for file in os.listdir(source_directory):
    if file.endswith(".pdb") and "c." in file:
        input_file = os.path.join(source_directory, file)
        output_file = os.path.join(destination_directory, file)
        renumber_pdb(input_file, output_file, chain_a_start=12, chain_p_start=1)

print("Renumbering complete.")
