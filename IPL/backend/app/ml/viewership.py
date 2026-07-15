"""Linear Regression model for viewership estimation"""

import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Tuple
from pathlib import Path
from app.logger import logger


class ViewershipEstimator:
    """Linear Regression model for predicting IPL viewership"""

    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        self.model = None
        self.poly_features = None
        self.feature_names = None
        logger.info("ViewershipEstimator initialized")

    def build_model(self, use_polynomial: bool = False, poly_degree: int = 2) -> LinearRegression:
        """Build Linear Regression model"""
        self.model = LinearRegression()

        if use_polynomial:
            self.poly_features = PolynomialFeatures(degree=poly_degree)
            logger.info(f"ViewershipEstimator with polynomial features (degree={poly_degree})")
        else:
            logger.info("ViewershipEstimator with linear features")

        return self.model

    def prepare_features(self, X: np.ndarray, fit: bool = False) -> np.ndarray:
        """Apply polynomial transformation if configured"""
        if self.poly_features is None:
            return X

        if fit:
            return self.poly_features.fit_transform(X)
        else:
            return self.poly_features.transform(X)

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        feature_names: list = None,
        use_polynomial: bool = False,
    ) -> Dict:
        """Train the linear regression model"""
        if self.model is None:
            self.build_model(use_polynomial=use_polynomial)

        self.feature_names = feature_names or [f"feature_{i}" for i in range(X_train.shape[1])]

        # Prepare features
        X_train_prepared = self.prepare_features(X_train, fit=True)
        X_val_prepared = self.prepare_features(X_val, fit=False)

        logger.info(f"Training viewership model: {len(X_train)} samples, {X_train_prepared.shape[1]} features")

        self.model.fit(X_train_prepared, y_train)

        logger.info("Training complete")
        return self.evaluate(X_train_prepared, y_train, X_val_prepared, y_val)

    def evaluate(self, X_train, y_train, X_val, y_val) -> Dict:
        """Evaluate model on train and validation sets"""
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)

        metrics = {
            "train_r2": r2_score(y_train, train_pred),
            "val_r2": r2_score(y_val, val_pred),
            "train_mae": mean_absolute_error(y_train, train_pred),
            "val_mae": mean_absolute_error(y_val, val_pred),
            "train_rmse": np.sqrt(mean_squared_error(y_train, train_pred)),
            "val_rmse": np.sqrt(mean_squared_error(y_val, val_pred)),
        }

        logger.info(f"Metrics: Train R²={metrics['train_r2']:.4f}, Val R²={metrics['val_r2']:.4f}")
        logger.info(f"         Train MAE={metrics['train_mae']:.0f}, Val MAE={metrics['val_mae']:.0f}")

        return metrics

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained")

        X_prepared = self.prepare_features(X, fit=False)
        return self.model.predict(X_prepared)

    def save(self, name: str = "viewership_regression") -> None:
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save")

        model_file = self.model_path / f"{name}.pkl"
        with open(model_file, "wb") as f:
            pickle.dump(self.model, f)

        # Save preprocessing info
        metadata_file = self.model_path / f"{name}_metadata.pkl"
        metadata = {
            "feature_names": self.feature_names,
            "poly_features": self.poly_features,
        }
        with open(metadata_file, "wb") as f:
            pickle.dump(metadata, f)

        logger.info(f"Model saved: {model_file}")

    def load(self, name: str = "viewership_regression") -> None:
        """Load model from disk"""
        model_file = self.model_path / f"{name}.pkl"
        with open(model_file, "rb") as f:
            self.model = pickle.load(f)

        # Load preprocessing info
        metadata_file = self.model_path / f"{name}_metadata.pkl"
        with open(metadata_file, "rb") as f:
            metadata = pickle.load(f)
            self.feature_names = metadata["feature_names"]
            self.poly_features = metadata["poly_features"]

        logger.info(f"Model loaded: {model_file}")

    def estimate_viewership(self, match_data: Dict) -> Dict:
        """Estimate viewership for a match"""
        # Convert dict to feature vector
        features = []
        for feature_name in self.feature_names:
            if feature_name in match_data:
                features.append(float(match_data[feature_name]))
            else:
                features.append(0.0)

        X = np.array([features])

        prediction = self.predict(X)[0]

        return {
            "predicted_live_viewers": int(max(0, prediction * 0.7)),  # Estimate 70% watching live
            "predicted_total_viewers": int(max(0, prediction)),
            "confidence": 0.75,
            "model_version": "linear_v1",
        }

    def get_coefficients(self) -> Dict:
        """Get model coefficients for interpretability"""
        if self.model is None or self.feature_names is None:
            raise ValueError("Model not trained")

        # For linear model
        if len(self.model.coef_) == len(self.feature_names):
            coefficients = dict(zip(self.feature_names, self.model.coef_))
        else:
            # For polynomial features, map back to original features if possible
            coefficients = {f"coef_{i}": coef for i, coef in enumerate(self.model.coef_)}

        coefficients["intercept"] = float(self.model.intercept_)
        return coefficients
