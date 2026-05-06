import subprocess
import shutil
import os
import pandas as pd
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python script.py <gpu_index>", flush=True)
    sys.exit(1)

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
    # print(result.stdout)
    # print(result.stderr)
    output = result.stdout + result.stderr
    for line in output.splitlines():
        if "warning" in line.lower() or "fatal" in line.lower():
            print(line) # print(line[:max_chars])
    
mini_prefix = "step4.0_minimization"
equi_prefix = "step4.0_minimization"
prod_prefix = "step5_production"
prod_step = "step5"

start_time = time.time()
for i in range(1, 1001):

    command = ["gmx", "grompp", "-v", "-f", f"{mini_prefix}.mdp", "-o", f"{mini_prefix}.tpr", 
               "-c", "structure_solv_ions.gro", "-r", "structure_solv_ions.gro", 
               "-p", "topol.top", "-n", "index.ndx", "-maxwarn", "5"]
    run_command(command)
    
    command = ["gmx", "mdrun", "-v", "-deffnm", mini_prefix, "-ntmpi", "1"]
    run_command(command)

    command_grompp = ["gmx", "grompp", "-f", f"{prod_prefix}.mdp", "-o", f"{prod_step}.tpr",
                      "-c", f"{equi_prefix}.gro", "-p", "topol.top", "-n", "index.ndx"]
    run_command(command_grompp)
    
    command_mdrun = ["gmx", "mdrun", "-v", "-deffnm", prod_step, "-ntmpi", "1"]
    run_command(command_mdrun)


    mv_command = ["mv", "step4.0_minimization.gro", f"step4.0_minimization_{i}.gro"]
    run_command(mv_command)
    mv_command = ["mv", "step5.gro", f"step5_{i}.gro"]
    run_command(mv_command)

    if i % 10 == 0:
        end_time = time.time()
        elapsed_time = (end_time - start_time) / 60
        print(f"{elapsed_time}", flush=True)
        start_time = time.time()
