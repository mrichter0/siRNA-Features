from pymol import cmd
import matplotlib.pyplot as plt
import sys
import numpy as np
import gc
import os
from multiprocessing import Pool
from tqdm.notebook import tqdm
import csv
cmd.reinitialize()
num_processes = 64

directories = [
    '/data/home/mrichte3/RNASeq/unmod/step4',
    '/data/home/mrichte3/RNASeq/amide/step4',
    '/data/home/mrichte3/RNASeq/gna/step4'
]

# Use a static reference file located in the current directory
ref_file = os.path.join(os.getcwd(), "4f3t.cif")

files = []

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(('.cif', '.gro', '.pdb')):
            comp_file = os.path.join(directory, filename)
            files.append((ref_file, comp_file))

combined_index_A = list(range(22, 859))

combined_distances_A = {}

def process_files(file_pair):
    ref_file, comp_file = file_pair
    try:
        cmd.reinitialize()
        cmd.load(ref_file, 'ref')
        cmd.load(comp_file, 'comp')
        if cmd.count_atoms('ref') == 0 or cmd.count_atoms('comp') == 0:
            return None
        cmd.remove('solvent')
        cmd.remove('ref and resn CL')
        cmd.remove('ref and resn NA+')
        cmd.remove('ref and hydrogen')
        cmd.remove('comp and hydrogen')
        cmd.align('comp', 'ref')
        cmd.select('not_C3_ref', 'ref and not byres name C3\'')
        cmd.select('not_C3_comp', 'comp and not byres name C3\'')
        ref_atom_count = cmd.count_atoms('not_C3_ref')
        comp_atom_count = cmd.count_atoms('not_C3_comp')
        if ref_atom_count == 0 or comp_atom_count == 0:
            return None
        distances_A = []
        for i in combined_index_A:
            distance = cmd.distance(f'dist_{i}', f'not_C3_ref and resi {i} and name C', f'not_C3_comp and resi {i} and name C')
            distances_A.append(distance)
        cmd.delete("all") 
        return distances_A
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    combined_distances_A = {}
    failed_files = []
    with Pool(processes=num_processes) as pool:
        results = list(tqdm(pool.imap(process_files, files), total=len(files), desc="Processing files", leave=True))
        gc.collect()

    for index, result in enumerate(results):
        if isinstance(result, str):
            failed_files.append((files[index][1], result))
        elif result:
            comp_name = f"{index}_{files[index][1]}"
            combined_distances_A[comp_name] = result

    if not os.path.exists('rawdata_ref_4f3t'):
        os.makedirs('rawdata_ref_4f3t')

    for directory in directories:
        dir_name = os.path.basename(os.path.dirname(directory))
        output_file = f'rawdata_ref_4f3t/raw_data_{dir_name}.csv'
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['comp_name'] + list(combined_index_A)
            writer.writerow(header)
            for comp_name, distances_A in combined_distances_A.items():
                if directory in comp_name:
                    base_name = comp_name.split('/')[-1].replace('.gro', '')
                    row = [base_name]
                    for index in combined_index_A:
                        if len(distances_A) > combined_index_A.index(index):
                            value = round(distances_A[combined_index_A.index(index)], 4)
                            row.append(value)
                    writer.writerow(row)

    print("Failed to process the following files:")
    for file, error in failed_files:
        print(f"{file}: {error}")

