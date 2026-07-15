"""Utility functions for data processing and model inference"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List
from app.logger import logger


class DataValidator:
    """Validate and sanitize input data"""

    @staticmethod
    def validate_match_data(data: Dict[str, Any]) -> bool:
        """Validate match prediction input"""
        required_fields = ["team1", "team2", "venue", "season"]
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_score_data(data: Dict[str, Any]) -> bool:
        """Validate score prediction input"""
        required_fields = ["current_runs", "current_wickets", "overs_completed", "target"]
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_player_data(data: Dict[str, Any]) -> bool:
        """Validate player stats prediction input"""
        required_fields = ["player_name", "role", "recent_form"]
        return all(field in data for field in required_fields)


class DataProcessor:
    """Process and transform data for models"""

    @staticmethod
    def normalize_features(features: np.ndarray) -> np.ndarray:
        """Normalize features to 0-1 range"""
        min_val = features.min()
        max_val = features.max()
        if max_val - min_val == 0:
            return np.zeros_like(features)
        return (features - min_val) / (max_val - min_val)

    @staticmethod
    def standardize_features(features: np.ndarray) -> np.ndarray:
        """Standardize features to mean 0, std 1"""
        mean = features.mean()
        std = features.std()
        if std == 0:
            return np.zeros_like(features)
        return (features - mean) / std

    @staticmethod
    def create_feature_vector(data: Dict[str, Any]) -> np.ndarray:
        """Convert dictionary to feature vector"""
        try:
            features = []
            for key in sorted(data.keys()):
                value = data[key]
                if isinstance(value, (int, float)):
                    features.append(float(value))
                elif isinstance(value, str):
                    # Simple hash-based encoding for strings
                    features.append(float(hash(value) % 100))
            return np.array(features)
        except Exception as e:
            logger.error(f"Feature vector creation failed: {str(e)}")
            return np.array([])


class ModelUtils:
    """Model loading and inference utilities"""

    @staticmethod
    def ensemble_predictions(predictions: List[float]) -> float:
        """Average ensemble predictions"""
        return np.mean(predictions) if predictions else 0.0

    @staticmethod
    def calibrate_probability(prob: float, min_prob: float = 0.1, max_prob: float = 0.9) -> float:
        """Calibrate probability to reasonable bounds"""
        return max(min_prob, min(max_prob, prob))

    @staticmethod
    def format_prediction_response(
        prediction: float,
        confidence: float,
        prediction_type: str
    ) -> Dict[str, Any]:
        """Format model prediction into response"""
        return {
            "prediction": round(prediction, 4),
            "confidence": round(confidence, 4),
            "type": prediction_type,
            "timestamp": pd.Timestamp.now().isoformat(),
        }
