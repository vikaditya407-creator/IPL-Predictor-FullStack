"""Model serving utilities for API integration"""

import numpy as np
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from app.logger import logger
from app.ml.model_manager import ModelManager


class PredictionType(str, Enum):
    """Types of predictions the system supports"""
    MATCH_WINNER = "match_winner"
    SCORE_PREDICTION = "score_prediction"
    PLAYER_STATS = "player_stats"
    VIEWERSHIP = "viewership"


@dataclass
class PredictionResult:
    """Standard prediction result format"""
    success: bool
    prediction_type: PredictionType
    result: Dict[str, Any]
    error: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Optional[Dict] = None


class ModelServer:
    """Production-grade model serving interface"""

    _instance: Optional["ModelServer"] = None
    _models_loaded = False

    def __new__(cls):
        """Singleton pattern for model server"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize model server (runs once)"""
        if not self._models_loaded:
            self.manager = ModelManager()
            self._models_loaded = self.manager.load_all_models()
            if self._models_loaded:
                self.manager.load_scalers()
            logger.info(f"ModelServer initialized. Models loaded: {self._models_loaded}")

    @property
    def is_ready(self) -> bool:
        """Check if models are ready for inference"""
        return self._models_loaded and hasattr(self, "manager")

    def predict_match_winner(self, match_data: Dict[str, Any]) -> PredictionResult:
        """
        Predict match winner

        Args:
            match_data: Dictionary with match features
                - team1_name: str
                - team2_name: str
                - team1_win_rate: float (0-1)
                - team2_win_rate: float (0-1)
                - venue: str
                - toss_winner: str
                - season: int
                - month: int

        Returns:
            PredictionResult with winner probabilities
        """
        if not self.is_ready:
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.MATCH_WINNER,
                result={},
                error="Models not loaded",
            )

        try:
            result = self.manager.predict_match_winner(match_data)

            if "error" not in result:
                team1_win_prob = result.get("team1_win_probability", 0.5)
                confidence = max(team1_win_prob, 1 - team1_win_prob)

                return PredictionResult(
                    success=True,
                    prediction_type=PredictionType.MATCH_WINNER,
                    result=result,
                    confidence=confidence,
                    metadata={
                        "team1": match_data.get("team1_name", "Team 1"),
                        "team2": match_data.get("team2_name", "Team 2"),
                    },
                )
            else:
                return PredictionResult(
                    success=False,
                    prediction_type=PredictionType.MATCH_WINNER,
                    result=result,
                    error=result.get("error"),
                )

        except Exception as e:
            logger.error(f"Match winner prediction error: {str(e)}")
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.MATCH_WINNER,
                result={},
                error=str(e),
            )

    def predict_final_score(self, match_data: Dict[str, Any]) -> PredictionResult:
        """
        Predict final score for batting team

        Args:
            match_data: Dictionary with match features
                - current_runs: int
                - current_rate: float
                - wickets_lost: int
                - overs_played: float
                - powerplay_runs: int

        Returns:
            PredictionResult with predicted final score
        """
        if not self.is_ready:
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.SCORE_PREDICTION,
                result={},
                error="Models not loaded",
            )

        try:
            features = np.array([
                match_data.get("current_runs", 0),
                match_data.get("current_rate", 5.0),
                match_data.get("wickets_lost", 0),
                match_data.get("overs_played", 6.0),
                match_data.get("powerplay_runs", 30),
            ])

            result = self.manager.predict_score(features)

            if "error" not in result:
                return PredictionResult(
                    success=True,
                    prediction_type=PredictionType.SCORE_PREDICTION,
                    result=result,
                    metadata={
                        "current_runs": match_data.get("current_runs", 0),
                        "overs_played": match_data.get("overs_played", 0),
                    },
                )
            else:
                return PredictionResult(
                    success=False,
                    prediction_type=PredictionType.SCORE_PREDICTION,
                    result=result,
                    error=result.get("error"),
                )

        except Exception as e:
            logger.error(f"Score prediction error: {str(e)}")
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.SCORE_PREDICTION,
                result={},
                error=str(e),
            )

    def predict_player_stats(
        self, player_data: Dict[str, Any], stat_types: Optional[List[str]] = None
    ) -> PredictionResult:
        """
        Predict player performance statistics

        Args:
            player_data: Dictionary with player features
                - player_name: str
                - role: str (Batsman/Bowler/All-rounder)
                - matches_played: int
                - avg_performance: float
                - recent_form: float (0-1)
            stat_types: List of statistics to predict (if None, predict all)

        Returns:
            PredictionResult with predicted player stats
        """
        if not self.is_ready:
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.PLAYER_STATS,
                result={},
                error="Models not loaded",
            )

        try:
            feature_keys = list(player_data.keys())
            result = self.manager.predict_player_performance(player_data, feature_keys)

            if "error" not in result:
                return PredictionResult(
                    success=True,
                    prediction_type=PredictionType.PLAYER_STATS,
                    result=result,
                    metadata={"player": player_data.get("player_name", "Unknown")},
                )
            else:
                return PredictionResult(
                    success=False,
                    prediction_type=PredictionType.PLAYER_STATS,
                    result=result,
                    error=result.get("error"),
                )

        except Exception as e:
            logger.error(f"Player stats prediction error: {str(e)}")
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.PLAYER_STATS,
                result={},
                error=str(e),
            )

    def estimate_viewership(self, match_data: Dict[str, Any]) -> PredictionResult:
        """
        Estimate match viewership

        Args:
            match_data: Dictionary with match features
                - team1: str
                - team2: str
                - venue: str
                - day_of_week: int (0-6)
                - season: int
                - is_playoff: bool

        Returns:
            PredictionResult with viewership estimates
        """
        if not self.is_ready:
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.VIEWERSHIP,
                result={},
                error="Models not loaded",
            )

        try:
            result = self.manager.estimate_viewership(match_data)

            if "error" not in result:
                return PredictionResult(
                    success=True,
                    prediction_type=PredictionType.VIEWERSHIP,
                    result=result,
                    metadata={
                        "venue": match_data.get("venue", "Unknown"),
                        "teams": f"{match_data.get('team1', 'Team1')} vs {match_data.get('team2', 'Team2')}",
                    },
                )
            else:
                return PredictionResult(
                    success=False,
                    prediction_type=PredictionType.VIEWERSHIP,
                    result=result,
                    error=result.get("error"),
                )

        except Exception as e:
            logger.error(f"Viewership estimation error: {str(e)}")
            return PredictionResult(
                success=False,
                prediction_type=PredictionType.VIEWERSHIP,
                result={},
                error=str(e),
            )

    def health_check(self) -> Dict[str, Any]:
        """Check model server health"""
        return {
            "status": "healthy" if self.is_ready else "degraded",
            "models_loaded": self._models_loaded,
            "available_models": [
                PredictionType.MATCH_WINNER.value,
                PredictionType.SCORE_PREDICTION.value,
                PredictionType.PLAYER_STATS.value,
                PredictionType.VIEWERSHIP.value,
            ] if self.is_ready else [],
        }


# Singleton instance
model_server = ModelServer()


def get_model_server() -> ModelServer:
    """Get singleton model server instance"""
    return model_server
