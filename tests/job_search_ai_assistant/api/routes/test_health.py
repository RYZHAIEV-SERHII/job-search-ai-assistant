"""Tests for the health check endpoint."""

from src.job_search_ai_assistant.api.schemas.health import HealthResponse

# HTTP status code constants
HTTP_200_OK = 200


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"

    # Validate response matches schema
    health_response = HealthResponse(**data)
    assert isinstance(health_response, HealthResponse)
