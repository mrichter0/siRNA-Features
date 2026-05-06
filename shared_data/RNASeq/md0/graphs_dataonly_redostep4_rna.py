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
output_cifs_dir = '/data/home/mrichte3/RNASeq/output_cifs/'
files = []

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(('.cif', '.gro', '.pdb')):
            file_basename = os.path.splitext(os.path.basename(filename))[0]
            ref_file = os.path.join(output_cifs_dir, f'{file_basename}.cif')
            files.append((ref_file, os.path.join(directory, filename)))

# Process only one file temporarily
# files = files[:10]

combined_index_A = list(range(0, 42))
combined_distances_A = {}

def process_files(file_pair):
    ref_file, comp_file = file_pair
    cmd.reinitialize()
    cmd.load(ref_file, 'ref')
    cmd.load(comp_file, 'comp')
    if cmd.count_atoms('ref') == 0 or cmd.count_atoms('comp') == 0:
        print(f"Error: One of the structures failed to load: {ref_file} or {comp_file}")
        return None

    cmd.remove('solvent')
    cmd.remove('resn CL')
    cmd.remove('resn NA+')
    cmd.remove('hydrogen')

    alignment_rms = cmd.align('comp', 'ref')
    cmd.select("only_C3_ref", "ref and (name C3' or name C3G)")
    cmd.select("only_C3_comp", "comp and (name C3' or name C3G)")
    distances_A = []
    distances_chain_a = []
    distances_chain_b = []
    
    for resi in range(1, 22):
        cmd.select("first_rna_base_ref", f"first (only_C3_ref and resi {resi})")
        cmd.select("first_rna_base_comp", f"first (only_C3_comp and resi {resi})")
        
        if cmd.count_atoms("first_rna_base_ref") > 0 and cmd.count_atoms("first_rna_base_comp") > 0:
            distance_a = cmd.get_distance("first_rna_base_ref", "first_rna_base_comp")
            distances_chain_a.append(distance_a)
        
        cmd.select("first_rna_base_comp_b", f"first (only_C3_comp and resi {resi} and not first_rna_base_comp)")
        cmd.select("first_rna_base_ref_b", f"first (only_C3_ref and resi {resi} and not first_rna_base_ref)")
        
        if cmd.count_atoms("first_rna_base_ref_b") > 0 and cmd.count_atoms("first_rna_base_comp_b") > 0:
            distance_b = cmd.get_distance("first_rna_base_ref_b", "first_rna_base_comp_b")
            distances_chain_b.append(distance_b)
        
    distances_A = distances_chain_a + distances_chain_b
    cmd.delete("all") 
    return distances_A

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

    if not os.path.exists('rawdata_ref_cif'):
        os.makedirs('rawdata_ref_cif')

    for directory in directories:
        dir_name = os.path.basename(os.path.dirname(directory))
        output_file = f'rawdata_ref_cif/raw_data_{dir_name}_rna.csv'
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['comp_name'] + list(combined_index_A)
            writer.writerow(header)
            for comp_name, distances_A in combined_distances_A.items():
                if directory in comp_name:
                    base_name = os.path.basename(comp_name).replace('.gro', '')
                    row = [base_name]
                    for index in combined_index_A:
                        if len(distances_A) > index:
                            value = round(distances_A[index], 4)
                            row.append(value)
                    writer.writerow(row)

    print("Failed to process the following files:")
    for file, error in failed_files:
        print(f"{file}: {error}")