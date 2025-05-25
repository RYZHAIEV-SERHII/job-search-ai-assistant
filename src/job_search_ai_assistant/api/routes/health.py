"""Health check endpoints."""

from fastapi import APIRouter

from ..schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Perform a health check of the API.

    Returns:
        HealthResponse: Health check response containing status and version.
    """
    return HealthResponse(
        status="ok",
        version="0.1.0",
    )
