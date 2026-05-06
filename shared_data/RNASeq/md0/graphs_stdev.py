from pymol import cmd
import matplotlib.pyplot as plt

i = 1
cmd.reinitialize()
files = [
    # ('4f3t.cif', 'step5_1.gro'),
    # ('4f3t.cif', 'step5_2.gro'),
    # ('4f3t.cif', 'step5_3.gro'),
    # ('4f3t.cif', 'step5_4.gro'),
    # ('4f3t.cif', 'step5_5.gro'),

    # ('4f3t.cif', 'step5_6.gro'),
    # ('4f3t.cif', 'step5_7.gro'),
    # ('4f3t.cif', 'step5_8.gro'),
    # ('4f3t.cif', 'step5_9.gro'),
    # ('4f3t.cif', 'step5_10.gro'),
    # ('4f3t.cif', 'chpc095/step4_updated_ENSG00000001497.gro'),
    # ('4f3t.cif', 'step4.0_minimization_3.gro')


    # 
    # ('4f3t.cif', 'step4.0_minimization_1.gro'), 
    # ('4f3t.cif', 'step4.0_minimization_2.gro'),
    # ('4f3t.cif', 'step4.0_minimization_3.gro'),
    # ('4f3t.cif', 'step4.0_minimization_4.gro'),
    # ('4f3t.cif', 'step4.0_minimization_5.gro'),
    # ('4f3t.cif', 'step4.0_minimization_6.gro'),
    # ('4f3t.cif', 'step4.0_minimization_7.gro'),
    # ('4f3t.cif', 'step4.0_minimization_8.gro'),
    # ('4f3t.cif', 'step4.0_minimization_9.gro'),
    # ('4f3t.cif', 'step4.0_minimization_10.gro'),
    # ('4f3t.cif', 'structure_solv_ions.gro')

    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 1}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 2}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 3}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 4}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 5}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 6}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 7}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 8}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 9}.gro'),
    ('4f3t.cif', f'step4.0_minimization_{i * 10 + 10}.gro'),
    ('4f3t.cif', 'structure_solv_ions.gro')
]

combined_index_A = list(range(22, 200))
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

######################################################
import numpy as np

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

print("Sum of absolute standard deviations for each pair key (initial):")
for key, total_std_dev in absolute_std_dev_sums.items():
    print(f"{key}: {total_std_dev}")

max_key = max(absolute_std_dev_sums, key=absolute_std_dev_sums.get)
del combined_distances_A[max_key]
#########################################################################
import numpy as np

first_items = [combined_distances_A[key][20] for key in combined_distances_A]
average_first = np.mean(first_items)
std_dev_first = np.std(first_items)

print("First items for each pair key:")
for key in combined_distances_A:
    print(f"{key}: {combined_distances_A[key][20]}")

print(f"Average of first items: {average_first}")
print(f"Standard deviation of first items: {std_dev_first}")

for key in combined_distances_A:
    num_stdevs = (combined_distances_A[key][20] - average_first) / std_dev_first if std_dev_first != 0 else 0
    print(f"{key} is {num_stdevs} standard deviations from the average")
###############################################################################
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

print("Sum of absolute standard deviations for each pair key (after removal):")
for key, total_std_dev in absolute_std_dev_sums.items():
    print(f"{key}: {total_std_dev}")
######################################################
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
# ##########################################################
plt.figure(figsize=(14, 7))
for comp_name, distances in combined_distances_A.items():
    # print(f"Plotting data for {comp_name}: {distances[:10]}...")
    plt.plot(combined_index_A, distances, label=f'{comp_name}')
plt.xlabel('Residue Index')
plt.ylabel('Distance (Å)')
plt.title("Protein Region (not C3') Residue-level Distance Comparison Across Structures")
plt.legend()
plt.show()