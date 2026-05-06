#!/bin/bash
#SBATCH --job-name=md2
#SBATCH --output=output.md2
#SBATCH --error=error.md2
#SBATCH --partition=gpucompute-a40
#SBATCH --gres=gpu:1
#SBATCH --time=50:00:00
#SBATCH --mem=120000
#SBATCH --cpus-per-task=6

module load cuda/12.4
module load gnu13/13.2.0

python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
python 0minmd.py 0
