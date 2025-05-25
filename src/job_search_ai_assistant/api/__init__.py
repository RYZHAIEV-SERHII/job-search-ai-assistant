"""API package for job-search-ai-assistant."""

from collections.abc import Awaitable
from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from .config import logger, setup_logging
from .routes import health_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    # Setup logging
    setup_logging()

    app = FastAPI(
        title="Job Search AI Assistant",
        description="AI-powered job search aggregator across multiple platforms",
        version="0.1.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Configure this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add Gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Error handling middleware
    @app.middleware("http")
    async def error_handling_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Global error handling middleware.

        Args:
            request: The incoming request
            call_next: The next middleware/route handler

        Returns:
            Response: The API response
        """
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled error: {e}", exc_info=True)
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    # Create API router
    api_router = APIRouter(prefix="/api/v1")

    # Register routers
    api_router.include_router(health_router)

    # Register API v1 router
    app.include_router(api_router)

    return app
