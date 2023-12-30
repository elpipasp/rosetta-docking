import os
import pandas as pd

# List of data files
data_files = [
    'c4.dat',
    'c1.dat',
    'c12.dat',
    'c3.dat',
    'c11.dat',
    'c2.dat',
    'c14.dat',
    'c10.dat',
    'c8.dat',
    'c32.dat',
    'c17.dat',
    'c5.dat',
    'c13.dat',
    'c16.dat',
    'c18.dat',
    'c19.dat',
    'c22.dat',
    'c21.dat',
    'c38.dat',
    'c29.dat',
    'c20.dat',
]

# Process each data file
for file_name in data_files:
    # Read the data file
    data = pd.read_csv(file_name, delim_whitespace=True)

    # Save the data as a space-separated file with a .txt extension
    output_file_path = f'{file_name.split(".")[0]}.txt'
    data.to_csv(output_file_path, sep=' ', index=False)

    print(f'{file_name} converted to {output_file_path}')
