###
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

def run_command(command, input_text=None, max_chars=100):
    result = subprocess.run(command, capture_output=True, text=True, input=input_text)
    print(result.stdout)
    print(result.stderr)
    output = result.stdout + result.stderr
    for line in output.splitlines():
        if "warning" in line.lower() or "fatal" in line.lower():
            print(line) # print(line[:max_chars])
    
mini_prefix = "step4.0_minimization"
equi_prefix = "step4.0_minimization"
prod_prefix = "step5_production"
prod_step = "step5"

for i in range(20, 151):
    start_time = time.time()

    command = ["gmx", "grompp", "-v", "-f", f"{mini_prefix}.mdp", "-o", f"{mini_prefix}.tpr", 
               "-c", "structure_solv_ions.gro", "-r", "structure_solv_ions.gro", 
               "-p", "topol.top", "-n", "index.ndx", "-maxwarn", "5"]
    run_command(command)
    
    command = ["gmx", "mdrun", "-v", "-deffnm", mini_prefix, "-ntmpi", "1"]
    run_command(command)
    elapsed_time = time.time() - start_time
    print(f"Process {i} completed in {elapsed_time:.2f} seconds.")





