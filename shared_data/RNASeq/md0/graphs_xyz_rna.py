from pymol import cmd
import matplotlib.pyplot as plt
import sys
import numpy as np
import gc
import csv
import os

cmd.reinitialize()
files = []
cpus = 64
output_file = 'raw_data_xyz_rna_unmod.csv'
directories = [
    # '/data/home/mrichte3/RNASeq/amide/step5',
    # '/data/home/mrichte3/RNASeq/gna/step5',
    '/data/home/mrichte3/RNASeq/unmod',
]
for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(('.cif', '.gro', '.pdb')) and os.path.join(directory, filename) != '/data/home/mrichte3/RNASeq/gna/step5/ENSG00000187837.gro':
            files.append(('4f3t.cif', os.path.join(directory, filename)))

# files = files[:1000]
# first_4000 = files[:4000]
# second_4000 = files[4000:8000]
# third_4000 = files[8000:12000]
# fourth_4000 = files[12000:16000]
combined_index_A = list(range(0, 42))  #22 800 22 200
combined_distances_A = {}

from multiprocessing import Pool

def process_files(file_pair):
    ref_file, comp_file = file_pair
    # print(f"processing {comp_file}")
    cmd.reinitialize()
    cmd.load(ref_file, 'ref')
    cmd.load(comp_file, 'comp')
    if cmd.count_atoms('ref') == 0 or cmd.count_atoms('comp') == 0:
        print(f"Error: One of the structures failed to load: {ref_file} or {comp_file}")

    cmd.remove('solvent')
    cmd.remove('ref and resn CL')
    cmd.remove('ref and resn NA+')
    cmd.remove('ref and hydrogen')
    cmd.remove('comp and hydrogen')

    alignment_rms = cmd.align('comp', 'ref')
    cmd.select("only_C3_ref", "ref and byres (name C3' or name C3G)")
    cmd.select("only_C3_comp", "comp and byres (name C3' or name C3G)")
    distances_A = []
    distances_chain_a = []
    distances_chain_b = []
    
    for resi in range(1, 22):
        cmd.select("first_rna_base_comp", f"byres (first (only_C3_comp and resi {resi}))")
        coords_a = cmd.get_coords(f"first (only_C3_comp and resi {resi})")
        distances_chain_a.append(coords_a)
        
        cmd.select("first_rna_base_comp_b", f"byres (only_C3_comp and resi {resi} and not first_rna_base_comp)")
        coords_b_comp = cmd.get_coords("first_rna_base_comp_b")
        distances_chain_b.append(coords_b_comp)
    distances_A = distances_chain_a + distances_chain_b
    cmd.delete("all") 
    return distances_A

if __name__ == '__main__':
    from tqdm.notebook import tqdm
    combined_distances_A = {}
    with Pool(processes=cpus) as pool:
        # results = pool.map(process_files, files)
        # results = list(tqdm(pool.imap(process_files, files), total=len(files), desc="Processing files"))
        results = list(tqdm(pool.imap(process_files, files), total=len(files), desc="Processing files", leave=True))
        gc.collect()
    print("results rcvd")
    for index, distances_A in enumerate(results):
        if distances_A:
            comp_name = f"{index}_{files[index][1]}"
            combined_distances_A[comp_name] = distances_A

##################################################################
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    header = ['comp_name']
    for index in combined_index_A:
        header.extend([f'{index}x', f'{index}y', f'{index}z'])
    writer.writerow(header)
    for comp_name, distances_A in combined_distances_A.items():
        base_name = comp_name.split('/')[-1].replace('.gro', '').replace('.pdb', '')
        row = [base_name]
        for index in combined_index_A:
            idx = combined_index_A.index(index)
            if len(distances_A) > idx:
                value = distances_A[idx]
                if value is None:
                    print(f'None value for comp_name: {base_name}, index: {index}')
                elif len(value) > 0:
                    row.extend([value[0][0], value[0][1], value[0][2]])
        writer.writerow(row)
##################################################################
