Last updated: **2026-05-06 11:17 EDT** 
# All notebooks have been rewritten and are now separated by dataset - on the landing page enter a dataset id (0-7) to access them individually, or `G` / `T` for the Gromacs and Training pipelines. Also included is the modified cif files and post-minimization gros at [http://4.bio250293.projects.jetstream-cloud.org/sirna-features/](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/). 

| Dataset | Description | Key features | Features | Ref. | Live notebook |
| --- | --- | --- | ---: | --- | --- |
| 0 | Distances calculated after modeling siRNA structures with chemical modifications. | Two molecular fingerprints containing dinucleotide at positions 3-4 and a monomer at position 7; distances calculated after trajectories. | 896 | 4f3t | [Dataset 0](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_0_pipeline.ipynb) |
| 1 | After modeling, full xyz coordinates of each residue stored as features. | Coordinates of all protein and RNA residues; no fingerprints; trajectories. | 2637 | 4f3t | [Dataset 1](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_1_pipeline.ipynb) |
| 2 | Simple RNA encoding of guide strand and predicted target with numerical modification indicators. | Encodings: A = 1, C = 2, G = 3, U = 4, dimer = 5-6, monomer = 7. | 42 | None | [Dataset 2](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_2_pipeline.ipynb) |
| 3 | Extended Connectivity Fingerprints (ECFPs) from guide strand and target sequences from alignments. | As Dataset 2, using fingerprints rather than simple numerical encoding. | 1344 | None | [Dataset 3](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_3_pipeline.ipynb) |
| 4 | Gene index data used as features; same fingerprints as Dataset 0. | Ensembl IDs as uint8 (gene index 0-2); fingerprints for positions 3-4, 7. | 99 | None | [Dataset 4](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_4_pipeline.ipynb) |
| 6N | Distances from minimized structures; pre-modeled structure used as reference. | Distances from pre-modeled base structure; RNA distances included. | 879 | Base | [Dataset 6/7](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_6_7_pipeline.ipynb) |
| 6R | As 6N but rescaled (0-255 range normalization). | Rescaled distances for comparability. | 842 | Base | [Dataset 6/7](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_6_7_pipeline.ipynb) |
| 7N | Distances from minimized structures; literature reference used. | Distances from the literature reference; no RNA distances. | 837 | 4f3t | [Dataset 6/7](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_6_7_pipeline.ipynb) |
| 7R | Same as 7N but rescaled. | Rescaled distances for comparability. | 800 | 4f3t | [Dataset 6/7](http://4.bio250293.projects.jetstream-cloud.org/sirna-features/jupyter/notebooks/dataset_6_7_pipeline.ipynb) |


Dataset 3, which uses ECFPs to encode siRNA and target features, is the current best-performing approach, while the minimized structural datasets still showed strong promise and could likely improve further with continued refinement.

![Figure 6 stack level and time optimization](.github/assets/figure6_stack_time.png)

The workflow consisted of three phases: experimental, bioinformatics, and machine learning, combining chemically modified siRNA production and RNA-Seq collection with structural prediction, molecular modeling, dynamics, and AutoGluon optimization.

![Figure 1 workflow](.github/assets/figure1_workflow_clean.png)


## Citation

If you use this work, please cite:

```bibtex
@article{richter2025sirnafeatures,
  title={siRNA Features-Automated Machine Learning of 3D Molecular Fingerprints and Structures for Therapeutic Off-Target Data},
  author={Richter, Michael and Admasu, Alem},
  journal={International Journal of Molecular Sciences},
  volume={26},
  number={14},
  pages={6795},
  year={2025},
  doi={10.3390/ijms26146795}
}
```
