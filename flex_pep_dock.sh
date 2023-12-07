#!/bin/bash
# command to do dockings of template input structures
# Set the full path to the Rosetta database
DATABASE_PATH="/opt/software/rosetta/2021.16.61629/main/database/"

# Set the pattern for input PDB files
INPUT_PATTERN="tem_*.pdb"

# Specify the options file
OPTIONS_FILE="options_flex.inp"

# Iterate over the list of input PDB files
for pdb_file in $INPUT_PATTERN
do
    # Set the input PDB file
    INPUT_PDB="-s $pdb_file"

    # Set the output prefix based on the input file name
    OUTPUT_PREFIX="-out:prefix flex_$(basename $pdb_file .pdb)"

    # Run the FlexPepDocking command
    /opt/software/rosetta/2021.16.61629/main/source/bin/FlexPepDocking.static.linuxgccrelease $INPUT_PDB $OUTPUT_PREFIX @$OPTIONS_FILE > dock.log

    # Optionally, you can collect the results or perform additional processing here
done

# all resulting structures will be clusterd 
