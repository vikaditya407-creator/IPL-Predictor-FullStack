"""Configuration management for IPL Predictor"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # FastAPI Configuration
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    debug: bool = True
    environment: str = "development"
    api_title: str = "IPL Predictor API"
    api_version: str = "1.0.0"

    # Database Configuration
    database_url: str = "postgresql://user:password@localhost:5432/ipl_predictor"
    sqlalchemy_echo: bool = False

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_expiry: int = 3600

    # JWT Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # MLflow Configuration
    mlflow_tracking_uri: str = "./mlflow_artifacts"
    mlflow_backend_store_uri: str = "sqlite:///mlflow.db"

    # CORS Configuration
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://localhost:8081",
    ]

    # Model Configuration
    model_path: str = "./models"
    win_probability_model: str = "match_winner_xgboost.pkl"
    score_prediction_model: str = "score_lstm.h5"
    player_stats_model: str = "player_stats_rf.pkl"
    viewership_model: str = "viewership_regression.pkl"

    # Kaggle API
    kaggle_username: str = ""
    kaggle_key: str = ""

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
