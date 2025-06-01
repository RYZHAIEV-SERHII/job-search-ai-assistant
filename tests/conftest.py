"""Test configuration and shared fixtures."""

import json
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from crawl4ai import LLMConfig
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from src.job_search_ai_assistant import assistant


# FastAPI Fixtures
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


# Crawl4AI Testing Fixtures
@pytest.fixture
def sample_html() -> str:
    """Sample HTML content for testing."""
    return """
    <div class="job-posting">
        <h2 class="job-title">Senior Python Developer</h2>
        <div class="company-name">Tech Corp</div>
        <div class="job-location">Kyiv, Ukraine</div>
        <div class="salary">$5000-7000</div>
        <div class="job-description">
            Looking for an experienced Python developer...
        </div>
        <ul class="requirements">
            <li>5+ years Python experience</li>
            <li>Strong knowledge of FastAPI</li>
            <li>Experience with async programming</li>
        </ul>
        <a class="job-link" href="https://example.com/job/123">Apply Now</a>
    </div>
    """


@pytest.fixture
def sample_job_response() -> dict[str, Any]:
    """Sample job response data."""
    return {
        "title": "Senior Python Developer",
        "company": "Tech Corp",
        "location": "Kyiv, Ukraine",
        "salary": "$5000-7000",
        "description": "Looking for an experienced Python developer...",
        "requirements": [
            "5+ years Python experience",
            "Strong knowledge of FastAPI",
            "Experience with async programming",
        ],
        "url": "https://example.com/job/123",
    }


@pytest.fixture
def mock_openai_response() -> dict[str, Any]:
    """Mock OpenAI API response."""
    return {
        "id": "mock-response-id",
        "object": "chat.completion",
        "created": 1683000000,
        "model": "gpt-4",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": json.dumps(
                        {
                            "title": "Senior Python Developer",
                            "company": "Tech Corp",
                            "location": "Kyiv, Ukraine",
                            "salary": "$5000-7000",
                            "description": "Looking for an experienced Python developer...",
                            "requirements": [
                                "5+ years Python experience",
                                "Strong knowledge of FastAPI",
                                "Experience with async programming",
                            ],
                        }
                    ),
                },
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }


@pytest.fixture
def mock_openai_config() -> LLMConfig:
    """Mock OpenAI configuration."""
    return LLMConfig(
        provider="openai/gpt-4",
        max_tokens=2000,
    )


@pytest.fixture
def data_dir(tmp_path) -> Path:
    """Create a temporary directory for test data."""
    test_data = tmp_path / "test_data"
    test_data.mkdir()
    return test_data


@pytest.fixture(autouse=True)
def mock_crawler_config(mocker: MockerFixture) -> None:
    """Mock crawler configuration for all tests."""
    # Mock the AsyncWebCrawler class itself to avoid initialization
    mock_crawler = mocker.MagicMock()

    async def mock_arun(*args, **kwargs):
        return {"success": True, "content": [], "html": "", "markdown": ""}

    mock_crawler.arun = mocker.AsyncMock(side_effect=mock_arun)

    # Mock the AsyncWebCrawler constructor
    mocker.patch("crawl4ai.AsyncWebCrawler", return_value=mock_crawler)


# Mock JobPosting to avoid Pydantic validation errors
class MockJobPosting:
    """Mock JobPosting class for testing."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def model_validate(cls, data):
        return cls(**data)

    @classmethod
    def model_json_schema(cls):
        return {"type": "object", "properties": {}}


mock_models = MagicMock()
mock_models.JobPosting = MockJobPosting
sys.modules["src.job_search_ai_assistant.collectors.crawl4ai.models"] = mock_models
