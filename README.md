[Datasets are now available at this link](https://binghamton-my.sharepoint.com/:u:/g/personal/mrichte3_binghamton_edu/EbXq_8BXbx5Ni-6pfzaYEecBth-tEwPrjvfDZ1J_QlviEg?e=9LmXRA)

# siRNA-Features

This repository contains the code and data accompanying the paper "siRNA Features - Reproducible Structure-Based Chemical Features for Off-Target Prediction".

[![Paper](https://img.shields.io/badge/paper-link-blue)](paper_link)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

This project introduces a framework for generating reproducible structure-based chemical features for siRNA, incorporating both molecular fingerprints and computationally derived siRNA-AGO2 complex structures. The framework enables better prediction of off-target effects in siRNA therapeutics through advanced feature engineering and machine learning approaches.

## Key Features

- Structural prediction and modeling of siRNA-AGO2 complexes
- Extended Connectivity Fingerprint (ECFP) generation for siRNA modifications
- Multiple feature representation strategies (9 distinct datasets)
- Machine learning pipeline using AutoGluon
- Reproducible molecular dynamics simulations

## Installation

```bash
# Clone the repository
git clone https://github.com/username/siRNA-Features.git
cd siRNA-Features

# Create and activate a conda environment
conda create -n sirna_features python=3.8
conda activate sirna_features

# Install dependencies
pip install -r requirements.txt
```

## Project Structure

```
siRNA-Features/
├── data/                    # Dataset storage
│   ├── raw/                # Raw RNA-Seq data
│   └── processed/          # Processed features and results
├── docs/                   # Documentation
├── models/                 # Trained models
├── notebooks/             # Jupyter notebooks
│   ├── RNASeq/            # RNA-Seq analysis notebooks
│   ├── alignments/        # Structure alignment notebooks
│   └── modifications/     # Chemical modification notebooks
├── src/                   # Source code
│   ├── features/          # Feature generation
│   ├── models/           # Model training and evaluation
│   └── utils/            # Utility functions
├── tests/                # Unit tests
├── LICENSE
└── README.md
```

## Usage

### Feature Generation

1. **Structural Prediction**:
```python
from src.features import structural_prediction
model = structural_prediction.ChaiDiscovery()
structure = model.predict_structure(sequence)
```

2. **ECFP Generation**:
```python
from src.features import fingerprints
ecfps = fingerprints.generate_ecfp(molecule, nbits=512, radius=2)
```

3. **Dataset Creation**:
```python
from src.features import dataset_builder
dataset = dataset_builder.create_dataset(structure, ecfps, type="dataset3")
```

### Model Training

```python
from src.models import training
model = training.AutoGluonTrainer(dataset)
model.train()
```

## Datasets

The datasets used in this study are available at:
- RNA-Seq dataset: [Dataset Link]
- Processed features: [Features Link](https://binghamton-my.sharepoint.com/:u:/g/personal/mrichte3_binghamton_edu/EbXq_8BXbx5Ni-6pfzaYEecBth-tEwPrjvfDZ1J_QlviEg?e=9LmXRA)
- Pre-trained models: [Models Link]

## Results

Our framework achieved:
- AUPRC scores up to 0.784 (Dataset 3)
- Robust performance across multiple feature representations
- Reproducible structural predictions

## Citation

If you use this code or find our work helpful, please cite:

```bibtex
@article{richter2024sirna,
  title={siRNA Features - Reproducible Structure-Based Chemical Features for Off-Target Prediction},
  author={Richter, Michael and Admasub, Alem},
  journal={Journal Name},
  year={2024}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## Contact

- Michael Richter - richter@binghamton.edu
- Alem Admasub - alem@rutgers.edu
