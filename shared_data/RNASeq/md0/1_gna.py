from pymol import cmd
import numpy as np
import matplotlib.pyplot as plt
import os
import random

def remove_first_ter_after_chain_b(input_pdb, output_pdb):
    chain_b_started = False
    ter_skipped = False

    with open(input_pdb, 'r') as infile, open(output_pdb, 'w') as outfile:
        for line in infile:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                chain_id = line[21].strip()  # Column 5 (21st character in 0-indexed line)
                
                # Change HETATM to ATOM if it is part of chain B
                if line.startswith("HETATM"):
                    line = line.replace("HETATM", "ATOM  ", 1)
                
                if chain_id == "B":
                    chain_b_started = True
            if line.startswith("CONECT") or line.startswith("ANISOU"):
                continue
            if chain_b_started and line.startswith("TER") and not ter_skipped:
                ter_skipped = True
                continue

            outfile.write(line)  # Write all other lines

def main(cif_file):
    cmd.reinitialize()
    cmd.load(cif_file, 'ENSG00000174780')

    cmd.load('5v2h.cif')
    # cmd.remove('hydrogen')
    cmd.select('t_methyl', '5v2h and chain A and resi 5 and (name C5M or name H5M1 or name H5M2 or name H5M3)')
    cmd.remove('t_methyl')
    cmd.select('sel_gna', '5v2h and chain A and resi 4-6')
    
    cmd.create('gna', 'sel_gna')
    cmd.select('gna46', 'gna and (resi 4 or resi 6)')
    cmd.select('main68', 'ENSG00000174780 and chain B and (resi 6 or resi 8)')
    cmd.align('gna46', 'main68')
    
    cmd.remove('gna and (resi 4 or resi 6)')
    cmd.remove('ENSG00000174780 and chain B and resi 7')
    cmd.alter('gna', 'resi=7')
    cmd.alter('gna', 'segi="B"')
    cmd.alter('gna', 'chain="B"')
    cmd.alter('gna', 'resn="GNAU"')
    cmd.create('ENSG00000174780', 'ENSG00000174780 or gna')
    cmd.select('atom1', 'ENSG00000174780 and chain B and resi 6 and name O3\'')
    cmd.select('atom2', 'ENSG00000174780 and chain B and resi 7 and name P')
    cmd.select('atom3', 'ENSG00000174780 and chain B and resi 7 and name O2G')
    cmd.select('atom4', 'ENSG00000174780 and chain B and resi 8 and name P')
    cmd.bond('atom1', 'atom2')
    cmd.bond('atom3', 'atom4')
    cmd.select("proton_site", "ENSG00000174780 and chain B and resi 7 and name C5")
    cmd.edit("proton_site")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor proton_site)", "name='H01'")
    cmd.unpick()
    
    distance_atom3_atom4 = cmd.get_distance('atom3', 'atom4')
    coord_atom3 = np.array(cmd.get_atom_coords('atom3'))
    coord_atom4 = np.array(cmd.get_atom_coords('atom4'))
    vector3_4 = coord_atom4 - coord_atom3
    vector3_4_normalized = vector3_4 / np.linalg.norm(vector3_4)
    current_distance_3_4 = distance_atom3_atom4
    desired_distance_3_4 = 1.6
    translation_vector_3_4 = vector3_4_normalized * (current_distance_3_4 - desired_distance_3_4)
    if current_distance_3_4 > desired_distance_3_4:
        cmd.select('translate_selection', 'ENSG00000174780 and chain B and resi 8-21')
        cmd.translate(list(-translation_vector_3_4), 'translate_selection')
    distance_atom1_atom2 = cmd.get_distance('atom1', 'atom2')
    coord_atom1 = np.array(cmd.get_atom_coords('atom1'))
    coord_atom2 = np.array(cmd.get_atom_coords('atom2'))
    vector1_2 = coord_atom2 - coord_atom1
    vector1_2_normalized = vector1_2 / np.linalg.norm(vector1_2)
    current_distance_1_2 = distance_atom1_atom2
    desired_distance_1_2 = 1.6
    translation_vector_1_2 = vector1_2_normalized * (current_distance_1_2 - desired_distance_1_2)
    if current_distance_1_2 > desired_distance_1_2:
        cmd.select('translate_selection_1_6', 'ENSG00000174780 and chain B and resi 7-21')
        cmd.translate(list(-translation_vector_1_2), 'translate_selection_1_6')
    
    #REMOVE 5' PHOS CHAIN B/C
    cmd.select("phosphate_atoms", "chain B and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")
    cmd.select("phosphate_atoms", "chain C and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")
    cmd.save('ENSG00000174780_gna_TER.pdb', 'ENSG00000174780')
    
    def remove_first_ter_after_chain_b(input_pdb, output_pdb):
        chain_b_started = False
        ter_skipped = False
    
        with open(input_pdb, 'r') as infile, open(output_pdb, 'w') as outfile:
            for line in infile:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    chain_id = line[21].strip()  # Column 5 (21st character in 0-indexed line)
                    
                    # Change HETATM to ATOM if it is part of chain B
                    if line.startswith("HETATM"):
                        line = line.replace("HETATM", "ATOM  ", 1)
                    
                    if chain_id == "B":
                        chain_b_started = True
                if line.startswith("CONECT") or line.startswith("ANISOU"):
                    continue
                if chain_b_started and line.startswith("TER") and not ter_skipped:
                    ter_skipped = True
                    continue
    
                outfile.write(line)  # Write all other lines
    
    input_pdb = "ENSG00000174780_gna_TER.pdb"
    remove_first_ter_after_chain_b(input_pdb, "pdb_with_modification.pdb")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script_name.py path/to/your_cif_file.cif")
        sys.exit(1)
    cif_file = sys.argv[1]
    main(cif_file)