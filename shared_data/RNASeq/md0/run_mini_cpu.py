import os
from pymol import cmd
import subprocess
import os
import shutil
import time
os.environ['PATH'] = '/data/home/mrichte3/gromacs-2024.2/install/bin:' + os.environ['PATH']
if 'LD_LIBRARY_PATH' in os.environ:
    os.environ['LD_LIBRARY_PATH'] = '/data/home/mrichte3/gromacs-2024.2/install/lib:' + os.environ['LD_LIBRARY_PATH']
else:
    os.environ['LD_LIBRARY_PATH'] = '/data/home/mrichte3/gromacs-2024.2/install/lib'
os.environ['GMX_MAXBACKUP'] = '-1'


def remove_phos(cif_file):
    cmd.reinitialize()
    cmd.load(cif_file, 'PIK3CB_guide_target') 
    cmd.select("phosphate_atoms", "chain B and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")
    cmd.select("phosphate_atoms", "chain C and resi 1 and (name OP1 or name OP2 or name P)")
    cmd.extract("phosphate_group", "phosphate_atoms")
    cmd.remove("phosphate_atoms")
    cmd.save('pdb_with_modification.pdb', 'PIK3CB_guide_target')

def run_command(command, input_text=None, max_chars=100):
    result = subprocess.run(command, capture_output=True, text=True, input=input_text)
    print(result.stdout)
    print(result.stderr)
    output = result.stdout + result.stderr
    for line in output.splitlines():
        if "warning" in line.lower() or "fatal" in line.lower():
            print(line) # print(line[:max_chars])
    
def run_gromacs_commands():
    command = ["gmx", "pdb2gmx", "-f", "pdb_with_modification.pdb", "-o", "structure_processed.gro", 
               "-p", "topol.top", "-i", "posre.itp"]
    input_text = "6\n1\n"        ############ 6 1 for custom
    run_command(command, input_text)
    command = ["gmx", "editconf", "-f", "structure_processed.gro", "-o", "structure_box.gro", "-c", "-d", "1.0", "-bt", "cubic"]
    run_command(command)
    command = ["gmx", "solvate", "-cp", "structure_box.gro", "-cs", "spc216.gro", "-o", "structure_solv.gro", "-p", "topol.top"]
    run_command(command)
    command = ["gmx", "grompp", "-f", "ions.mdp", "-c", "structure_solv.gro", "-p", "topol.top", "-o", "ions.tpr", "-maxwarn", "3"]
    run_command(command)
    command = ["gmx", "genion", "-s", "ions.tpr", "-o", "structure_solv_ions.gro", "-p", "topol.top", 
               "-pname", "NA", "-nname", "CL", "-neutral", "-conc", "0.15"]
    input_text = "14\n"
    run_command(command, input_text)
    command = ["gmx", "make_ndx", "-f", "structure_solv_ions.gro", "-o", "index.ndx"]
    input_text = "name 19 SOLV\n1 | 12\nname 20 SOLU\nq\n"
    run_command(command, input_text)

    mini_prefix = "step4.0_minimization"
    
    init = "structure_solv_ions"
    topol_file = "topol.top"
    gro_file = f"{init}.gro"
    
    command = ["gmx", "grompp", "-v", "-f", f"{mini_prefix}.mdp", "-o", f"{mini_prefix}.tpr", 
               "-c", gro_file, "-r", gro_file, "-p", topol_file, "-n", "index.ndx", "-maxwarn", "5", "-ntomp", "28", "-nb", "cpu"]
    run_command(command)
    command = ["gmx", "mdrun", "-v", "-deffnm", mini_prefix, "-ntmpi", "1"]
    run_command(command)


start_time = time.time()
run_gromacs_commands()
end_time = time.time()
elapsed_time = (end_time - start_time) / 60
print(f"{elapsed_time}",flush=True)


