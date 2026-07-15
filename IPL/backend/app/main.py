"""Main FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.logger import logger

# Import routes (will be created in Step 2)
from app.routes import predictions, players, tomorrow_match

settings = get_settings()


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="IPL Match and Player Prediction API",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "environment": settings.environment}

    # API version endpoint
    @app.get("/api/version", tags=["Info"])
    async def version():
        """Get API version"""
        return {"version": settings.api_version, "name": settings.api_title}

    # Global exception handler
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {str(exc)}", extra={"path": request.url.path})
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "type": type(exc).__name__},
        )

    # Include routers (uncomment as we build them)
    app.include_router(predictions, prefix="/api", tags=["Predictions"])
    app.include_router(players, prefix="/api/players", tags=["Players"])
    app.include_router(tomorrow_match, tags=["Tomorrow Match Prediction"])
    # app.include_router(matches.router, prefix="/api/matches", tags=["Matches"])
    # app.include_router(players.router, prefix="/api/players", tags=["Players"])
    # app.include_router(viewership.router, prefix="/api/viewership", tags=["Viewership"])

    logger.info("FastAPI application created successfully")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.debug,
    )
