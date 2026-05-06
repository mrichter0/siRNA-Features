import subprocess
import os
os.environ['PATH'] = '/data/home/mrichte3/gromacs-2024.2/install/bin:' + os.environ['PATH']
if 'LD_LIBRARY_PATH' in os.environ:
    os.environ['LD_LIBRARY_PATH'] = '/data/home/mrichte3/gromacs-2024.2/install/lib:' + os.environ['LD_LIBRARY_PATH']
else:
    os.environ['LD_LIBRARY_PATH'] = '/data/home/mrichte3/gromacs-2024.2/install/lib'
os.environ['GMX_MAXBACKUP'] = '-1'

def run_command(command, input_text=None):
    """Run a shell command with optional input and capture output."""
    result = subprocess.run(command, capture_output=True, text=True, input=input_text)
    # print(result.stdout)
    # print(result.stderr)
    return result

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

run_gromacs_commands()
init = "structure_solv_ions"
mini_prefix = "step4.0_minimization"
topol_file = "topol.top"
gro_file = f"{init}.gro"

command = ["gmx", "grompp", "-v", "-f", f"{mini_prefix}.mdp", "-o", f"{mini_prefix}.tpr", 
           "-c", gro_file, "-r", gro_file, "-p", topol_file, "-n", "index.ndx", "-maxwarn", "5"]
run_command(command)
command = ["gmx", "mdrun", "-v", "-deffnm", mini_prefix, "-ntmpi", "1"]
run_command(command)

equi_prefix = "step4.1_equilibration"
command = ["gmx", "grompp", "-f", f"{equi_prefix}.mdp", "-o", f"{equi_prefix}.tpr", 
           "-c", f"{mini_prefix}.gro", "-r", f"{init}.gro", "-p", "topol.top", "-maxwarn", "1", "-n", "index.ndx"]
run_command(command)
command = ["gmx", "mdrun", "-v", "-deffnm", equi_prefix, "-ntmpi", "1"]
run_command(command)


prod_prefix = "step5_production"
prod_step = "step5"
import time
start_time = time.time()
command_grompp = ["gmx", "grompp", "-f", f"{prod_prefix}.mdp", "-o", f"{prod_step}.tpr",
                  "-c", f"{equi_prefix}.gro", "-p", "topol.top", "-maxwarn", "2", "-n", "index.ndx"]
run_command(command_grompp)

command_mdrun = ["gmx", "mdrun", "-v", "-deffnm", prod_step, "-ntmpi", "1"]
run_command(command_mdrun)
end_time = time.time()
elapsed_time = (end_time - start_time) / 60
print(f"{elapsed_time}")

