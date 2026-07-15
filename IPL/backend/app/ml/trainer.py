"""MLflow integration for model tracking and versioning"""

import mlflow
import mlflow.xgboost
import mlflow.sklearn
import json
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
from app.config import get_settings
from app.logger import logger


class MLflowTracker:
    """MLflow wrapper for experiment tracking"""

    def __init__(self):
        self.settings = get_settings()
        mlflow.set_tracking_uri(self.settings.mlflow_tracking_uri)
        mlflow.set_experiment("IPL_Predictor")
        logger.info("MLflow tracker initialized")

    def start_run(self, run_name: str, tags: Dict[str, str] = None) -> str:
        """Start a new MLflow run"""
        run = mlflow.start_run(run_name=run_name)
        
        if tags:
            for key, value in tags.items():
                mlflow.set_tag(key, value)

        logger.info(f"MLflow run started: {run.info.run_id}")
        return run.info.run_id

    def log_params(self, params: Dict[str, Any]) -> None:
        """Log parameters"""
        for key, value in params.items():
            mlflow.log_param(key, value)
        logger.info(f"Logged {len(params)} parameters")

    def log_metrics(self, metrics: Dict[str, float], step: int = None) -> None:
        """Log metrics"""
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)
        logger.info(f"Logged {len(metrics)} metrics")

    def log_artifact(self, artifact_path: str, artifact_type: str = "file") -> None:
        """Log artifact"""
        if artifact_type == "directory":
            mlflow.log_artifacts(artifact_path)
        else:
            mlflow.log_artifact(artifact_path)
        logger.info(f"Logged artifact: {artifact_path}")

    def log_model_xgboost(self, model, model_path: str = "xgboost_model") -> None:
        """Log XGBoost model"""
        mlflow.xgboost.log_model(model, model_path)
        logger.info(f"Logged XGBoost model: {model_path}")

    def log_model_sklearn(self, model, model_path: str = "sklearn_model") -> None:
        """Log scikit-learn model"""
        mlflow.sklearn.log_model(model, model_path)
        logger.info(f"Logged sklearn model: {model_path}")

    def log_dict(self, data: Dict, file_name: str) -> None:
        """Log dictionary as JSON artifact"""
        temp_file = Path("/tmp") / f"{file_name}.json"
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=2)
        mlflow.log_artifact(str(temp_file))
        temp_file.unlink()
        logger.info(f"Logged dict: {file_name}")

    def end_run(self) -> None:
        """End the current MLflow run"""
        mlflow.end_run()
        logger.info("MLflow run ended")

    def load_model(self, run_id: str, model_path: str):
        """Load logged model"""
        model_uri = f"runs:/{run_id}/{model_path}"
        return mlflow.sklearn.load_model(model_uri)


class ModelTrainer:
    """Unified trainer for all models with MLflow tracking"""

    def __init__(self):
        self.mlflow_tracker = MLflowTracker()
        logger.info("ModelTrainer initialized")

    def train_match_winner(
        self,
        X_train, y_train, X_val, y_val,
        feature_names: list = None,
        xgb_params: Dict = None,
    ) -> Dict:
        """Train match winner model with MLflow"""
        from app.ml.match_winner import MatchWinnerPredictor

        run_id = self.mlflow_tracker.start_run(
            "match_winner_xgboost",
            tags={"model_type": "xgboost", "task": "classification"}
        )

        try:
            # Log parameters
            params = xgb_params or {}
            params.update({
                "n_estimators": params.get("n_estimators", 100),
                "max_depth": params.get("max_depth", 7),
                "learning_rate": params.get("learning_rate", 0.1),
            })
            self.mlflow_tracker.log_params(params)

            # Train
            predictor = MatchWinnerPredictor()
            predictor.build_model(**params)
            metrics = predictor.train(X_train, y_train, X_val, y_val, feature_names)

            # Log metrics
            self.mlflow_tracker.log_metrics(metrics)

            # Log model
            self.mlflow_tracker.log_model_sklearn(predictor.model, "xgboost_model")

            # Log feature importance
            feature_imp = predictor.get_feature_importance(top_n=15)
            self.mlflow_tracker.log_dict(feature_imp, "feature_importance")

            # Save model
            predictor.save()

            logger.info(f"Match winner training complete (Run ID: {run_id})")
            return metrics

        finally:
            self.mlflow_tracker.end_run()

    def train_score_prediction(
        self,
        X_train, y_train, X_val, y_val,
        lstm_units: int = 64,
        epochs: int = 50,
    ) -> Dict:
        """Train score prediction model with MLflow"""
        from app.ml.score_prediction import ScorePredictor

        run_id = self.mlflow_tracker.start_run(
            "score_lstm",
            tags={"model_type": "lstm", "task": "regression"}
        )

        try:
            # Log parameters
            params = {
                "lstm_units": lstm_units,
                "epochs": epochs,
                "batch_size": 32,
            }
            self.mlflow_tracker.log_params(params)

            # Train
            predictor = ScorePredictor()
            predictor.build_model(input_shape=(X_train.shape[1], X_train.shape[2]), lstm_units=lstm_units)
            metrics = predictor.train(X_train, y_train, X_val, y_val, epochs=epochs)

            # Log metrics
            self.mlflow_tracker.log_metrics(metrics)

            # Log model
            self.mlflow_tracker.log_model_sklearn(predictor.model, "score_prediction_model")

            # Save model
            predictor.save()

            logger.info(f"Score prediction training complete (Run ID: {run_id})")
            return metrics

        finally:
            self.mlflow_tracker.end_run()

    def train_player_stats(
        self,
        X_train, y_train, X_val, y_val,
        stat_types: list = None,
        feature_names: list = None,
    ) -> Dict:
        """Train player stats models with MLflow"""
        from app.ml.player_stats import PlayerStatsPredictor

        stat_types = stat_types or ["runs", "strike_rate", "wickets", "economy"]
        all_metrics = {}

        for stat_type in stat_types:
            run_id = self.mlflow_tracker.start_run(
                f"player_{stat_type}",
                tags={"model_type": "random_forest", "task": "regression", "stat": stat_type}
            )

            try:
                # Log parameters
                params = {
                    "model_type": "random_forest",
                    "n_estimators": 100,
                    "max_depth": 15,
                    "stat_type": stat_type,
                }
                self.mlflow_tracker.log_params(params)

                # Train
                predictor = PlayerStatsPredictor()
                predictor.build_model(stat_type=stat_type)
                metrics = predictor.train(X_train, y_train, X_val, y_val, stat_type, feature_names)

                # Log metrics
                self.mlflow_tracker.log_metrics(metrics)

                # Log model
                self.mlflow_tracker.log_model_sklearn(
                    predictor.models[stat_type],
                    f"player_{stat_type}_model"
                )

                # Log feature importance
                feature_imp = predictor.get_feature_importance(stat_type, top_n=10)
                self.mlflow_tracker.log_dict(feature_imp, f"feature_importance_{stat_type}")

                all_metrics[stat_type] = metrics

            finally:
                self.mlflow_tracker.end_run()

        # Save all models
        predictor.save()

        logger.info(f"Player stats training complete - {len(stat_types)} models trained")
        return all_metrics

    def train_viewership(
        self,
        X_train, y_train, X_val, y_val,
        feature_names: list = None,
        use_polynomial: bool = False,
    ) -> Dict:
        """Train viewership model with MLflow"""
        from app.ml.viewership import ViewershipEstimator

        run_id = self.mlflow_tracker.start_run(
            "viewership_regression",
            tags={"model_type": "linear_regression", "task": "regression"}
        )

        try:
            # Log parameters
            params = {
                "model_type": "linear_regression",
                "use_polynomial": use_polynomial,
            }
            self.mlflow_tracker.log_params(params)

            # Train
            estimator = ViewershipEstimator()
            estimator.build_model(use_polynomial=use_polynomial)
            metrics = estimator.train(X_train, y_train, X_val, y_val, feature_names, use_polynomial)

            # Log metrics
            self.mlflow_tracker.log_metrics(metrics)

            # Log model
            self.mlflow_tracker.log_model_sklearn(estimator.model, "linear_regression_model")

            # Log coefficients
            coefficients = estimator.get_coefficients()
            self.mlflow_tracker.log_dict(coefficients, "model_coefficients")

            # Save model
            estimator.save()

            logger.info(f"Viewership training complete (Run ID: {run_id})")
            return metrics

        finally:
            self.mlflow_tracker.end_run()
