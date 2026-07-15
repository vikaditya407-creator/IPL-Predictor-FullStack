"""Random Forest models for player statistics prediction"""

import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
from typing import Dict, Tuple, Optional
from pathlib import Path
from app.logger import logger


class PlayerStatsPredictor:
    """Random Forest models for predicting player statistics"""

    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        self.models = {}  # Dict to store multiple models
        self.feature_names = None
        logger.info("PlayerStatsPredictor initialized")

    def build_model(
        self,
        stat_type: str = "runs",  # runs, strike_rate, wickets, economy
        n_estimators: int = 100,
        max_depth: int = 15,
        **rf_params
    ) -> object:
        """Create Random Forest model for specific player stat"""
        
        if stat_type in ["runs", "strike_rate", "economy", "average"]:
            # Regression models
            default_params = {
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "random_state": 42,
                "n_jobs": -1,
            }
            default_params.update(rf_params)
            model = RandomForestRegressor(**default_params)
        else:
            # Classification models (e.g., likely_to_get_out)
            default_params = {
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "random_state": 42,
                "n_jobs": -1,
            }
            default_params.update(rf_params)
            model = RandomForestClassifier(**default_params)

        self.models[stat_type] = model
        logger.info(f"Random Forest model created for {stat_type}")
        return model

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        stat_type: str = "runs",
        feature_names: list = None,
    ) -> Dict:
        """Train model for specific player statistic"""
        if stat_type not in self.models:
            self.build_model(stat_type)

        if feature_names:
            self.feature_names = feature_names

        model = self.models[stat_type]

        logger.info(f"Training {stat_type} predictor: {len(X_train)} samples, {X_train.shape[1]} features")

        model.fit(X_train, y_train)

        logger.info(f"{stat_type} training complete")
        return self.evaluate(stat_type, X_train, y_train, X_val, y_val)

    def evaluate(self, stat_type: str, X_train, y_train, X_val, y_val) -> Dict:
        """Evaluate model"""
        model = self.models[stat_type]

        train_pred = model.predict(X_train)
        val_pred = model.predict(X_val)

        metrics = {
            "stat_type": stat_type,
            "train_r2": r2_score(y_train, train_pred),
            "val_r2": r2_score(y_val, val_pred),
            "train_mae": mean_absolute_error(y_train, train_pred),
            "val_mae": mean_absolute_error(y_val, val_pred),
            "train_rmse": np.sqrt(mean_squared_error(y_train, train_pred)),
            "val_rmse": np.sqrt(mean_squared_error(y_val, val_pred)),
        }

        logger.info(f"{stat_type} - Val R²={metrics['val_r2']:.4f}, Val MAE={metrics['val_mae']:.2f}")

        return metrics

    def predict(self, stat_type: str, X: np.ndarray) -> np.ndarray:
        """Make predictions for specific stat"""
        if stat_type not in self.models:
            raise ValueError(f"Model for {stat_type} not trained")

        return self.models[stat_type].predict(X)

    def predict_player_stats(self, player_data: Dict, feature_names: list) -> Dict:
        """Predict all stats for a player"""
        # Convert dict to feature vector
        features = []
        for feature_name in feature_names:
            if feature_name in player_data:
                features.append(float(player_data[feature_name]))
            else:
                features.append(0.0)

        X = np.array([features])

        predictions = {}

        if "runs" in self.models:
            predictions["predicted_runs"] = int(self.predict("runs", X)[0])

        if "strike_rate" in self.models:
            predictions["predicted_strike_rate"] = float(self.predict("strike_rate", X)[0])

        if "wickets" in self.models:
            predictions["predicted_wickets"] = int(self.predict("wickets", X)[0])

        if "economy" in self.models:
            predictions["predicted_economy"] = float(self.predict("economy", X)[0])

        return predictions

    def get_feature_importance(self, stat_type: str, top_n: int = 10) -> Dict:
        """Get top N important features for a stat type"""
        if stat_type not in self.models:
            raise ValueError(f"Model for {stat_type} not trained")

        model = self.models[stat_type]
        importances = model.feature_importances_

        if self.feature_names:
            feature_importance = dict(zip(self.feature_names, importances))
        else:
            feature_importance = {f"feature_{i}": imp for i, imp in enumerate(importances)}

        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_features[:top_n])

    def save(self, name: str = "player_stats_rf") -> None:
        """Save all models to disk"""
        if not self.models:
            raise ValueError("No models to save")

        for stat_type, model in self.models.items():
            model_file = self.model_path / f"{name}_{stat_type}.pkl"
            with open(model_file, "wb") as f:
                pickle.dump(model, f)
            logger.info(f"Model saved: {model_file}")

    def load(self, name: str = "player_stats_rf") -> None:
        """Load models from disk"""
        import glob

        # Find all matching model files
        pattern = str(self.model_path / f"{name}_*.pkl")
        matching_files = glob.glob(pattern)

        for model_file in matching_files:
            stat_type = Path(model_file).stem.replace(f"{name}_", "")
            with open(model_file, "rb") as f:
                self.models[stat_type] = pickle.load(f)
            logger.info(f"Model loaded: {model_file}")
