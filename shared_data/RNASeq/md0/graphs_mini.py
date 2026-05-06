from pymol import cmd
import matplotlib.pyplot as plt

cmd.reinitialize()
files = [
    ('4f3t.cif', 'step4.0_minimization_1.gro'),
    ('4f3t.cif', 'step4.0_minimization_2.gro'),
    ('4f3t.cif', 'step4.0_minimization_3.gro'),
    ('4f3t.cif', 'step4.0_minimization_4.gro'),
    ('4f3t.cif', 'step4.0_minimization_5.gro'),
    ('4f3t.cif', 'step4.0_minimization_6.gro'),
    ('4f3t.cif', 'step4.0_minimization_7.gro'),
    ('4f3t.cif', 'step4.0_minimization_8.gro'),
    ('4f3t.cif', 'step4.0_minimization_9.gro'),
    ('4f3t.cif', 'step4.0_minimization_10.gro'),
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
##########################################################
plt.figure(figsize=(14, 7))
for comp_name, distances in combined_distances_A.items():
    # print(f"Plotting data for {comp_name}: {distances[:10]}...")
    plt.plot(combined_index_A, distances, label=f'{comp_name}')
plt.xlabel('Residue Index')
plt.ylabel('Distance (Å)')
plt.title("Protein Region (not C3') Residue-level Distance Comparison Across Structures")
plt.legend()
plt.show()