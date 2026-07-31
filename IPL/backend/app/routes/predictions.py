from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
from app.schemas.schemas import PredictionRequest, ScorePredictionRequest, PlayerStatsPredictionRequest
from app.logger import logger
from app.ml.model_manager import ModelManager
import numpy as np

router = APIRouter()

# Initialize ModelManager
# In a real production app, this should be initialized on startup using FastAPI lifespan events
model_manager = ModelManager()
models_loaded = model_manager.load_all_models()
if models_loaded:
    model_manager.load_scalers()

# Keep a simple history to satisfy GET endpoints
prediction_history = []

@router.get("/predictions", response_model=List[Dict[str, Any]])
async def get_predictions():
    """Get all available match predictions"""
    logger.info("Fetching all predictions")
    return prediction_history

@router.get("/predictions/{match_id}", response_model=Dict[str, Any])
async def get_prediction(match_id: str):
    """Get prediction for a specific match"""
    logger.info(f"Fetching prediction for match: {match_id}")
    prediction = next((p for p in prediction_history if p.get("match_id") == match_id), None)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@router.post("/predictions", response_model=Dict[str, Any])
async def create_prediction(request: PredictionRequest):
    """Create a new match winner prediction using ML models"""
    logger.info(f"Creating prediction for teams: {request.team1} vs {request.team2}")

    match_data = {
        "team1": request.team1,
        "team2": request.team2,
        "venue": request.venue or "Unknown",
        "season": request.season or 2024,
    }

    # Use ModelManager for real prediction
    result = model_manager.predict_match_winner(match_data)

    # Format the result to match expected API response
    prob1 = result.get("team1_win_probability", 0.5)
    prob2 = result.get("team2_win_probability", 0.5)
    winner = request.team1 if prob1 > prob2 else request.team2
    
    match_id = f"{request.team1.lower().replace(' ', '-')}-vs-{request.team2.lower().replace(' ', '-')}"

    prediction = {
        "match_id": match_id,
        "team1": {
            "name": request.team1,
            "probability": round(prob1 * 100, 1),
            "logo": "🏏"
        },
        "team2": {
            "name": request.team2,
            "probability": round(prob2 * 100, 1),
            "logo": "🏏"
        },
        "predicted_winner": winner,
        "confidence": "High" if abs(prob1 - prob2) > 0.2 else "Medium",
        "factors": result.get("factors", [
            "Historical performance",
            "Current form",
            "Player statistics",
            "Venue conditions"
        ]),
        "model_used": "ModelManager.match_winner",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "raw_model_output": result
    }
    
    prediction_history.append(prediction)
    return prediction

@router.post("/score", response_model=Dict[str, Any])
async def predict_score(request: ScorePredictionRequest):
    """Predict final match score based on current state using ML models"""
    logger.info(f"Predicting score for current state: {request.current_runs} runs, {request.current_wickets} wickets, {request.overs_completed} overs")

    # The ScorePredictor expects a numpy array
    avg_rate = request.current_runs / request.overs_completed if request.overs_completed > 0 else 0
    current_data = np.array([
        request.current_runs, 
        avg_rate, 
        request.current_wickets, 
        request.runs_last_6_balls, 
        25  # Dummy additional feature (e.g., powerplay context)
    ])

    result = model_manager.predict_score(current_data)
    
    # Extract prediction or provide a fallback based on current runs
    predicted_score = result.get("predicted_final_score", request.current_runs + int(avg_rate * (20 - request.overs_completed)))

    prediction = {
        "predicted_score": predicted_score,
        "confidence_interval": {
            "lower": max(request.current_runs, predicted_score - 20),
            "upper": predicted_score + 20
        },
        "predicted_wickets": request.current_wickets + 2,
        "current_run_rate": round(avg_rate, 2),
        "projected_run_rate": round(predicted_score / 20, 2),
        "remaining_overs": max(0, 20 - request.overs_completed),
        "factors": [
            f"Current run rate: {round(avg_rate, 2)} RPO",
            f"Wickets lost: {request.current_wickets}",
            f"Remaining overs: {max(0, 20 - request.overs_completed)}"
        ],
        "model_used": "ModelManager.score_predictor",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "raw_model_output": result
    }

    return prediction

@router.post("/player-stats", response_model=Dict[str, Any])
async def predict_player_stats(request: PlayerStatsPredictionRequest):
    """Predict player performance statistics using ML models"""
    logger.info(f"Predicting stats for player: {request.player_name}")

    player_data = {
        "player_name": request.player_name,
        "role": request.role,
        "recent_form": request.recent_form,
        "opponent_team": request.opponent_team,
        "venue": request.venue
    }
    
    # Feature names expected by the model
    feature_names = ["recent_form", "venue_avg", "opponent_avg"]
    
    result = model_manager.predict_player_performance(player_data, feature_names)

    prediction = {
        "player_name": request.player_name,
        "role": request.role,
        "predicted_runs": result.get("predicted_runs", 30),
        "predicted_wickets": result.get("predicted_wickets", 1),
        "predicted_strike_rate": result.get("predicted_strike_rate", 120.0),
        "predicted_economy": result.get("predicted_economy", 8.0),
        "predicted_average": result.get("predicted_average", 25.0),
        "confidence_score": 75.0,
        "factors": [
            f"Recent form: {request.recent_form}%",
            f"Player role: {request.role}",
            f"Venue: {request.venue}",
            f"Opponent: {request.opponent_team}"
        ],
        "model_used": "ModelManager.player_stats",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "raw_model_output": result
    }

    return prediction