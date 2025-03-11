"""
Quick start example for siRNA-Features.
"""

import pandas as pd
from src.features import dataset_builder
from src.models import training

def main():
    # Load example data
    sequences = [
        "GCAAGCTGACCCTGAAGTTCAT",
        "GGACTCAGATCTCGAGCTCAAG",
    ]
    
    modifications = [
        {3: {"type": "amide", "position": "backbone"}},
        {7: {"type": "gna", "position": "sugar"}},
    ]
    
    targets = [
        "ATGAACTTCAGGGTCAGCTTGC",
        "CTTGAGCTCGAGATCTGAGTCC",
    ]
    
    # Create dataset builder
    builder = dataset_builder.DatasetBuilder()
    
    # Generate Dataset 3 features
    features_df = builder.create_dataset_3(sequences, modifications, targets)
    
    # Add target column (dummy values for example)
    features_df['target'] = [0, 1]
    
    # Initialize and train model
    model = training.AutoGluonTrainer(
        target_column='target',
        time_limit=600  # 10 minutes
    )
    
    # Train model
    model.train(features_df)
    
    # Get feature importance
    importance = model.get_feature_importance()
    print("\nFeature Importance:")
    print(importance.head())
    
    # Make predictions on new data
    predictions = model.predict(features_df)
    print("\nPredictions:")
    print(predictions)

if __name__ == "__main__":
    main()