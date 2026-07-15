from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas.schemas import PredictionRequest, PredictionResponse, ScorePredictionRequest, PlayerStatsPredictionRequest
from app.logger import logger

router = APIRouter()

# Mock data for predictions
MOCK_PREDICTIONS = [
    {
        "match_id": "mi-vs-csk-2024-45",
        "team1": {
            "name": "Mumbai Indians",
            "probability": 0.62,
            "logo": "🏆"
        },
        "team2": {
            "name": "Chennai Super Kings",
            "probability": 0.38,
            "logo": "🐯"
        },
        "predicted_winner": "Mumbai Indians",
        "confidence": "High",
        "factors": [
            "Home advantage at DY Patil Stadium",
            "Strong recent form (won last 3 matches)",
            "Superior bowling attack with Jasprit Bumrah",
            "Better head-to-head record this season"
        ],
        "model_used": "xgboost_classifier_v2.0",
        "timestamp": "2024-04-19T10:30:00Z"
    },
    {
        "match_id": "rcb-vs-kkr-2024-46",
        "team1": {
            "name": "Royal Challengers Bangalore",
            "probability": 0.55,
            "logo": "🦁"
        },
        "team2": {
            "name": "Kolkata Knight Riders",
            "probability": 0.45,
            "logo": "🐱"
        },
        "predicted_winner": "Royal Challengers Bangalore",
        "confidence": "Medium",
        "factors": [
            "Strong batting lineup with Virat Kohli",
            "Captain Faf du Plessis' experience",
            "Venue familiarity at M. Chinnaswamy Stadium",
            "Recent improvement in bowling"
        ],
        "model_used": "xgboost_classifier_v2.0",
        "timestamp": "2024-04-19T10:30:00Z"
    },
    {
        "match_id": "dc-vs-srh-2024-47",
        "team1": {
            "name": "Delhi Capitals",
            "probability": 0.48,
            "logo": "🦅"
        },
        "team2": {
            "name": "Sunrisers Hyderabad",
            "probability": 0.52,
            "logo": "🌞"
        },
        "predicted_winner": "Sunrisers Hyderabad",
        "confidence": "Low",
        "factors": [
            "Pitch conditions favoring spinners",
            "Weather forecast (possible rain interruption)",
            "Player availability and fitness",
            "Recent form comparison"
        ],
        "model_used": "xgboost_classifier_v2.0",
        "timestamp": "2024-04-19T10:30:00Z"
    }
]

@router.get("/predictions", response_model=List[Dict[str, Any]])
async def get_predictions():
    """Get all available match predictions"""
    logger.info("Fetching all predictions")
    return MOCK_PREDICTIONS

@router.get("/predictions/{match_id}", response_model=Dict[str, Any])
async def get_prediction(match_id: str):
    """Get prediction for a specific match"""
    logger.info(f"Fetching prediction for match: {match_id}")
    prediction = next((p for p in MOCK_PREDICTIONS if p["match_id"] == match_id), None)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

@router.post("/predictions", response_model=Dict[str, Any])
async def create_prediction(request: PredictionRequest):
    """Create a new prediction (mock implementation)"""
    logger.info(f"Creating prediction for teams: {request.team1} vs {request.team2}")

    # Mock prediction logic
    import random
    prob1 = random.uniform(0.4, 0.7)
    prob2 = 1 - prob1

    winner = request.team1 if prob1 > prob2 else request.team2

    prediction = {
        "match_id": f"{request.team1.lower().replace(' ', '-')}-vs-{request.team2.lower().replace(' ', '-')}",
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
        "confidence": "Medium" if abs(prob1 - prob2) < 0.2 else "High",
        "factors": [
            "Historical performance",
            "Current form",
            "Player statistics",
            "Venue conditions"
        ],
        "model_used": "xgboost_classifier_v2.0",
        "timestamp": "2024-04-19T10:30:00Z"
    }

    return prediction

@router.post("/score", response_model=Dict[str, Any])
async def predict_score(request: ScorePredictionRequest):
    """Predict final match score based on current state"""
    logger.info(f"Predicting score for current state: {request.current_runs} runs, {request.current_wickets} wickets, {request.overs_completed} overs")

    # Mock score prediction logic
    import random
    
    # Base prediction on current runs and wickets
    base_score = request.current_runs
    remaining_overs = 20 - request.overs_completed
    remaining_balls = remaining_overs * 6
    
    # Estimate runs per ball based on current rate
    if request.overs_completed > 0:
        current_run_rate = request.current_runs / request.overs_completed
    else:
        current_run_rate = 8.0  # Default IPL run rate
    
    # Adjust for wickets
    wicket_penalty = request.current_wickets * 15  # Each wicket costs ~15 runs
    
    # Predict remaining runs
    predicted_remaining = int((current_run_rate * remaining_overs * 0.8) - wicket_penalty)
    predicted_remaining = max(0, predicted_remaining)
    
    final_score = request.current_runs + predicted_remaining
    
    # Add some randomness
    final_score += random.randint(-20, 20)
    final_score = max(request.current_runs, final_score)
    
    # Predict wickets
    predicted_wickets = request.current_wickets + random.randint(0, 3)
    predicted_wickets = min(10, predicted_wickets)
    
    # Confidence interval
    confidence_lower = max(request.current_runs, final_score - 30)
    confidence_upper = final_score + 25
    
    prediction = {
        "predicted_score": final_score,
        "confidence_interval": {
            "lower": confidence_lower,
            "upper": confidence_upper
        },
        "predicted_wickets": predicted_wickets,
        "current_run_rate": round(current_run_rate, 2),
        "projected_run_rate": round(final_score / 20, 2),
        "remaining_overs": remaining_overs,
        "factors": [
            f"Current run rate: {round(current_run_rate, 2)} RPO",
            f"Wickets lost: {request.current_wickets}",
            f"Remaining overs: {remaining_overs}",
            "Historical IPL averages applied"
        ],
        "model_used": "score_regression_v1.0",
        "timestamp": "2024-04-19T10:30:00Z"
    }

    return prediction

@router.post("/player-stats", response_model=Dict[str, Any])
async def predict_player_stats(request: PlayerStatsPredictionRequest):
    """Predict player performance statistics"""
    logger.info(f"Predicting stats for player: {request.player_name}")

    # Mock player stats prediction logic
    import random
    
    # Base stats vary by role
    if request.role.lower() == "batter":
        base_runs = random.randint(25, 45)
        base_strike_rate = random.uniform(120, 150)
        base_average = random.uniform(25, 40)
        wickets = 0
        economy = 0
    elif request.role.lower() == "bowler":
        base_runs = random.randint(5, 15)
        base_strike_rate = random.uniform(80, 120)
        base_average = random.uniform(15, 25)
        wickets = random.randint(1, 3)
        economy = random.uniform(7.5, 9.5)
    else:  # All-rounder
        base_runs = random.randint(20, 35)
        base_strike_rate = random.uniform(110, 140)
        base_average = random.uniform(20, 30)
        wickets = random.randint(0, 2)
        economy = random.uniform(8.0, 10.0) if wickets > 0 else 0

    # Adjust based on recent form (0-100 scale)
    form_multiplier = request.recent_form / 100.0
    predicted_runs = int(base_runs * (0.8 + form_multiplier * 0.4))
    predicted_strike_rate = base_strike_rate * (0.9 + form_multiplier * 0.2)
    predicted_average = base_average * (0.9 + form_multiplier * 0.2)
    
    if wickets > 0:
        predicted_wickets = max(1, int(wickets * (0.8 + form_multiplier * 0.4)))
        predicted_economy = economy * (0.9 + (1 - form_multiplier) * 0.2)  # Lower economy is better
    else:
        predicted_wickets = 0
        predicted_economy = 0

    # Add some venue/opponent adjustments
    venue_bonus = random.uniform(0.9, 1.1)
    predicted_runs = int(predicted_runs * venue_bonus)
    predicted_strike_rate *= venue_bonus

    prediction = {
        "player_name": request.player_name,
        "role": request.role,
        "predicted_runs": predicted_runs,
        "predicted_wickets": predicted_wickets,
        "predicted_strike_rate": round(predicted_strike_rate, 2),
        "predicted_economy": round(predicted_economy, 2) if predicted_economy > 0 else 0,
        "predicted_average": round(predicted_average, 2),
        "confidence_score": round(70 + form_multiplier * 25 + random.uniform(-10, 10), 1),
        "factors": [
            f"Recent form: {request.recent_form}%",
            f"Player role: {request.role}",
            f"Venue: {request.venue}",
            f"Opponent: {request.opponent_team}",
            "Historical performance analysis"
        ],
        "model_used": "player_stats_rf_v1.0",
        "timestamp": "2024-04-19T10:30:00Z"
    }

    return prediction