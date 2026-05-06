from pymol import cmd
import matplotlib.pyplot as plt
import sys
import numpy as np
import gc
import os
cmd.reinitialize()
cpus = 48
output_file = 'raw_data_xyz_unmod.csv'

files = []
directories = [
    # '/data/home/mrichte3/RNASeq/amide/step5',
    # '/data/home/mrichte3/RNASeq/gna/step5',
    '/data/home/mrichte3/RNASeq/unmod',
]
# for directory in directories:
#     for filename in os.listdir(directory):
#         if filename.endswith(('.cif', '.gro', '.pdb')):
#             files.append(('4f3t.cif', os.path.join(directory, filename)))
for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(('.cif', '.gro', '.pdb')) and os.path.join(directory, filename) != '/data/home/mrichte3/RNASeq/gna/step5/ENSG00000187837.gro':
            files.append(('4f3t.cif', os.path.join(directory, filename)))

# files = files[:1]
# first_4000 = files[:4000]
# second_4000 = files[4000:8000]
# third_4000 = files[8000:12000]
# fourth_4000 = files[12000:16000]
combined_index_A = list(range(22, 859))  #22 800 22 200
combined_distances_A = {}
# index = 0
# for ref_file, comp_file in files:
#     cmd.reinitialize()
#     # print(f"Loading reference file: {ref_file}")
#     # print(f"Loading comparison file: {comp_file}")
#     cmd.load(ref_file, 'ref')
#     cmd.load(comp_file, 'comp')
#     if cmd.count_atoms('ref') == 0 or cmd.count_atoms('comp') == 0:
#         print(f"Error: One of the structures failed to load: {ref_file} or {comp_file}")
#         continue
#     cmd.remove('solvent')
#     cmd.remove('ref and resn CL')
#     cmd.remove('ref and resn NA+')
#     cmd.remove('ref and hydrogen')
#     cmd.remove('comp and hydrogen')
#     alignment_rms = cmd.align('comp', 'ref')
#     # print(f"Alignment RMSD for {comp_file}: {alignment_rms}")
#     cmd.select('not_C3_ref', 'ref and not byres name C3\'')
#     cmd.select('not_C3_comp', 'comp and not byres name C3\'')
#     ref_atom_count = cmd.count_atoms('not_C3_ref')
#     comp_atom_count = cmd.count_atoms('not_C3_comp')
#     # print(f"Atoms in not_C3_ref: {ref_atom_count}, Atoms in not_C3_comp: {comp_atom_count}")
#     if ref_atom_count == 0 or comp_atom_count == 0:
#         print(f"Error: No atoms found in one of the selections for {comp_file}")
#         continue
#     distances_A = []
#     for i in combined_index_A:
#         distance = cmd.distance(f'dist_{i}', f'not_C3_ref and resi {i} and name C', f'not_C3_comp and resi {i} and name C')
#         distances_A.append(distance)
#     comp_name = f"{index}_{comp_file}"
#     index += 1
#     if len(distances_A) > 0:
#         combined_distances_A[comp_name] = distances_A
#         print(f"Distances calculated for {comp_name}: {len(distances_A)}")
#     else:
#         print(f"Warning: No distances found for {comp_name}")

#############################################
# min_max_data = {}
# for comp_name, distances_A in combined_distances_A.items():
#     min_max_data[comp_name] = {}
#     for index in combined_index_A:
#         if index < len(distances_A):
#             min_value = min(distances_A[index])
#             max_value = max(distances_A[index])
#             min_max_data[comp_name][index] = (min_value, max_value)
#             print(f"{comp_name} - Index {index}: Min = {min_value}, Max = {max_value}")
##################################################
# plt.figure(figsize=(14, 7))
# for comp_name, distances in combined_distances_A.items():
#     # print(f"Plotting data for {comp_name}: {distances[:10]}...")
#     plt.plot(combined_index_A, distances, label=f'{comp_name}')
# plt.xlabel('Residue Index')
# plt.ylabel('Distance (Å)')
# plt.title("Protein Region (not C3') Residue-level Distance Comparison Across Structures")
# plt.legend()
# plt.show()
##############################################
# num_items = len(next(iter(combined_distances_A.values())))
# rsd_sums = 0
# for index in range(num_items):
#     values_at_index = [combined_distances_A[key][index] for key in combined_distances_A if "structure_solv_ions" not in key]
#     absolute_values_at_index = [abs(value) for value in values_at_index]
#     average = np.mean(absolute_values_at_index)
#     std_dev = np.std(absolute_values_at_index)
#     rsd = std_dev / average if average != 0 else 0
#     rsd_sums += rsd
# print(f"Sum of relative standard deviations: {rsd_sums:.4f}")
################################################################
# num_items = len(next(iter(combined_distances_A.values())))
# rsd_sums = 0
# for index in range(num_items):
#     values_at_index = [combined_distances_A[key][index] for key in combined_distances_A]
#     absolute_values_at_index = [abs(value) for value in values_at_index]
#     average = np.mean(absolute_values_at_index)
#     std_dev = np.std(absolute_values_at_index)
#     rsd = std_dev / average if average != 0 else 0
#     rsd_sums += rsd
# print(f"Sum of relative standard deviations: {rsd_sums:.4f}")
# # ###################################################
# pair1_key = f"0_{files[0][1]}"
# pair2_key = f"{len(files) - 1}_{files[-1][1]}"

# if pair1_key in combined_distances_A and pair2_key in combined_distances_A:
#     distances_1 = combined_distances_A[pair1_key]
#     distances_2 = combined_distances_A[pair2_key]
#     if len(distances_1) == len(distances_2):
#         differences = [abs(a - b) for a, b in zip(distances_1, distances_2)]
#         total_sum = round(sum(differences), 1)
#         print(f"Sum of differences between first and last pair: {total_sum}")
#     else:
#         print("Error: Distance lists have different lengths.")
# else:
#     print("Error: One or both files not processed correctly.")
from multiprocessing import Pool

def process_files(file_pair):
    ref_file, comp_file = file_pair
    # print(f"processing {comp_file}")
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
##########################################################################################################################################
        coords_A = cmd.get_coords(f'not_C3_ref and resi {i} and name C')
        coords_B = cmd.get_coords(f'not_C3_comp and resi {i} and name C')
        # print(f'Residue {i}: Ref Coords {coords_A}, Comp Coords {coords_B}, Comp File {comp_file}')
        # if i == 26:
        #     cmd.save('aligned_structure.pdb', 'comp')
        #     break
        distances_A.append(coords_B)
##########################################################################################################################################
        # distance = cmd.distance(f'dist_{i}', f'not_C3_ref and resi {i} and name C', f'not_C3_comp and resi {i} and name C')
        # distances_A.append(distance)
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


#########################################function for collecting min/max values
    # min_max_data = {}
    # for index in combined_index_A:
    #     min_value = float('inf')
    #     max_value = float('-inf')
    #     data_found = False
    
    #     for comp_name, distances_A in combined_distances_A.items():
    #         if len(distances_A) > combined_index_A.index(index):
    #             value = distances_A[combined_index_A.index(index)]
    #             if isinstance(value, (float, int)):
    #                 data_found = True
    #                 min_value = min(min_value, value)
    #                 max_value = max(max_value, value)
    
    #     if data_found:
    #         min_max_data[index] = (min_value, max_value)
    #         print(f"Index {index}: Min = {min_value}, Max = {max_value}")
    #     else:
    #         print(f"No data found at Index {index}.")
##############################################################################
# min_max_data = {}
# with open('min_max_results_all.txt', 'w') as f:
#     for index in combined_index_A:
#         min_value = float('inf')
#         max_value = float('-inf')
#         data_found = False
#         for comp_name, distances_A in combined_distances_A.items():
#             if len(distances_A) > combined_index_A.index(index):
#                 value = distances_A[combined_index_A.index(index)]
#                 if isinstance(value, (float, int)):
#                     data_found = True
#                     min_value = min(min_value, value)
#                     max_value = max(max_value, value)
#                     if value > 25:
#                         print(f"High value found: {value} from {comp_name} at Index {index}")
#         if data_found:
#             min_max_data[index] = (min_value, max_value)
#             f.write(f"Index {index}: Min = {min_value}, Max = {max_value}\n")
#         else:
#             f.write(f"No data found at Index {index}.\n")
# print(f"data was written to file")
##################################################################
# import csv
# with open('raw_data_gna.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     header = ['comp_name'] + list(combined_index_A)
#     writer.writerow(header)
#     for comp_name, distances_A in combined_distances_A.items():
#         base_name = comp_name.split('/')[-1].replace('.gro', '')
#         row = [base_name]
#         for index in combined_index_A:
#             if len(distances_A) > combined_index_A.index(index):
#                 value = round(distances_A[combined_index_A.index(index)], 4)
#                 row.append(value)
#         writer.writerow(row)
##################################################################
import csv
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
            if len(distances_A) > combined_index_A.index(index):
                value = distances_A[combined_index_A.index(index)]
                row.extend([value[0][0], value[0][1], value[0][2]])
        writer.writerow(row)
##################################################################
    # plt.figure(figsize=(14, 7))
    # for comp_name, distances in combined_distances_A.items():
    #     # print(f"Plotting data for {comp_name}: {distances[:10]}...")
    #     plt.plot(combined_index_A, distances, label=f'{comp_name}')
    # plt.xlabel('Residue Index')
    # plt.ylabel('Distance (Å)')
    # plt.title("Protein Region (not C3') Residue-level Distance Comparison Across Structures")
    # plt.legend()
    # plt.show()