from pymol import cmd
import numpy as np
import os

def remove_first_ter_after_chain_b(input_pdb, output_pdb):
    chain_b_started = False
    ter_skipped = False

    with open(input_pdb, 'r') as infile, open(output_pdb, 'w') as outfile:
        for line in infile:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                chain_id = line[21].strip()  # Column 5 (21st character in 0-indexed line)
                if chain_id == "B":
                    chain_b_started = True

            if chain_b_started and line.startswith("TER") and not ter_skipped:
                ter_skipped = True  # Skip the first TER after chain B starts
                continue

            outfile.write(line)  # Write all other lines

def main(cif_file):
    cmd.reinitialize()
    cmd.load(cif_file, 'PIK3CB_guide_target') 
    cmd.load('4f3t_v4G2c.pdb')
    
    cmd.select('chainB_resi3_4', 'chain B and (resi 3 or resi 4)')
    cmd.select('chainR_resi2_3', 'chain R and (resi 2 or resi 3)')
    cmd.create('new_obj_chainR', 'chainR_resi2_3')
    cmd.align('new_obj_chainR', 'chainB_resi3_4')
    cmd.select('chainB_atoms', 'chain B and ((resi 3 and name O3\') or (resi 4 and (name OP1 or name OP2 or name P or name C5\' or name O5\')))')
    cmd.select('keep_new_obj_chainR_atoms', 'new_obj_chainR and ((resi 2 and (name C or name O or name C6\')) or (resi 3 and (name N or name C5\')))')
    cmd.remove('new_obj_chainR and not keep_new_obj_chainR_atoms')
    cmd.remove('chainB_atoms')
    cmd.create('PIK3CB_guide_target', 'PIK3CB_guide_target or new_obj_chainR')
    cmd.select('atom1', 'PIK3CB_guide_target and chain B and resi 3 and name C3\'')
    cmd.select('atom2', 'PIK3CB_guide_target and chain R and name C6\'')
    cmd.bond('atom1', 'atom2')
    cmd.select('atom3', 'PIK3CB_guide_target and chain B and resi 4 and name C4\'')
    cmd.select('atom4', 'PIK3CB_guide_target and chain R and name C5\'')
    cmd.bond('atom3', 'atom4')

    distance_atom3_atom4 = cmd.get_distance('atom3', 'atom4')
    coord_atom3 = np.array(cmd.get_atom_coords('atom3'))
    coord_atom4 = np.array(cmd.get_atom_coords('atom4'))
    vector3_4 = coord_atom4 - coord_atom3
    vector3_4_normalized = vector3_4 / np.linalg.norm(vector3_4)
    current_distance_3_4 = distance_atom3_atom4
    desired_distance_3_4 = 1.6
    translation_vector_3_4 = vector3_4_normalized * (current_distance_3_4 - desired_distance_3_4)
    if current_distance_3_4 > desired_distance_3_4:
        cmd.translate(list(-translation_vector_3_4), 'atom4')
    
    distance_atom1_atom2 = cmd.get_distance('atom1', 'atom2')
    coord_atom1 = np.array(cmd.get_atom_coords('atom1'))
    coord_atom2 = np.array(cmd.get_atom_coords('atom2'))
    vector1_2 = coord_atom2 - coord_atom1
    vector1_2_normalized = vector1_2 / np.linalg.norm(vector1_2)
    current_distance_1_2 = distance_atom1_atom2
    desired_distance_1_2 = 1.6
    translation_vector_1_2 = vector1_2_normalized * (current_distance_1_2 - desired_distance_1_2)
    if current_distance_1_2 > desired_distance_1_2:
        cmd.translate(list(-translation_vector_1_2), 'atom2')
    
    cmd.alter('atom2', 'chain="B"')
    cmd.alter('atom2', 'resi=3')
    cmd.alter('atom2', 'resn="A"')
    cmd.alter('atom2', 'segi="B"')
    cmd.alter('chain R', 'resi=4')
    cmd.alter('chain R', 'resn="G"')
    cmd.alter('chain R', 'segi="B"')
    cmd.alter('chain R', 'chain="B"')
    cmd.alter("chain B and resi 3", "resn='R3'")
    cmd.alter("chain B and resi 4", "resn='R4'")
    ###########
    cmd.sort()
    
    cmd.select("phosphate_atoms", "chain B and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")
    cmd.select("phosphate_atoms", "chain C and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")

    ##R3
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C5'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H02'")
    cmd.attach("H", 1, 1)
    cmd.unpick()
    cmd.select("incorrect_hydrogen", "(neighbor target_atom) and elem H and not name H02")
    cmd.alter("incorrect_hydrogen", "name='H06'")
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/N6")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H11'")
    cmd.attach("H", 1, 1)
    cmd.unpick()
    cmd.select("incorrect_hydrogen", "(neighbor target_atom) and elem H and not name H11")
    cmd.alter("incorrect_hydrogen", "name='H12'")
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C6'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H01'")
    cmd.attach("H", 1, 1)
    cmd.unpick()
    cmd.select("incorrect_hydrogen", "(neighbor target_atom) and elem H and not name H01")
    cmd.alter("incorrect_hydrogen", "name='H03'")
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C4'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H04'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C1'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H09'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C8")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H13'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C2")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H10'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C3'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H05'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/C2'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H07'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/3/O2'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H08'")
    cmd.unpick()
    
    ########################### R4
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/N2")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H08'")
    cmd.attach("H", 1, 1)
    cmd.unpick()
    cmd.select("incorrect_hydrogen", "(neighbor target_atom) and elem H and not name H08")
    cmd.alter("incorrect_hydrogen", "name='H09'")
    
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/C5'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H01'")
    cmd.attach("H", 1, 1)
    cmd.unpick()
    cmd.select("incorrect_hydrogen", "(neighbor target_atom) and elem H and not name H01")
    cmd.alter("incorrect_hydrogen", "name='H02'")
    
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/C4'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H03'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/C3'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H04'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/C2'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H05'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/O2'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H06'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/C1'")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H07'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/C8")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H10'")
    cmd.unpick()
    
    cmd.select("target_atom", "/PIK3CB_guide_target//B/4/N")
    cmd.edit("target_atom")
    cmd.attach("H", 1, 1)
    cmd.alter("(elem H and neighbor target_atom)", "name='H14'")
    cmd.unpick()

    
    cmd.sort()

    

    
    cmd.save('PIK3CB_guide_target_amide_TER.pdb', 'PIK3CB_guide_target')
    
    input_pdb = "PIK3CB_guide_target_amide_TER.pdb"
    remove_first_ter_after_chain_b(input_pdb, "pdb_with_modification.pdb")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script_name.py path/to/your_cif_file.cif")
        sys.exit(1)
    cif_file = sys.argv[1]
    main(cif_file)