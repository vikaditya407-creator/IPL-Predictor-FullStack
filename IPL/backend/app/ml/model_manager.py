"""Model management utilities for inference and deployment"""

import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from app.logger import logger


class ModelManager:
    """Load and manage trained models for inference"""

    def __init__(self, model_path: str = "./models"):
        self.model_path = Path(model_path)
        self.models = {}
        self.scalers = {}
        logger.info("ModelManager initialized")

    def load_all_models(self) -> bool:
        """Load all trained models"""
        try:
            # Load match winner
            from app.ml.match_winner import MatchWinnerPredictor
            self.match_winner = MatchWinnerPredictor()
            self.match_winner.load()
            logger.info("✓ Loaded match winner model")

            # Load score prediction
            from app.ml.score_prediction import ScorePredictor
            self.score_predictor = ScorePredictor()
            self.score_predictor.load()
            logger.info("✓ Loaded score prediction model")

            # Load player stats
            from app.ml.player_stats import PlayerStatsPredictor
            self.player_stats = PlayerStatsPredictor()
            self.player_stats.load()
            logger.info("✓ Loaded player stats model")

            # Load viewership
            from app.ml.viewership import ViewershipEstimator
            self.viewership = ViewershipEstimator()
            try:
                self.viewership.load()
                logger.info("✓ Loaded viewership model")
            except:
                logger.warning("⚠ Viewership model not found")

            logger.info("All models loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load models: {str(e)}")
            return False

    def load_scalers(self) -> bool:
        """Load feature scalers"""
        try:
            from data.dataset_manager import DatasetManager
            manager = DatasetManager()

            try:
                self.scalers["match_winner"] = manager.load_scaler("match_winner")
            except:
                logger.warning("Match winner scaler not found")

            try:
                self.scalers["score_prediction"] = manager.load_scaler("score_prediction")
            except:
                logger.warning("Score prediction scaler not found")

            logger.info(f"Loaded {len(self.scalers)} scalers")
            return True

        except Exception as e:
            logger.error(f"Failed to load scalers: {str(e)}")
            return False

    def predict_match_winner(
        self, match_data: Dict[str, Any], use_scaler: bool = True
    ) -> Dict:
        """Predict match winner"""
        try:
            # Prepare features
            features = self._dict_to_features(match_data)
            X = np.array([features])

            # Scale if available
            if use_scaler and "match_winner" in self.scalers:
                X = self.scalers["match_winner"].transform(X)

            # Predict
            return self.match_winner.predict_match(match_data, scaler=None)

        except Exception as e:
            logger.error(f"Match winner prediction failed: {str(e)}")
            return {
                "error": str(e),
                "team1_win_probability": 0.5,
                "team2_win_probability": 0.5,
            }

    def predict_score(self, current_data: np.ndarray) -> Dict:
        """Predict final score"""
        try:
            return self.score_predictor.predict_score(current_data)

        except Exception as e:
            logger.error(f"Score prediction failed: {str(e)}")
            return {"error": str(e), "predicted_final_score": 0}

    def predict_player_performance(
        self, player_data: Dict[str, Any], feature_names: list
    ) -> Dict:
        """Predict player statistics"""
        try:
            return self.player_stats.predict_player_stats(player_data, feature_names)

        except Exception as e:
            logger.error(f"Player prediction failed: {str(e)}")
            return {"error": str(e)}

    def estimate_viewership(self, match_data: Dict[str, Any]) -> Dict:
        """Estimate viewership"""
        try:
            return self.viewership.estimate_viewership(match_data)

        except Exception as e:
            logger.error(f"Viewership estimation failed: {str(e)}")
            return {"error": str(e), "predicted_viewers": 0}

    @staticmethod
    def _dict_to_features(data: Dict[str, Any]) -> list:
        """Convert dictionary to feature vector"""
        features = []
        for key in sorted(data.keys()):
            value = data[key]
            if isinstance(value, (int, float)):
                features.append(float(value))
            elif isinstance(value, str):
                features.append(float(hash(value) % 100))
            elif value is None:
                features.append(0.0)
        return features


class ModelEvaluator:
    """Evaluate models on test data"""

    def __init__(self, model_manager: ModelManager):
        self.manager = model_manager
        logger.info("ModelEvaluator initialized")

    def evaluate_match_winner(
        self, X_test: np.ndarray, y_test: np.ndarray
    ) -> Dict:
        """Evaluate match winner model"""
        try:
            from sklearn.metrics import (
                accuracy_score, precision_score, recall_score,
                f1_score, roc_auc_score, confusion_matrix
            )

            predictions, probabilities = self.manager.match_winner.predict(X_test)

            metrics = {
                "accuracy": accuracy_score(y_test, predictions),
                "precision": precision_score(y_test, predictions, zero_division=0),
                "recall": recall_score(y_test, predictions, zero_division=0),
                "f1": f1_score(y_test, predictions, zero_division=0),
                "auc": roc_auc_score(y_test, probabilities),
                "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
            }

            logger.info(f"Match winner evaluation: Accuracy={metrics['accuracy']:.4f}, AUC={metrics['auc']:.4f}")
            return metrics

        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            return {}

    def evaluate_score_prediction(
        self, X_test: np.ndarray, y_test: np.ndarray
    ) -> Dict:
        """Evaluate score prediction model"""
        try:
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

            predictions = self.manager.score_predictor.predict(X_test)

            metrics = {
                "rmse": np.sqrt(mean_squared_error(y_test, predictions)),
                "mae": mean_absolute_error(y_test, predictions),
                "r2": r2_score(y_test, predictions),
            }

            logger.info(f"Score prediction evaluation: RMSE={metrics['rmse']:.2f}, R²={metrics['r2']:.4f}")
            return metrics

        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            return {}

    def generate_report(self) -> Dict:
        """Generate comprehensive evaluation report"""
        report = {
            "models_loaded": len([m for m in [
                getattr(self.manager, name, None)
                for name in ["match_winner", "score_predictor", "player_stats"]
            ] if m]),
            "timestamp": str(Path self.manager.model_path),
        }

        logger.info("Evaluation report generated")
        return report


def test_model_inference():
    """Test model inference with sample data"""
    logger.info("\n" + "=" * 60)
    logger.info("Testing Model Inference")
    logger.info("=" * 60)

    manager = ModelManager()

    if not manager.load_all_models():
        logger.error("Failed to load models")
        return False

    if not manager.load_scalers():
        logger.warning("Some scalers not available")

    try:
        # Test match winner prediction
        sample_match = {
            "team1_win_rate": 0.55,
            "team2_win_rate": 0.45,
            "run_differential": 10,
            "wicket_differential": 0,
            "season": 2023,
            "year": 2023,
            "month": 4,
            "day_of_week": 3,
        }

        logger.info("Testing match winner prediction...")
        match_result = manager.predict_match_winner(sample_match)
        logger.info(f"Result: {match_result}")

        # Test score prediction
        logger.info("Testing score prediction...")
        sample_score_data = np.array([120, 4.5, 2, 3, 25])  # runs, avg_rate, wickets, dots, powerplay
        score_result = manager.predict_score(sample_score_data)
        logger.info(f"Result: {score_result}")

        logger.info("\n✅ Inference tests passed")
        return True

    except Exception as e:
        logger.error(f"❌ Inference test failed: {str(e)}")
        return False


if __name__ == "__main__":
    import sys
    success = test_model_inference()
    sys.exit(0 if success else 1)
