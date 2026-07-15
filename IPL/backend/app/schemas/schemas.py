"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# ============= Match Schemas =============

class MatchBase(BaseModel):
    season: int
    match_date: datetime
    team1: str
    team2: str
    venue: str


class MatchCreate(MatchBase):
    pass


class MatchResponse(MatchBase):
    id: int
    winner: Optional[str] = None
    player_of_match: Optional[str] = None

    class Config:
        from_attributes = True


# ============= Prediction Request Schemas =============

class PredictionRequest(BaseModel):
    team1: str = Field(..., description="First team name")
    team2: str = Field(..., description="Second team name")
    venue: Optional[str] = None
    season: Optional[int] = None

class PredictionResponse(BaseModel):
    match_id: str
    team1: dict
    team2: dict
    predicted_winner: str
    confidence: str
    factors: List[str]
    model_used: str
    timestamp: str

class MatchWinnerPredictionRequest(BaseModel):
    team1: str = Field(..., description="First team name")
    team2: str = Field(..., description="Second team name")
    venue: str = Field(..., description="Match venue")
    season: int = Field(..., description="IPL season")
    toss_winner: Optional[str] = None
    toss_decision: Optional[str] = None

    @validator("season")
    def validate_season(cls, v):
        if v < 2008 or v > 2030:
            raise ValueError("Season must be between 2008 and 2030")
        return v


class ScorePredictionRequest(BaseModel):
    current_runs: int = Field(..., ge=0, description="Current runs scored")
    current_wickets: int = Field(..., ge=0, le=10, description="Wickets lost")
    overs_completed: float = Field(..., ge=0, le=20, description="Overs bowled")
    runs_last_6_balls: int = Field(default=0, description="Runs in last 6 balls")
    target: Optional[int] = None


class PlayerStatsPredictionRequest(BaseModel):
    player_name: str
    role: str = Field(..., description="Batter, Bowler, or All-rounder")
    recent_form: float = Field(..., ge=0, le=100, description="Recent performance %")
    opponent_team: str
    venue: str


class TomorrowMatchPredictionRequest(BaseModel):
    teamA: str = Field(..., min_length=1, description="First team name or code")
    teamB: str = Field(..., min_length=1, description="Second team name or code")
    matchDate: str = Field(..., description="Match date in YYYY-MM-DD format")
    stadium: str = Field(..., min_length=1, description="Stadium name")

    @validator("teamB")
    def validate_different_teams(cls, v, values):
        team_a = values.get("teamA")
        if team_a and team_a.strip().lower() == v.strip().lower():
            raise ValueError("teamA and teamB must be different")
        return v

    @validator("matchDate")
    def validate_match_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("matchDate must use YYYY-MM-DD format") from exc
        return v


# ============= Prediction Response Schemas =============

class WinnerPredictionResponse(BaseModel):
    team1: str
    team2: str
    team1_win_probability: float
    team2_win_probability: float
    predicted_winner: str
    confidence_score: float
    model_version: str


class ScorePredictionResponse(BaseModel):
    predicted_score: int
    confidence_interval: dict  # {"lower": int, "upper": int}
    predicted_wickets: int
    model_version: str


class PlayerPerformanceResponse(BaseModel):
    player_name: str
    predicted_runs: Optional[int] = None
    predicted_wickets: Optional[int] = None
    predicted_strike_rate: Optional[float] = None
    predicted_economy: Optional[float] = None
    confidence_score: float
    model_version: str


class ViewershipEstimateResponse(BaseModel):
    predicted_live_viewers: int
    predicted_total_viewers: int
    confidence_score: float
    model_version: str


# ============= Player Schemas =============

class PlayerBase(BaseModel):
    name: str
    role: str
    country: str


class PlayerCreate(PlayerBase):
    batting_hand: Optional[str] = None
    bowling_arm: Optional[str] = None
    bowling_type: Optional[str] = None


class PlayerResponse(PlayerBase):
    id: int
    career_runs: int
    career_wickets: int
    career_matches: int

    class Config:
        from_attributes = True


class PlayerStatsResponse(BaseModel):
    player_name: str
    season: int
    matches_played: int
    runs_scored: int
    strike_rate: float
    average: float
    wickets: int
    economy_rate: float

    class Config:
        from_attributes = True


# ============= Error Schemas =============

class ErrorResponse(BaseModel):
    detail: str
    error_type: str = "BadRequest"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
