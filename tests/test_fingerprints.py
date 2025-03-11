"""
Tests for fingerprint generation module.
"""

import numpy as np
import pytest
from rdkit import Chem
from src.features import fingerprints

def test_generate_ecfp():
    # Test with valid SMILES
    mol = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
    fp = fingerprints.generate_ecfp(mol)
    assert isinstance(fp, np.ndarray)
    assert fp.shape == (256,)  # Default nbits
    
    # Test with invalid SMILES
    with pytest.raises(ValueError):
        fingerprints.generate_ecfp("invalid_smiles")
        
def test_process_monomer():
    # Test with nucleotide
    monomer = "CC1=CN(C2CC(O)C(CO)O2)C(=O)NC1=O"  # Thymidine
    fp = fingerprints.process_monomer(monomer)
    assert isinstance(fp, np.ndarray)
    assert fp.shape == (256,)
    
def test_compress_fingerprint():
    # Test compression
    fp = np.ones(256, dtype=bool)
    compressed = fingerprints.compress_fingerprint(fp)
    assert isinstance(compressed, np.ndarray)
    assert compressed.dtype == np.uint8
    assert len(compressed) == 32  # 256/8