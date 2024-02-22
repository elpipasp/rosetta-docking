import os
from Bio import PDB

def find_contacts(pdb_file, chain_gpcr, chain_peptide, distance_threshold=5.0):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('struct', pdb_file)

    #function to choose the right atom for distance calculation
    def get_representative_atom(residue):
        if residue.get_resname() == 'GLY':
            return residue['CA'] if 'CA' in residue else None
        else:
            return residue['CB'] if 'CB' in residue else residue.get('CA', None)

    #extract representative atoms from GPCR and peptide
    rep_atoms_gpcr = []
    rep_atoms_peptide = []
    for model in structure:
        for chain in model:
            if chain.id == chain_gpcr:
                for residue in chain.get_unpacked_list():
                    if residue.id[0] == ' ':
                        atom = get_representative_atom(residue)
                        if atom:
                            rep_atoms_gpcr.append(atom)
            elif chain.id == chain_peptide:
                for residue in chain.get_unpacked_list():
                    if residue.id[0] == ' ':
                        atom = get_representative_atom(residue)
                        if atom:
                            rep_atoms_peptide.append(atom)

    #check if there are atoms to work with
    if not rep_atoms_gpcr or not rep_atoms_peptide:
        print(f"No valid atoms found in {pdb_file} for contact analysis.")
        return []
        
    #finding contacts
    ns = PDB.NeighborSearch(rep_atoms_gpcr)
    contacts = []
    for atom in rep_atoms_peptide:
        close_atoms = ns.search(atom.get_coord(), distance_threshold)
        for close_atom in close_atoms:
            contacts.append((atom, close_atom))

    return contacts
source_directory = '.'  #current directory
output_filename = 'contacts_c4.txt'
chain_gpcr = 'A'  # replace with the chain ID of the GPCR
chain_peptide = 'P'  #replace with the chain ID of the peptide
#process each PDB file and write contacts to file
with open(output_filename, 'w') as output_file:
    for file in os.listdir(source_directory):
        if file.endswith(".pdb") and "c.4." in file:
            pdb_file = os.path.join(source_directory, file)
            contacts = find_contacts(pdb_file, chain_gpcr, chain_peptide)
            output_file.write(f'Contacts in {file}:\n')
            for atom1, atom2 in contacts:
                res1 = atom1.get_parent()
                res2 = atom2.get_parent()
                output_file.write(f"{res1.get_resname()} {res1.id[1]} {atom1.get_name()} - {res2.get_resname()} {res2.id[1]} {atom2.get_name()}\n")
            output_file.write("\n")
print("Contact analysis complete. Results are in 'contacts_c4.txt'")
