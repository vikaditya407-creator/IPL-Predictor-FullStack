"""Machine Learning Models Module

This module contains all machine learning models for IPL Prediction:

MODELS:
-------

1. MatchWinnerPredictor (match_winner.py)
   - XGBoost for binary classification
   - Predicts which team will win
   - Features: team stats, venue, toss, temporal features
   - Output: win probability for each team

2. ScorePredictor (score_prediction.py)
   - LSTM for sequence prediction
   - Predicts final score from current match state
   - Input: ball-by-ball features (6 overs lookback default)
   - Output: predicted final score with confidence interval

3. PlayerStatsPredictor (player_stats.py)
   - Random Forest regression models
   - Separate models for: runs, strike_rate, wickets, economy
   - Features: player history, role, recent form
   - Output: predicted player statistics

4. ViewershipEstimator (viewership.py)
   - Linear Regression for viewership forecasting
   - Predicts live viewers and total audience
   - Features: teams, venue, time slot, season
   - Output: estimated viewership numbers

5. MLflowTracker (trainer.py)
   - MLflow integration for experiment tracking
   - Logs parameters, metrics, models, artifacts
   - Enables model versioning and comparison

6. ModelTrainer (trainer.py)
   - Unified trainer interface
   - Trains all models with MLflow logging
   - Uses cross-validation and early stopping
   - Saves models and metrics

USAGE:
------

1. TRAIN ALL MODELS (Recommended):

   from data.dataset_manager import DatasetManager
   from app.ml.trainer import ModelTrainer
   
   # Prepare data
   manager = DatasetManager()
   datasets = manager.prepare_all()
   
   # Train
   trainer = ModelTrainer()
   trainer.train_match_winner(X_train, y_train, X_val, y_val)
   trainer.train_score_prediction(X_train, y_train, X_val, y_val)
   trainer.train_player_stats(X_train, y_train, X_val, y_val)
   trainer.train_viewership(X_train, y_train, X_val, y_val)

2. INDIVIDUAL MODEL TRAINING:

   from app.ml.match_winner import MatchWinnerPredictor
   
   predictor = MatchWinnerPredictor()
   predictor.build_model(n_estimators=100, max_depth=7)
   metrics = predictor.train(X_train, y_train, X_val, y_val)
   predictor.save()

3. LOAD TRAINED MODELS:

   from app.ml.match_winner import MatchWinnerPredictor
   
   predictor = MatchWinnerPredictor()
   predictor.load()
   
   predictions, probabilities = predictor.predict(X_test)

4. MAKE PREDICTIONS:

   # Match winner
   match_data = {
       "team1": "KKR",
       "team2": "MI",
       "team1_win_rate": 0.55,
       ...
   }
   result = predictor.predict_match(match_data, scaler)
   
   # Score prediction
   score_result = score_predictor.predict_score(current_data)
   
   # Player stats
   player_result = player_predictor.predict_player_stats(player_data, feature_names)
   
   # Viewership
   viewership = viewership_estimator.estimate_viewership(match_data)

TRAINING PIPELINE:
------------------

1. Data Preparation
   └─ Load raw dataset
   └─ Preprocess
   └─ Feature engineering
   └─ Train/Val/Test split
   └─ Feature scaling

2. Model Training
   ├─ XGBoost
   │  ├─ Hyperparameter tuning
   │  ├─ Cross-validation
   │  └─ Feature importance
   │
   ├─ LSTM
   │  ├─ Sequence preparation
   │  ├─ Early stopping
   │  └─ Learning rate scheduling
   │
   ├─ Random Forest
   │  ├─ Multiple stat models
   │  ├─ Feature selection
   │  └─ Feature importance
   │
   └─ Linear Regression
       ├─ Polynomial features
       ├─ Coefficient analysis
       └─ Residual analysis

3. Experiment Tracking (MLflow)
   ├─ Log hyperparameters
   ├─ Log metrics
   ├─ Log models
   ├─ Log artifacts
   └─ Version control

4. Model Evaluation
   ├─ Training metrics
   ├─ Validation metrics
   ├─ Test set evaluation
   ├─ Cross-validation scores
   └─ Confusion matrices

5. Model Deployment
   ├─ Save models to disk
   ├─ Save feature scalers
   ├─ Save metadata
   └─ Archive in MLflow

EXPECTED PERFORMANCE:
---------------------

Match Winner (XGBoost):
  - Accuracy: 65-70%
  - AUC-ROC: 0.70-0.75
  - F1-Score: 0.65-0.70
  - Expected: Better than random (50%)

Score Prediction (LSTM):
  - RMSE: 15-20 runs
  - MAE: 10-15 runs
  - R²: 0.60-0.70
  - Confidence interval: ±10%

Player Performance (Random Forest):
  - R² (runs): 0.50-0.65
  - R² (strike_rate): 0.45-0.60
  - MAE (runs): 8-12
  - RMSE (strike_rate): 12-15

Viewership (Linear Regression):
  - R²: 0.70-0.80
  - MAE: 2-3 million viewers
  - RMSE: 3-4 million viewers

HYPERPARAMETERS:
----------------

XGBoost:
  - n_estimators: 100
  - max_depth: 7
  - learning_rate: 0.1
  - subsample: 0.8
  - colsample_bytree: 0.8

LSTM:
  - units: 64, 32
  - dropout: 0.2
  - learning_rate: 0.001
  - batch_size: 32
  - epochs: 50

Random Forest:
  - n_estimators: 100
  - max_depth: 15
  - random_state: 42
  - n_jobs: -1

Linear Regression:
  - Use polynomial features if non-linear
  - Polynomial degree: 2

FEATURE IMPORTANCE:
-------------------

Match Winner (Top 5):
  1. team1_win_rate
  2. team2_win_rate
  3. run_differential
  4. venue
  5. day_of_week

Score Prediction (Top 5):
  1. total_runs
  2. avg_runs_per_delivery
  3. wickets
  4. powerplay_runs
  5. phase

Player Stats (Top 5):
  1. recent_form
  2. career_runs
  3. matches_played
  4. strike_rate_history
  5. role_type

DEPLOYMENT:
-----------

1. Save models after training
   model.save()

2. Version in MLflow
   mlflow_tracker.log_model_*()

3. Load in API
   model.load()

4. Make predictions
   result = model.predict(X)

5. Monitor performance
   Compare val metrics with new data

TROUBLESHOOTING:
----------------

1. "Model not trained"
   └─ Call train() before predict()

2. "Shape mismatch"
   └─ Ensure input has same features as training

3. "Low performance"
   └─ Check data quality and feature engineering
   └─ Try hyperparameter tuning
   └─ Increase training data

4. "Memory error"
   └─ Reduce batch_size
   └─ Use data generator
   └─ Train on subset

NEXT STEPS:
-----------

1. Run training script: `python scripts/train_all_models.py`
2. Check MLflow UI: `mlflow ui`
3. Evaluate metrics: See MLflow experiment
4. Build API endpoints (Step 4)
5. Deploy models (Step 6)

"""

from .match_winner import MatchWinnerPredictor
from .score_prediction import ScorePredictor
from .player_stats import PlayerStatsPredictor
from .viewership import ViewershipEstimator
from .trainer import MLflowTracker, ModelTrainer
from .model_manager import ModelManager, ModelEvaluator
from .model_serving import ModelServer, get_model_server, PredictionType, PredictionResult

__all__ = [
    "MatchWinnerPredictor",
    "ScorePredictor",
    "PlayerStatsPredictor",
    "ViewershipEstimator",
    "MLflowTracker",
    "ModelTrainer",
    "ModelManager",
    "ModelEvaluator",
    "ModelServer",
    "get_model_server",
    "PredictionType",
    "PredictionResult",
]
