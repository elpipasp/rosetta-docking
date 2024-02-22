#!/bin/bash
# command to do dockings of template input structures
#set the full path to the Rosetta database
DATABASE_PATH="/opt/software/rosetta/2021.16.61629/main/database/"

#set the pattern for input PDB files
INPUT_PATTERN="tem_*.pdb"

#specify the options file
OPTIONS_FILE="options_flex.inp"

#iterate over the list of input PDB files
for pdb_file in $INPUT_PATTERN
do
    # Set the input PDB file
    INPUT_PDB="-s $pdb_file"

    #set the output prefix based on the input file name
    OUTPUT_PREFIX="-out:prefix flex_$(basename $pdb_file .pdb)"

    #run the FlexPepDocking command
    /opt/software/rosetta/2021.16.61629/main/source/bin/FlexPepDocking.static.linuxgccrelease $INPUT_PDB $OUTPUT_PREFIX @$OPTIONS_FILE > dock.log
done
