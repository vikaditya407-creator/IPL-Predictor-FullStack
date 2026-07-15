"""XGBoost model for match winner prediction"""

import numpy as np
import pandas as pd
import xgboost as xgb
import pickle
from typing import Tuple, Dict, Optional
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from app.logger import logger


class MatchWinnerPredictor:
    """XGBoost model for predicting match winners"""

    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        self.model = None
        self.feature_names = None
        self.feature_importance = None
        logger.info("MatchWinnerPredictor initialized")

    def build_model(self, **xgb_params) -> xgb.XGBClassifier:
        """Create XGBoost model with specified parameters"""
        default_params = {
            "n_estimators": 100,
            "max_depth": 7,
            "learning_rate": 0.1,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "objective": "binary:logistic",
            "eval_metric": "logloss",
            "random_state": 42,
            "verbosity": 0,
        }
        default_params.update(xgb_params)

        self.model = xgb.XGBClassifier(**default_params)
        logger.info(f"XGBoost model created with params: {default_params}")
        return self.model

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        feature_names: list = None,
    ) -> Dict:
        """Train the model with validation data"""
        if self.model is None:
            self.build_model()

        self.feature_names = feature_names or [f"feature_{i}" for i in range(X_train.shape[1])]

        logger.info(f"Training XGBoost: {X_train.shape[0]} samples, {X_train.shape[1]} features")

        # Train with early stopping
        self.model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=10,
            verbose=False,
        )

        # Get feature importance
        self.feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))

        logger.info("Training complete")
        return self.evaluate(X_train, y_train, X_val, y_val)

    def evaluate(self, X_train, y_train, X_val, y_val) -> Dict:
        """Evaluate model on train and validation sets"""
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)
        train_proba = self.model.predict_proba(X_train)[:, 1]
        val_proba = self.model.predict_proba(X_val)[:, 1]

        metrics = {
            "train_accuracy": accuracy_score(y_train, train_pred),
            "val_accuracy": accuracy_score(y_val, val_pred),
            "train_precision": precision_score(y_train, train_pred, zero_division=0),
            "val_precision": precision_score(y_val, val_pred, zero_division=0),
            "train_recall": recall_score(y_train, train_pred, zero_division=0),
            "val_recall": recall_score(y_val, val_pred, zero_division=0),
            "train_f1": f1_score(y_train, train_pred, zero_division=0),
            "val_f1": f1_score(y_val, val_pred, zero_division=0),
            "train_auc": roc_auc_score(y_train, train_proba),
            "val_auc": roc_auc_score(y_val, val_proba),
        }

        logger.info(f"Metrics: Train Acc={metrics['train_accuracy']:.4f}, Val Acc={metrics['val_accuracy']:.4f}")
        logger.info(f"         Train AUC={metrics['train_auc']:.4f}, Val AUC={metrics['val_auc']:.4f}")

        return metrics

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")

        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[:, 1]
        return predictions, probabilities

    def save(self, name: str = "match_winner_xgboost") -> None:
        """Save model to disk"""
        if self.model is None:
            raise ValueError("No model to save")

        model_file = self.model_path / f"{name}.pkl"
        with open(model_file, "wb") as f:
            pickle.dump(self.model, f)

        # Save metadata
        metadata_file = self.model_path / f"{name}_metadata.pkl"
        metadata = {
            "feature_names": self.feature_names,
            "feature_importance": self.feature_importance,
        }
        with open(metadata_file, "wb") as f:
            pickle.dump(metadata, f)

        logger.info(f"Model saved: {model_file}")

    def load(self, name: str = "match_winner_xgboost") -> None:
        """Load model from disk"""
        model_file = self.model_path / f"{name}.pkl"
        with open(model_file, "rb") as f:
            self.model = pickle.load(f)

        # Load metadata
        metadata_file = self.model_path / f"{name}_metadata.pkl"
        with open(metadata_file, "rb") as f:
            metadata = pickle.load(f)
            self.feature_names = metadata["feature_names"]
            self.feature_importance = metadata["feature_importance"]

        logger.info(f"Model loaded: {model_file}")

    def get_feature_importance(self, top_n: int = 10) -> Dict:
        """Get top N important features"""
        if self.feature_importance is None:
            raise ValueError("Model not trained")

        sorted_features = sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_features[:top_n])

    def predict_match(self, match_data: Dict, scaler=None) -> Dict:
        """Predict winner for a single match"""
        # Convert dict to feature vector
        features = []
        for feature_name in self.feature_names:
            if feature_name in match_data:
                features.append(float(match_data[feature_name]))
            else:
                features.append(0.0)

        X = np.array([features])

        if scaler:
            X = scaler.transform(X)

        pred, prob = self.predict(X)

        return {
            "team1_win_probability": float(prob[0]),
            "team2_win_probability": float(1 - prob[0]),
            "predicted_team1_wins": bool(pred[0]),
            "confidence": float(max(prob[0], 1 - prob[0])),
        }
