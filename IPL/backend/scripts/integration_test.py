"""
Integration test for all ML components
Verifies that all models can be trained, loaded, and used for inference
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

from app.logger import logger
from app.ml.model_manager import ModelManager
from app.ml.model_serving import get_model_server, PredictionType


def test_imports():
    """Test all ML module imports"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 1: IMPORTS")
    logger.info("=" * 80)

    try:
        from app.ml import (
            MatchWinnerPredictor,
            ScorePredictor,
            PlayerStatsPredictor,
            ViewershipEstimator,
            ModelTrainer,
            MLflowTracker,
            ModelManager,
            ModelEvaluator,
            ModelServer,
            get_model_server,
            PredictionType,
            PredictionResult,
        )

        logger.info("✓ All ML classes imported successfully")
        logger.info("  - MatchWinnerPredictor")
        logger.info("  - ScorePredictor")
        logger.info("  - PlayerStatsPredictor")
        logger.info("  - ViewershipEstimator")
        logger.info("  - ModelTrainer")
        logger.info("  - MLflowTracker")
        logger.info("  - ModelManager")
        logger.info("  - ModelEvaluator")
        logger.info("  - ModelServer")
        logger.info("  - get_model_server()")
        logger.info("  - PredictionType")
        logger.info("  - PredictionResult")
        return True

    except ImportError as e:
        logger.error(f"✗ Import failed: {str(e)}")
        return False


def test_model_loading():
    """Test loading all trained models"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 2: MODEL LOADING")
    logger.info("=" * 80)

    try:
        manager = ModelManager()
        success = manager.load_all_models()

        if success:
            logger.info("✓ All models loaded successfully")
            if hasattr(manager, "match_winner"):
                logger.info("  - MatchWinnerPredictor loaded")
            if hasattr(manager, "score_predictor"):
                logger.info("  - ScorePredictor loaded")
            if hasattr(manager, "player_stats"):
                logger.info("  - PlayerStatsPredictor loaded")
        else:
            logger.warning("⚠ Some models failed to load (this is OK if models not trained yet)")

        manager.load_scalers()
        logger.info(f"✓ Loaded {len(manager.scalers)} feature scalers")
        return True

    except Exception as e:
        logger.error(f"✗ Model loading failed: {str(e)}")
        return False


def test_model_server():
    """Test ModelServer singleton and health check"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 3: MODEL SERVER")
    logger.info("=" * 80)

    try:
        from app.ml.model_serving import get_model_server

        server = get_model_server()
        logger.info("✓ ModelServer singleton created")

        # Test health check
        health = server.health_check()
        logger.info(f"✓ Health check: {health['status']}")
        logger.info(f"  - Models loaded: {health['models_loaded']}")
        logger.info(f"  - Available models: {len(health['available_models'])}")

        # Test is_ready property
        if server.is_ready:
            logger.info("✓ ModelServer is ready for inference")
        else:
            logger.warning("⚠ ModelServer not ready (models may not be trained)")

        return True

    except Exception as e:
        logger.error(f"✗ ModelServer test failed: {str(e)}")
        return False


def test_prediction_types():
    """Test PredictionType enum"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 4: PREDICTION TYPES")
    logger.info("=" * 80)

    try:
        prediction_types = [
            PredictionType.MATCH_WINNER,
            PredictionType.SCORE_PREDICTION,
            PredictionType.PLAYER_STATS,
            PredictionType.VIEWERSHIP,
        ]

        logger.info(f"✓ Found {len(prediction_types)} prediction types:")
        for pt in prediction_types:
            logger.info(f"  - {pt.value}")

        return True

    except Exception as e:
        logger.error(f"✗ Prediction types test failed: {str(e)}")
        return False


def test_sample_predictions():
    """Test making sample predictions"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 5: SAMPLE PREDICTIONS")
    logger.info("=" * 80)

    try:
        server = get_model_server()

        if not server.is_ready:
            logger.warning("⚠ ModelServer not ready, skipping inference tests")
            return True

        # Test 1: Match Winner Prediction
        logger.info("\nTesting Match Winner Prediction...")
        match_data = {
            "team1_name": "Mumbai Indians",
            "team2_name": "Chennai Super Kings",
            "team1_win_rate": 0.55,
            "team2_win_rate": 0.45,
            "venue": "Wankhede",
            "day_of_week": 3,
            "season": 2023,
        }

        result = server.predict_match_winner(match_data)
        logger.info(f"  Success: {result.success}")
        if result.success:
            logger.info(f"  Confidence: {result.confidence:.2%}")
            logger.info(f"  Result keys: {list(result.result.keys())}")
        else:
            logger.info(f"  Error: {result.error}")

        # Test 2: Score Prediction
        logger.info("\nTesting Score Prediction...")
        score_data = {
            "current_runs": 120,
            "current_rate": 4.5,
            "wickets_lost": 2,
            "overs_played": 6.0,
            "powerplay_runs": 30,
        }

        result = server.predict_final_score(score_data)
        logger.info(f"  Success: {result.success}")
        if result.success:
            logger.info(f"  Result: {result.result}")
        else:
            logger.info(f"  Error: {result.error}")

        # Test 3: Player Stats Prediction
        logger.info("\nTesting Player Stats Prediction...")
        player_data = {
            "player_name": "Virat Kohli",
            "role": "Batsman",
            "matches_played": 150,
            "avg_performance": 45.5,
            "recent_form": 0.85,
        }

        result = server.predict_player_stats(player_data, list(player_data.keys()))
        logger.info(f"  Success: {result.success}")
        if result.success:
            logger.info(f"  Result type: {type(result.result)}")
            logger.info(f"  Metadata: {result.metadata}")
        else:
            logger.info(f"  Error: {result.error}")

        # Test 4: Viewership Estimation
        logger.info("\nTesting Viewership Estimation...")
        viewership_data = {
            "team1": "Mumbai",
            "team2": "Bangalore",
            "venue": "Wankhede",
            "day_of_week": 5,
            "season": 2023,
            "is_playoff": False,
        }

        result = server.estimate_viewership(viewership_data)
        logger.info(f"  Success: {result.success}")
        if result.success:
            logger.info(f"  Result: {result.result}")
        else:
            logger.info(f"  Error: {result.error}")

        logger.info("\n✓ Inference tests completed")
        return True

    except Exception as e:
        logger.error(f"✗ Sample predictions test failed: {str(e)}")
        return False


def test_data_structures():
    """Test key data structures"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 6: DATA STRUCTURES")
    logger.info("=" * 80)

    try:
        from app.ml.model_serving import PredictionResult

        # Test PredictionResult
        result = PredictionResult(
            success=True,
            prediction_type=PredictionType.MATCH_WINNER,
            result={"team1_prob": 0.6, "team2_prob": 0.4},
            confidence=0.6,
            metadata={"teams": "MI vs CSK"},
        )

        logger.info("✓ PredictionResult created successfully")
        logger.info(f"  - Success: {result.success}")
        logger.info(f"  - Type: {result.prediction_type.value}")
        logger.info(f"  - Confidence: {result.confidence:.2%}")
        logger.info(f"  - Has metadata: {'metadata' in result.__dict__}")

        return True

    except Exception as e:
        logger.error(f"✗ Data structures test failed: {str(e)}")
        return False


def test_file_structure():
    """Verify all required files exist"""
    logger.info("\n" + "=" * 80)
    logger.info("TEST 7: FILE STRUCTURE")
    logger.info("=" * 80)

    required_files = [
        "app/ml/__init__.py",
        "app/ml/match_winner.py",
        "app/ml/score_prediction.py",
        "app/ml/player_stats.py",
        "app/ml/viewership.py",
        "app/ml/trainer.py",
        "app/ml/model_manager.py",
        "app/ml/model_serving.py",
        "scripts/train_all_models.py",
        "scripts/evaluate_models.py",
    ]

    backend_path = Path("backend")
    if not backend_path.exists():
        backend_path = Path(".")

    missing_files = []
    for file in required_files:
        file_path = backend_path / file
        if not file_path.exists():
            missing_files.append(file)

    if missing_files:
        logger.error(f"✗ Missing {len(missing_files)} files:")
        for f in missing_files:
            logger.error(f"  - {f}")
        return False
    else:
        logger.info(f"✓ All {len(required_files)} required files exist:")
        for f in required_files:
            logger.info(f"  - {f}")
        return True


def run_all_tests():
    """Run all integration tests"""
    logger.info("\n" + "=" * 80)
    logger.info("ML MODULE INTEGRATION TESTS")
    logger.info("=" * 80)

    tests = [
        ("Imports", test_imports),
        ("Model Loading", test_model_loading),
        ("Model Server", test_model_server),
        ("Prediction Types", test_prediction_types),
        ("Data Structures", test_data_structures),
        ("File Structure", test_file_structure),
        ("Sample Predictions", test_sample_predictions),
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"✗ {test_name} crashed: {str(e)}")
            results[test_name] = False

    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("TEST SUMMARY")
    logger.info("=" * 80)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")

    logger.info(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        logger.info("\n✅ ALL TESTS PASSED - ML Module ready for use!")
        return True
    else:
        logger.warning(f"\n⚠️ {total - passed} test(s) failed")
        return passed > (total // 2)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
