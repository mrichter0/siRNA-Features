from setuptools import setup, find_packages

setup(
    name="sirna_features",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.2",
        "pandas>=1.2.0",
        "scipy>=1.6.0",
        "scikit-learn>=0.24.0",
        "torch>=1.8.0",
        "autogluon>=0.8.0",
        "rdkit>=2021.03.1",
        "biopython>=1.79",
        "chai-lab==0.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "isort>=5.8.0",
            "flake8>=3.9.2",
        ]
    },
    author="Michael Richter",
    author_email="richter@binghamton.edu",
    description="Reproducible Structure-Based Chemical Features for siRNA Off-Target Prediction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/siRNA-Features",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.8",
)