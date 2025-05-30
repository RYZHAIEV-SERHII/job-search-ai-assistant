"""Test configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.job_search_ai_assistant import assistant


@pytest.fixture
def app():
    """Create a test FastAPI application.

    Returns:
        FastAPI: Test application instance.
    """
    return assistant()


@pytest.fixture
def client(app):
    """Create a test client.

    Args:
        app: FastAPI application fixture.

    Returns:
        TestClient: FastAPI test client.
    """
    return TestClient(app)
