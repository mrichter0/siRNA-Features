## remove phosphates
from pymol import cmd
import numpy as np
import os

def main(cif_file):
    cmd.reinitialize()
    cmd.load(cif_file, 'PIK3CB_guide_target') 
    cmd.select("phosphate_atoms", "chain B and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")
    cmd.select("phosphate_atoms", "chain C and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")
    cmd.save('pdb_with_modification.pdb', 'PIK3CB_guide_target')

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script_name.py path/to/your_cif_file.cif")
        sys.exit(1)
    cif_file = sys.argv[1]
    main(cif_file)