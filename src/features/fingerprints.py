"""
ECFP generation module for siRNA modifications.
"""

from typing import List, Union
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

def generate_ecfp(mol: Union[str, Chem.Mol], 
                 nbits: int = 256,
                 radius: int = 1) -> np.ndarray:
    """Generate ECFP fingerprint for molecule.
    
    Args:
        mol: Input molecule as SMILES string or RDKit Mol object
        nbits: Number of bits in fingerprint
        radius: Radius for Morgan fingerprint
        
    Returns:
        Binary numpy array of fingerprint
    """
    if isinstance(mol, str):
        mol = Chem.MolFromSmiles(mol)
    
    if mol is None:
        raise ValueError("Invalid molecule")
        
    fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=nbits)
    return np.array(fingerprint)

def process_monomer(monomer: Union[str, Chem.Mol],
                   remove_hydrogens: bool = True) -> np.ndarray:
    """Process single RNA monomer for fingerprint generation.
    
    Args:
        monomer: Input monomer structure
        remove_hydrogens: Whether to remove hydrogens before fingerprinting
        
    Returns:
        Fingerprint array
    """
    if isinstance(monomer, str):
        mol = Chem.MolFromSmiles(monomer)
    else:
        mol = monomer
        
    if remove_hydrogens:
        mol = Chem.RemoveHs(mol)
        
    return generate_ecfp(mol)

def process_dimer(dimer: Union[str, Chem.Mol],
                 nbits: int = 512,
                 radius: int = 2) -> np.ndarray:
    """Process RNA dimer for fingerprint generation.
    
    Args:
        dimer: Input dimer structure
        nbits: Number of bits
        radius: Morgan fingerprint radius
        
    Returns:
        Fingerprint array
    """
    if isinstance(dimer, str):
        mol = Chem.MolFromSmiles(dimer)
    else:
        mol = dimer
        
    return generate_ecfp(mol, nbits=nbits, radius=radius)

def compress_fingerprint(fp: np.ndarray) -> np.ndarray:
    """Compress binary fingerprint to uint8 array.
    
    Args:
        fp: Binary fingerprint array
        
    Returns:
        Compressed uint8 array
    """
    return np.packbits(fp.astype(bool))