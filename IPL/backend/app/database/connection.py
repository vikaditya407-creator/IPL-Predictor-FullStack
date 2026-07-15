"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings
from app.logger import logger

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.sqlalchemy_echo,
    connect_args={
        "connect_timeout": 10,
        "check_same_thread": False if "sqlite" in settings.database_url else True,
    },
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """Dependency for getting database session in routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise


def get_session() -> Session:
    """Get a new database session"""
    return SessionLocal()
