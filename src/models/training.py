"""
Model training module using AutoGluon.
"""

from typing import Dict, Optional, Union
import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor

class AutoGluonTrainer:
    """Trainer class using AutoGluon."""
    
    def __init__(self,
                 target_column: str = 'target',
                 eval_metric: str = 'roc_auc_ovo_macro',
                 time_limit: int = 3600):
        """Initialize trainer.
        
        Args:
            target_column: Name of target column
            eval_metric: Evaluation metric
            time_limit: Time limit in seconds
        """
        self.target_column = target_column
        self.eval_metric = eval_metric
        self.time_limit = time_limit
        self.predictor = None
        
    def train(self,
              train_data: pd.DataFrame,
              hyperparameters: Optional[Dict] = None,
              **kwargs) -> None:
        """Train models using AutoGluon.
        
        Args:
            train_data: Training data
            hyperparameters: Optional hyperparameter configurations
            **kwargs: Additional arguments passed to fit()
        """
        self.predictor = TabularPredictor(
            label=self.target_column,
            eval_metric=self.eval_metric,
            problem_type='binary'
        )
        
        self.predictor.fit(
            train_data,
            time_limit=self.time_limit,
            hyperparameters=hyperparameters,
            **kwargs
        )
        
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Generate predictions.
        
        Args:
            data: Input data
            
        Returns:
            Array of predictions
        """
        if self.predictor is None:
            raise ValueError("Model not trained")
            
        return self.predictor.predict(data)
    
    def evaluate(self, 
                test_data: pd.DataFrame,
                metrics: Optional[Union[str, List[str]]] = None) -> Dict:
        """Evaluate model performance.
        
        Args:
            test_data: Test data
            metrics: Metrics to evaluate
            
        Returns:
            Dictionary of evaluation results
        """
        if self.predictor is None:
            raise ValueError("Model not trained")
            
        return self.predictor.evaluate(test_data, metrics=metrics)
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance scores.
        
        Returns:
            DataFrame with feature importance scores
        """
        if self.predictor is None:
            raise ValueError("Model not trained")
            
        return self.predictor.feature_importance()