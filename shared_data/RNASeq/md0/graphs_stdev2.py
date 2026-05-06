from pymol import cmd
import matplotlib.pyplot as plt
import sys
import numpy as np
if len(sys.argv) != 2:
    print("Usage: python script.py <gpu_index>", flush=True)
    sys.exit(1)

i = int(sys.argv[1])
cmd.reinitialize()

files = [
  

    # ('4f3t.cif', f'../md/working_folder_amide/step4.0_minimization.gro'),
    # ('4f3t.cif', f'../md/working_folder_gna/step4.0_minimization.gro'),
    
    # ('4f3t.cif', f'../md/working_folder_amide/step5_0.gro'), #1/90
    # ('4f3t.cif', f'../md/working_folder_gna/step5_0.gro'),
    # ('4f3t.cif', f'../md/working_folder_amide/step5_1.gro'), #2/90 3.9 43.3
    # ('4f3t.cif', f'../md/working_folder_gna/step5_1.gro'),
    # ('4f3t.cif', f'../md/working_folder_amide/step5_2.gro'), #2.5/90? 5.0 44.7
    # ('4f3t.cif', f'../md/working_folder_gna/step5_2.gro'),
    # ('4f3t.cif', f'../md/working_folder_amide/step5_3.gro'), #3/90 7.75 46.2
    # ('4f3t.cif', f'../md/working_folder_gna/step5_3.gro'),
    # ('4f3t.cif', f'../md/working_folder_amide/step5_4.gro'), #4/90
    # ('4f3t.cif', f'../md/working_folder_gna/step5_4.gro'),
    # ('4f3t.cif', f'../md/working_folder_amide/step5_5.gro'), #5/90
    # ('4f3t.cif', f'../md/working_folder_gna/step5_5.gro'),
    # ('4f3t.cif', f'../md/working_folder_amide/step5_6.gro'), #10/90#######
    # ('4f3t.cif', f'../md/working_folder_gna/step5.gro'),
    # ('4f3t.cif', f'../md/working_folder_amide/step5.gro'), #10/80#######
#1/90 3.1 47.3
#3/90 7.4 44
#4/90 9 40
#5/90 48
#10/90 62
#5/60 9/27
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/amide/ENSG00000000003.pdb'),############
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/amide/step4/ENSG00000019144.gro'),
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/gna/step5/ENSG00000001036.gro'),
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/unmod/step5/ENSG00000001036.gro'),
    # ('4f3t.cif', 'AGO2_msa.cif'),
    # ('4f3t.cif', 'AGO2_nomsa.cif'),
    # ('4f3t.cif', 'PIK3CB_guide_target.cif'),

    ('/data/home/mrichte3/RNASeq/output_cifs/ENSG00000019144.cif', f'/data/home/mrichte3/RNASeq/amide/step4/ENSG00000019144.gro'),
    ('/data/home/mrichte3/RNASeq/output_cifs/ENSG00000019144.cif', f'/data/home/mrichte3/RNASeq/gna/step4/ENSG00000019144.gro'),
    ('/data/home/mrichte3/RNASeq/output_cifs/ENSG00000019144.cif', f'/data/home/mrichte3/RNASeq/unmod/step4/ENSG00000019144.gro'),
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/amide/step5/ENSG00000000419.gro'),
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/gna/step5/ENSG00000000419.gro'),
    # # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/output_cifs/ENSG00000000419.cif'),
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/unmod/step5/ENSG00000000419.gro'),
 

    # ('4f3t.cif', f'../md/working_folder_amide/step4.0_minimization.gro'), #dif: 9.7
    # ('4f3t.cif', f'../md/working_folder_gna/step4.0_minimization.gro'),

    # ('4f3t.cif', f'../md/working_folder_unmod/step4.0_minimization.gro'),
    # ('4f3t.cif', f'../md/working_folder_unmod/step5.gro'),
    # ('4f3t.cif', f'/data/home/mrichte3/RNASeq/unmod/ENSG00000000003.pdb'),############

    ################

    # ('4f3t.cif', f'../md4/step5_{i * 10 + 0}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 1}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 2}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 3}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 4}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 5}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 6}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 7}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 8}.gro'),
    # ('4f3t.cif', f'../md4/step5_{i * 10 + 9}.gro'),
    # ('4f3t.cif', '../md4/structure_solv_ions.gro')
    # ('4f3t.cif', f'../md4/step4.0_minimization_{i * 10 + 1}.gro'),

]
# import os
# files = []
# directories = [
#     '/data/home/mrichte3/RNASeq/amide/step5',
#     '/data/home/mrichte3/RNASeq/gna/step5',
#     '/data/home/mrichte3/RNASeq/unmod',
# ]
# for directory in directories:
#     for filename in os.listdir(directory):
#         if filename.endswith(('.cif', '.gro', '.pdb')):
#             files.append(('4f3t.cif', os.path.join(directory, filename)))

# files = files[:5]
####################################################

combined_index_A = list(range(22, 859))  #22 200
combined_distances_A = {}
index = 0
for ref_file, comp_file in files:
    cmd.reinitialize()
    # print(f"Loading reference file: {ref_file}")
    # print(f"Loading comparison file: {comp_file}")
    cmd.load(ref_file, 'ref')
    cmd.load(comp_file, 'comp')
    if cmd.count_atoms('ref') == 0 or cmd.count_atoms('comp') == 0:
        print(f"Error: One of the structures failed to load: {ref_file} or {comp_file}")
        continue
    cmd.remove('solvent')
    cmd.remove('ref and resn CL')
    cmd.remove('ref and resn NA+')
    cmd.remove('ref and hydrogen')
    cmd.remove('comp and hydrogen')
    alignment_rms = cmd.align('comp', 'ref')
    # print(f"Alignment RMSD for {comp_file}: {alignment_rms}")
    cmd.select('not_C3_ref', 'ref and not byres name C3\'')
    cmd.select('not_C3_comp', 'comp and not byres name C3\'')
    ref_atom_count = cmd.count_atoms('not_C3_ref')
    comp_atom_count = cmd.count_atoms('not_C3_comp')
    # print(f"Atoms in not_C3_ref: {ref_atom_count}, Atoms in not_C3_comp: {comp_atom_count}")
    if ref_atom_count == 0 or comp_atom_count == 0:
        print(f"Error: No atoms found in one of the selections for {comp_file}")
        continue
    distances_A = []
    for i in combined_index_A:
        distance = cmd.distance(f'dist_{i}', f'not_C3_ref and resi {i} and name C', f'not_C3_comp and resi {i} and name C')
        distances_A.append(distance)
    comp_name = f"{index}_{comp_file}"
    index += 1
    if len(distances_A) > 0:
        combined_distances_A[comp_name] = distances_A
        # print(f"Distances calculated for {comp_name}: {len(distances_A)}")
    else:
        print(f"Warning: No distances found for {comp_name}")


##################################################
plt.figure(figsize=(14, 7))
for comp_name, distances in combined_distances_A.items():
    # print(f"Plotting data for {comp_name}: {distances[:10]}...")
    plt.plot(combined_index_A, distances, label=f'{comp_name}')
plt.xlabel('Residue Index')
plt.ylabel('Distance (Å)')
plt.title("Protein Region (not C3') Residue-level Distance Comparison Across Structures")
plt.legend()
plt.show()
##############################################
######################################################
###################goodness of fit?
# from sklearn.metrics import mean_squared_error
# import numpy as np

# num_items = len(next(iter(combined_distances_A.values())))
# scores = {}
# for index in range(num_items):
#     values_at_index = [combined_distances_A[key][index] for key in combined_distances_A]
#     mean_value = np.mean(values_at_index)
#     for key in combined_distances_A:
#         mse = mean_squared_error([combined_distances_A[key][index]], [mean_value])
#         if key not in scores:
#             scores[key] = 0
#         scores[key] += mse
# print("Mean squared error for each key compared to the mean:")
# for key, total_mse in scores.items():
#     print(f"{key}: {total_mse:.8f}")
####################################################
###########testing new code here
num_items = len(next(iter(combined_distances_A.values())))
rsd_sums = 0
for index in range(num_items):
    values_at_index = [combined_distances_A[key][index] for key in combined_distances_A if "structure_solv_ions" not in key]
    absolute_values_at_index = [abs(value) for value in values_at_index]
    average = np.mean(absolute_values_at_index)
    std_dev = np.std(absolute_values_at_index)
    rsd = std_dev / average if average != 0 else 0
    rsd_sums += rsd
print(f"Sum of relative standard deviations: {rsd_sums:.4f}")
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
pair1_key = f"0_{files[0][1]}"
pair2_key = f"{len(files) - 1}_{files[-1][1]}"

if pair1_key in combined_distances_A and pair2_key in combined_distances_A:
    distances_1 = combined_distances_A[pair1_key]
    distances_2 = combined_distances_A[pair2_key]
    if len(distances_1) == len(distances_2):
        differences = [abs(a - b) for a, b in zip(distances_1, distances_2)]
        total_sum = round(sum(differences), 1)
        print(f"Sum of differences between first and last pair: {total_sum}")
    else:
        print("Error: Distance lists have different lengths.")
else:
    print("Error: One or both files not processed correctly.")
# ##########################################################
while len(combined_distances_A) > 1:
    num_items = len(next(iter(combined_distances_A.values())))
    absolute_std_dev_sums = {}
    for index in range(num_items):
        values_at_index = [combined_distances_A[key][index] for key in combined_distances_A]
        absolute_values_at_index = [abs(value) for value in values_at_index]
        average = np.mean(absolute_values_at_index)
        std_dev = np.std(absolute_values_at_index)
        for key in combined_distances_A:
            num_stdevs = (abs(combined_distances_A[key][index]) - average) / std_dev if std_dev != 0 else 0
            if key not in absolute_std_dev_sums:
                absolute_std_dev_sums[key] = 0
            absolute_std_dev_sums[key] += abs(num_stdevs)
    # print("Sum of absolute standard deviations for each pair key (initial):")
    # for key, total_std_dev in absolute_std_dev_sums.items():
    #     print(f"{key}: {total_std_dev}")
##############################################
    # if 'normalized_std_dev_results' not in locals():
    #     absolute_std_dev_list = [total_std_dev for total_std_dev in absolute_std_dev_sums.values()]
    #     total_std_dev = sum(absolute_std_dev_list)
    #     final_results = {key: (total_std_dev, total_std_dev / total_std_dev) for key, total_std_dev in zip(absolute_std_dev_sums.keys(), absolute_std_dev_list)}
    #     normalized_std_dev_results = True
    #     normalized_values = [current_value / total_std_dev for current_value in absolute_std_dev_list]
    #     for key, current_value in zip(absolute_std_dev_sums.keys(), absolute_std_dev_list):
    #         normalized_value = current_value / total_std_dev
    #         # print(f"{key}: {current_value}, {normalized_value:.4f}")

######################################
        # from itertools import combinations
        # for combo in combinations(normalized_values, 4):
        #     if sum(combo) >= 0.4:
        #         print("This data is eliminated...................................................................................")
        #         break
                
##############################################
    max_key = max(absolute_std_dev_sums, key=absolute_std_dev_sums.get)
    del combined_distances_A[max_key]


###############################################################################
for comp_name, distances in combined_distances_A.items():
    for key, total_std_dev in absolute_std_dev_sums.items():
        if key == comp_name:
            print(f"Best plot id: {key}: {total_std_dev}")
######################################################

# plt.figure(figsize=(14, 7))
# for comp_name, distances in combined_distances_A.items():
#     # print(f"Plotting data for {comp_name}: {distances[:10]}...")
#     plt.plot(combined_index_A, distances, label=f'{comp_name}')
# plt.xlabel('Residue Index')
# plt.ylabel('Distance (Å)')
# plt.title("Protein Region (not C3') Residue-level Distance Comparison Across Structures")
# plt.legend()
# plt.show()