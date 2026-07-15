"""Comprehensive evaluation of all trained models"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Tuple
import json

from app.logger import logger
from app.ml.model_manager import ModelManager, ModelEvaluator
from data.dataset_manager import DatasetManager


class ComprehensiveEvaluator:
    """Evaluate all models with detailed metrics and visualizations"""

    def __init__(self):
        self.manager = ModelManager()
        self.evaluator = ModelEvaluator(self.manager)
        self.dataset_manager = DatasetManager()
        self.results = {}

    def run_full_evaluation(self) -> Dict:
        """Run complete evaluation suite"""
        logger.info("\n" + "=" * 80)
        logger.info("COMPREHENSIVE MODEL EVALUATION")
        logger.info("=" * 80)

        # Load models
        if not self.manager.load_all_models():
            logger.error("Failed to load models")
            return {}

        # Load scalers
        self.manager.load_scalers()

        # Load datasets
        logger.info("\nLoading datasets...")
        try:
            datasets = self.dataset_manager.load_prepared_data()
        except Exception as e:
            logger.error(f"Failed to load datasets: {str(e)}")
            return {}

        # Evaluate each model
        self.results = {
            "match_winner": self._evaluate_match_winner(datasets),
            "score_prediction": self._evaluate_score_prediction(datasets),
            "player_stats": self._evaluate_player_stats(datasets),
        }

        # Generate summary
        self._print_summary()
        self._save_results()

        return self.results

    def _evaluate_match_winner(self, datasets: Dict) -> Dict:
        """Evaluate match winner prediction model"""
        logger.info("\n" + "-" * 80)
        logger.info("MATCH WINNER PREDICTION EVALUATION")
        logger.info("-" * 80)

        try:
            X_test = datasets["match_winner"]["X_test"]
            y_test = datasets["match_winner"]["y_test"]

            logger.info(f"Test set size: {len(X_test)}")
            logger.info(f"Class distribution: {np.bincount(y_test)}")

            metrics = self.evaluator.evaluate_match_winner(X_test, y_test)

            # Feature importance
            if hasattr(self.manager.match_winner, "model"):
                feature_importance = self.manager.match_winner.feature_importance()
                if feature_importance:
                    logger.info("\nTop 10 Important Features:")
                    for i, (feat, imp) in enumerate(feature_importance[:10], 1):
                        logger.info(f"  {i:2d}. {feat:30s} {imp:.4f}")

            # Detailed metrics table
            logger.info("\nDetailed Metrics:")
            logger.info(f"  Accuracy:  {metrics.get('accuracy', 0):.4f}")
            logger.info(f"  Precision: {metrics.get('precision', 0):.4f}")
            logger.info(f"  Recall:    {metrics.get('recall', 0):.4f}")
            logger.info(f"  F1-Score:  {metrics.get('f1', 0):.4f}")
            logger.info(f"  AUC-ROC:   {metrics.get('auc', 0):.4f}")

            if "confusion_matrix" in metrics:
                cm = metrics["confusion_matrix"]
                logger.info(f"\nConfusion Matrix:\n  TN={cm[0][0]}  FP={cm[0][1]}\n  FN={cm[1][0]}  TP={cm[1][1]}")

            return metrics

        except Exception as e:
            logger.error(f"Match winner evaluation failed: {str(e)}")
            return {}

    def _evaluate_score_prediction(self, datasets: Dict) -> Dict:
        """Evaluate score prediction model"""
        logger.info("\n" + "-" * 80)
        logger.info("SCORE PREDICTION EVALUATION")
        logger.info("-" * 80)

        try:
            X_test = datasets["score_prediction"]["X_test"]
            y_test = datasets["score_prediction"]["y_test"]

            logger.info(f"Test set size: {len(X_test)}")
            logger.info(f"Score range: {y_test.min()}..{y_test.max()} runs")
            logger.info(f"Mean score: {y_test.mean():.1f} ± {y_test.std():.1f} runs")

            metrics = self.evaluator.evaluate_score_prediction(X_test, y_test)

            logger.info("\nDetailed Metrics:")
            logger.info(f"  RMSE: {metrics.get('rmse', 0):.2f} runs")
            logger.info(f"  MAE:  {metrics.get('mae', 0):.2f} runs")
            logger.info(f"  R²:   {metrics.get('r2', 0):.4f}")

            # Error analysis
            if hasattr(self.manager.score_predictor, "predict"):
                predictions = self.manager.score_predictor.predict(X_test)
                errors = np.abs(predictions - y_test)
                logger.info(f"\nError Analysis:")
                logger.info(f"  Mean Error:     {errors.mean():.2f} runs")
                logger.info(f"  Median Error:   {np.median(errors):.2f} runs")
                logger.info(f"  90th Percentile: {np.percentile(errors, 90):.2f} runs")

            return metrics

        except Exception as e:
            logger.error(f"Score prediction evaluation failed: {str(e)}")
            return {}

    def _evaluate_player_stats(self, datasets: Dict) -> Dict:
        """Evaluate player statistics prediction model"""
        logger.info("\n" + "-" * 80)
        logger.info("PLAYER STATISTICS PREDICTION EVALUATION")
        logger.info("-" * 80)

        try:
            X_test = datasets.get("player_stats", {}).get("X_test")
            if X_test is None:
                logger.warning("Player stats test set not available")
                return {}

            logger.info(f"Test set size: {len(X_test)}")

            # Test with sample data
            sample_data = {
                "player": "Player 1",
                "role": "Batsman",
                "matches_played": 50,
                "avg_runs": 35.5,
                "strike_rate": 130.0,
                "opponent_type": "Top5",
            }

            logger.info(f"\nSample prediction:")
            result = self.manager.predict_player_performance(sample_data, list(sample_data.keys()))
            logger.info(f"  {result}")

            return {"status": "evaluated", "sample_result": result}

        except Exception as e:
            logger.error(f"Player stats evaluation failed: {str(e)}")
            return {}

    def _print_summary(self) -> None:
        """Print evaluation summary"""
        logger.info("\n" + "=" * 80)
        logger.info("EVALUATION SUMMARY")
        logger.info("=" * 80)

        for model_name, metrics in self.results.items():
            logger.info(f"\n{model_name.upper().replace('_', ' ')}:")
            if metrics:
                if "accuracy" in metrics:
                    logger.info(f"  ✓ Accuracy: {metrics['accuracy']:.4f}")
                if "rmse" in metrics:
                    logger.info(f"  ✓ RMSE: {metrics['rmse']:.2f}")
                if "auc" in metrics:
                    logger.info(f"  ✓ AUC: {metrics['auc']:.4f}")
            else:
                logger.warning("  ✗ No metrics available")

    def _save_results(self) -> None:
        """Save evaluation results to JSON"""
        try:
            results_path = Path("./models/evaluation_results.json")
            results_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert numpy types to Python types for JSON serialization
            results_to_save = {}
            for model_name, metrics in self.results.items():
                results_to_save[model_name] = {}
                for key, value in metrics.items():
                    if isinstance(value, np.ndarray):
                        results_to_save[model_name][key] = value.tolist()
                    elif isinstance(value, (np.integer, np.floating)):
                        results_to_save[model_name][key] = float(value)
                    else:
                        results_to_save[model_name][key] = value

            with open(results_path, "w") as f:
                json.dump(results_to_save, f, indent=2)

            logger.info(f"\n✓ Results saved to {results_path}")

        except Exception as e:
            logger.error(f"Failed to save results: {str(e)}")


def run_inference_tests() -> bool:
    """Run comprehensive inference tests"""
    logger.info("\n" + "=" * 80)
    logger.info("INFERENCE TESTS")
    logger.info("=" * 80)

    manager = ModelManager()

    if not manager.load_all_models():
        logger.error("Failed to load models")
        return False

    logger.info("\n✓ All models loaded successfully")

    # Test match winner inference
    try:
        logger.info("\nTesting Match Winner Inference...")
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
        result = manager.predict_match_winner(sample_match)
        logger.info(f"  Result: {result}")
    except Exception as e:
        logger.error(f"  ✗ Failed: {str(e)}")

    # Test score prediction inference
    try:
        logger.info("\nTesting Score Prediction Inference...")
        sample_data = np.array([[120.0, 4.5, 2.0, 3.0, 25.0]])
        result = manager.predict_score(sample_data)
        logger.info(f"  Result: {result}")
    except Exception as e:
        logger.error(f"  ✗ Failed: {str(e)}")

    # Test player stats inference
    try:
        logger.info("\nTesting Player Stats Inference...")
        sample_player = {
            "player": "Player 1",
            "matches_played": 50,
            "avg_runs": 35.5,
        }
        result = manager.predict_player_performance(sample_player, list(sample_player.keys()))
        logger.info(f"  Result: {result}")
    except Exception as e:
        logger.error(f"  ✗ Failed: {str(e)}")

    logger.info("\n✓ Inference tests completed")
    return True


if __name__ == "__main__":
    import sys

    # Run evaluation
    evaluator = ComprehensiveEvaluator()
    evaluator.run_full_evaluation()

    # Run inference tests
    success = run_inference_tests()

    logger.info("\n" + "=" * 80)
    logger.info("EVALUATION COMPLETE")
    logger.info("=" * 80)

    sys.exit(0 if success else 1)
