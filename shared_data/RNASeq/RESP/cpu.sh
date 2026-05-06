#!/bin/bash
#SBATCH --job-name=nwchem
#SBATCH --output=output.nw
#SBATCH --error=error.nw
#SBATCH --partition=Standard
#SBATCH --time=48:00:00
#SBATCH --mem=62000
#SBATCH --cpus-per-task=28
#SBATCH --nodelist=chpc098
##SBATCH --ntasks=1

mpirun --map-by :OVERSUBSCRIBE -np 28 nwchem inputs/simple_test4f.inp
