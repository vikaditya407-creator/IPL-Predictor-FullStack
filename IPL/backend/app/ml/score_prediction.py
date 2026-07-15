"""Score prediction model for cricket score prediction"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, Optional
from pathlib import Path
import pickle
from app.logger import logger


class ScorePredictor:
    """Score prediction model for predicting cricket match scores"""

    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        self.model = None
        self.scaler = StandardScaler()
        self.history = None
        logger.info("ScorePredictor initialized")

    def build_model(
        self,
        n_estimators: int = 200,
        learning_rate: float = 0.1,
        max_depth: int = 6,
    ) -> GradientBoostingRegressor:
        """Build tree-based regression model for score prediction"""
        self.model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=42,
        )

        logger.info(
            f"GradientBoostingRegressor built with n_estimators={n_estimators}, "
            f"learning_rate={learning_rate}, max_depth={max_depth}"
        )
        return self.model

    def prepare_sequences(self, data: np.ndarray, lookback: int = 6) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare sequences for regression from flat data"""
        X, y = [], []

        for i in range(len(data) - lookback):
            sequence = data[i : i + lookback].flatten()
            X.append(sequence)
            y.append(data[i + lookback, 0])

        return np.array(X), np.array(y)

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        n_estimators: int = 200,
        learning_rate: float = 0.1,
        max_depth: int = 6,
    ) -> Dict:
        """Train the score prediction model"""
        if self.model is None:
            self.build_model(
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                max_depth=max_depth,
            )

        if X_train.ndim == 3:
            X_train = X_train.reshape(X_train.shape[0], -1)
            X_val = X_val.reshape(X_val.shape[0], -1)

        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)

        logger.info(f"Training score regressor: {len(X_train_scaled)} samples, shape {X_train_scaled.shape}")

        self.model.fit(X_train_scaled, y_train)

        logger.info("Training complete")
        return self.evaluate(X_train_scaled, y_train, X_val_scaled, y_val)

    def evaluate(self, X_train, y_train, X_val, y_val) -> Dict:
        """Evaluate model on train and validation sets"""
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)

        metrics = {
            "train_mse": mean_squared_error(y_train, train_pred),
            "val_mse": mean_squared_error(y_val, val_pred),
            "train_rmse": np.sqrt(mean_squared_error(y_train, train_pred)),
            "val_rmse": np.sqrt(mean_squared_error(y_val, val_pred)),
            "train_mae": mean_absolute_error(y_train, train_pred),
            "val_mae": mean_absolute_error(y_val, val_pred),
            "train_r2": r2_score(y_train, train_pred),
            "val_r2": r2_score(y_val, val_pred),
        }

        logger.info(
            f"Metrics: Train RMSE={metrics['train_rmse']:.2f}, Val RMSE={metrics['val_rmse']:.2f}"
        )
        logger.info(
            f"         Train MAE={metrics['train_mae']:.2f}, Val MAE={metrics['val_mae']:.2f}"
        )

        return metrics

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained")

        if X.ndim == 3:
            X = X.reshape(X.shape[0], -1)

        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def save(self, name: str = "score_predictor") -> None:
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save")

        model_file = self.model_path / f"{name}.pkl"
        with open(model_file, "wb") as f:
            pickle.dump({"model": self.model, "scaler": self.scaler}, f)

        logger.info(f"Model saved: {model_file}")

    def load(self, name: str = "score_predictor") -> None:
        """Load model from disk"""
        model_file = self.model_path / f"{name}.pkl"
        with open(model_file, "rb") as f:
            data = pickle.load(f)

        self.model = data["model"]
        self.scaler = data["scaler"]
        logger.info(f"Model loaded: {model_file}")

    def predict_score(self, current_data: np.ndarray) -> Dict:
        """Predict final score from current match state"""
        if self.model is None:
            raise ValueError("Model not trained")

        if current_data.ndim == 1:
            X = current_data.reshape(1, -1)
        else:
            X = current_data.reshape(1, -1)

        prediction = float(self.predict(X)[0])

        return {
            "predicted_final_score": int(prediction),
            "confidence_interval": {
                "lower": int(prediction * 0.9),
                "upper": int(prediction * 1.1),
            },
            "model_version": "regressor_v1",
        }
