"""Tests for the core FastAPI application."""

from fastapi import FastAPI
from starlette.testclient import TestClient

# HTTP status code constants
HTTP_200_OK = 200
HTTP_500_INTERNAL_SERVER_ERROR = 500


def test_app_creation(app: FastAPI):
    """Test that the application is created with correct configuration."""
    assert app.title == "Job Search AI Assistant"
    assert app.version == "0.1.0"


def test_cors_middleware_enabled(app: FastAPI):
    """Test that CORS middleware is configured."""
    # Test CORS by making an OPTIONS request
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://test.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == HTTP_200_OK
        assert response.headers["access-control-allow-origin"] == "*"
        # Credentials header is not sent when allow_credentials=False
        assert "access-control-allow-credentials" not in response.headers


def test_gzip_compression(app: FastAPI):
    """Test that Gzip compression is working."""
    # Create a response large enough to trigger compression
    large_data = "a" * 1500  # Above our 1000 byte threshold

    @app.get("/test-gzip")
    def test_route():
        return {"data": large_data}

    with TestClient(app) as client:
        response = client.get("/test-gzip", headers={"Accept-Encoding": "gzip"})
        assert response.status_code == HTTP_200_OK
        assert response.headers["Content-Encoding"] == "gzip"


def test_api_router_prefix(app: FastAPI):
    """Test that the API router is mounted with correct prefix."""
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == HTTP_200_OK


def test_error_handling(client):
    """Test the global error handling middleware."""

    @client.app.get("/test-error")
    async def error_route():
        raise ValueError

    response = client.get("/test-error")
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Internal server error"}
