"""Main entry point for the job-search-ai-assistant project."""

from fastapi import FastAPI

from .api import create_app


def assistant() -> FastAPI:
    """Create and return the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    return create_app()


if __name__ == "__main__":  # pragma: no cover
    assistant()
