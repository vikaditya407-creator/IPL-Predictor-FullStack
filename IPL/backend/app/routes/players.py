from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas.schemas import PlayerStatsResponse
from app.logger import logger

router = APIRouter()

# Mock player data
MOCK_PLAYERS = [
    {
        "id": 1,
        "name": "Virat Kohli",
        "team": "Royal Challengers Bangalore",
        "role": "Batter",
        "country": "India",
        "age": 35,
        "stats": {
            "season": 2024,
            "matches_played": 14,
            "runs_scored": 741,
            "strike_rate": 154.2,
            "average": 61.8,
            "wickets": 0,
            "economy_rate": 0
        }
    },
    {
        "id": 2,
        "name": "Jasprit Bumrah",
        "team": "Mumbai Indians",
        "role": "Bowler",
        "country": "India",
        "age": 30,
        "stats": {
            "season": 2024,
            "matches_played": 12,
            "runs_scored": 45,
            "strike_rate": 112.5,
            "average": 22.5,
            "wickets": 18,
            "economy_rate": 7.2
        }
    },
    {
        "id": 3,
        "name": "Rishabh Pant",
        "team": "Delhi Capitals",
        "role": "Wicketkeeper-Batter",
        "country": "India",
        "age": 26,
        "stats": {
            "season": 2024,
            "matches_played": 13,
            "runs_scored": 446,
            "strike_rate": 148.3,
            "average": 40.5,
            "wickets": 0,
            "economy_rate": 0
        }
    },
    {
        "id": 4,
        "name": "Mohammed Shami",
        "team": "Kolkata Knight Riders",
        "role": "Bowler",
        "country": "India",
        "age": 33,
        "stats": {
            "season": 2024,
            "matches_played": 10,
            "runs_scored": 28,
            "strike_rate": 93.3,
            "average": 14.0,
            "wickets": 15,
            "economy_rate": 8.1
        }
    },
    {
        "id": 5,
        "name": "Hardik Pandya",
        "team": "Mumbai Indians",
        "role": "All-rounder",
        "country": "India",
        "age": 30,
        "stats": {
            "season": 2024,
            "matches_played": 14,
            "runs_scored": 323,
            "strike_rate": 142.1,
            "average": 35.9,
            "wickets": 12,
            "economy_rate": 8.8
        }
    },
    {
        "id": 6,
        "name": "Shreyas Iyer",
        "team": "Kolkata Knight Riders",
        "role": "Batter",
        "country": "India",
        "age": 29,
        "stats": {
            "season": 2024,
            "matches_played": 12,
            "runs_scored": 401,
            "strike_rate": 136.4,
            "average": 40.1,
            "wickets": 0,
            "economy_rate": 0
        }
    }
]

@router.get("/", response_model=List[Dict[str, Any]])
async def get_players():
    """Get all players"""
    logger.info("Fetching all players")
    return MOCK_PLAYERS

@router.get("/{player_id}", response_model=Dict[str, Any])
async def get_player(player_id: int):
    """Get player by ID"""
    logger.info(f"Fetching player: {player_id}")
    player = next((p for p in MOCK_PLAYERS if p["id"] == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/{player_id}/stats", response_model=PlayerStatsResponse)
async def get_player_stats(player_id: int):
    """Get player statistics"""
    logger.info(f"Fetching stats for player: {player_id}")
    player = next((p for p in MOCK_PLAYERS if p["id"] == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    stats = player["stats"]
    return PlayerStatsResponse(
        player_name=player["name"],
        season=stats["season"],
        matches_played=stats["matches_played"],
        runs_scored=stats["runs_scored"],
        strike_rate=stats["strike_rate"],
        average=stats["average"],
        wickets=stats["wickets"],
        economy_rate=stats["economy_rate"]
    )