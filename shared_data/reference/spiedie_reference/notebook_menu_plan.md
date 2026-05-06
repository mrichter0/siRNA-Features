# Notebook Menu Plan

- Total notebooks mirrored: 65
- Main notebooks: 28
- Checkpoints: 37

## Recommended Menu

1. RNASeq Core
- RNASeq.ipynb [good_candidate_on_jetstream] tags=rnaseq,alignment needs=none
- RNASeq2.ipynb [good_candidate_on_jetstream] tags=rnaseq,alignment needs=none
- RNASeq3.ipynb [cluster_gpu_only] tags=rnaseq,alignment,gpu_or_modeling needs=chai_lab,torch,Bio,selenium
- RNASeq4.ipynb [cluster_gpu_only] tags=rnaseq,alignment,md,gpu_or_modeling needs=chai_lab,torch,Bio,matplotlib_venn

2. Chai / Structure Generation
- chai.ipynb [cluster_gpu_only] tags=gpu_or_modeling needs=chai_lab,torch
- chai2.ipynb [cluster_gpu_only] tags=alignment,gpu_or_modeling needs=chai_lab,torch

3. Alignment / Structure Comparison
- test_alignment/a_modeling.ipynb [cluster_or_special_env] tags=alignment,md,gpu_or_modeling needs=pymol
- test_alignment/alignments.ipynb [cluster_or_special_env] tags=rnaseq,alignment,md,gpu_or_modeling needs=pymol
- test_alignment/alignments2.ipynb [cluster_or_special_env] tags=rnaseq,alignment,md,gpu_or_modeling needs=pymol
- test_alignment/alignments3.ipynb [cluster_or_special_env] tags=rnaseq,alignment,md,gpu_or_modeling needs=pymol

4. Feature Engineering / Datasets
- test_alignment/md0/Untitled.ipynb [good_candidate_on_jetstream] tags=rnaseq,alignment needs=none
- test_alignment/md0/features.ipynb [cluster_or_special_env] tags=rnaseq,alignment,md needs=pymol,rdkit
- test_alignment/md0/features2.ipynb [good_candidate_on_jetstream] tags=rnaseq,alignment needs=none
- test_alignment/md0/temp/1.ipynb [cluster_or_special_env] tags=rnaseq,alignment,md needs=pymol2

5. MD / Reproducibility / Batch Prep
- test_alignment/md/working_folder_amide/amide.ipynb [cluster_or_special_env] tags=rnaseq,md,gpu_or_modeling needs=pymol
- test_alignment/md/working_folder_amide2/amide2.ipynb [data_only_on_jetstream] tags=rnaseq,md,gpu_or_modeling needs=none
- test_alignment/md/working_folder_amide3/amide3.ipynb [data_only_on_jetstream] tags=rnaseq,md,gpu_or_modeling needs=none
- test_alignment/md/working_folder_amide4/amide4.ipynb [data_only_on_jetstream] tags=rnaseq,md,gpu_or_modeling needs=none
- test_alignment/md/working_folder_gna/gna.ipynb [data_only_on_jetstream] tags=rnaseq,md needs=none
- test_alignment/md/working_folder_gna/working.ipynb [data_only_on_jetstream] tags=rnaseq,md needs=none
- test_alignment/md/working_folder_gna2/gna2.ipynb [data_only_on_jetstream] tags=rnaseq,md needs=none
- test_alignment/md/working_folder_unmod/unmod.ipynb [data_only_on_jetstream] tags=rnaseq,md needs=none
- test_alignment/md0/reproducible.ipynb [cluster_or_special_env] tags=rnaseq,alignment,md,gpu_or_modeling needs=pymol
- test_alignment/md0/reproducible2.ipynb [cluster_or_special_env] tags=rnaseq,alignment,md,gpu_or_modeling needs=pymol
- test_alignment/md2/md2.ipynb [data_only_on_jetstream] tags=rnaseq,md,gpu_or_modeling needs=none
- test_alignment/md3/md3.ipynb [data_only_on_jetstream] tags=rnaseq,md,gpu_or_modeling needs=none
- test_alignment/md4/md4.ipynb [data_only_on_jetstream] tags=rnaseq,md,gpu_or_modeling needs=none
- test_alignment/md5/fix.ipynb [data_only_on_jetstream] tags=rnaseq,md,gpu_or_modeling needs=none

## Serve Guidance

- good_candidate_on_jetstream: likely fine on the current Jetstream Jupyter service with normal Python/data packages.
- data_only_on_jetstream: can be served for reading or light dataframe work, but not full MD reproduction without the original binaries/filesystem assumptions.
- cluster_or_special_env: depends on PyMOL or similar special desktop/scientific packages; better treated as archive/reference unless we build that env explicitly.
- cluster_gpu_only: depends on Chai and/or Torch CUDA workflow; keep as archive/reference on Jetstream and run on GPU-backed cluster/instance only.

## First Pass Recommendation

- Default menu should expose only RNASeq Core + Feature Engineering / Datasets.
- Put Chai / Structure Generation and MD / Reproducibility behind an Advanced or Archive section.
- Hide checkpoints from the UI entirely.
