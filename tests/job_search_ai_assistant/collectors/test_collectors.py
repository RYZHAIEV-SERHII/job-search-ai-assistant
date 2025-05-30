"""Tests for job collectors module."""

from typing import Any
from uuid import UUID

import pytest
from pydantic import ValidationError

from src.job_search_ai_assistant.collectors import JobPosting


@pytest.fixture
def minimal_job_data() -> dict[str, Any]:
    """Minimal valid job posting data."""
    return {
        "title": "Python Developer",
        "company": "Tech Corp",
        "location": "Kyiv",
        "description": "We need a Python developer",
        "requirements": ["Python", "FastAPI"],
        "url": "https://example.com/job/123",
        "platform": "LinkedIn",
    }


@pytest.fixture
def full_job_data() -> dict[str, Any]:
    """Complete job posting data with all fields."""
    return {
        "title": "Senior Python Developer",
        "company": "Tech Corp",
        "location": "Kyiv, Ukraine",
        "salary": "$100,000 - $130,000",
        "description": "We are looking for a Senior Python Developer...",
        "requirements": [
            "5+ years of Python experience",
            "Strong knowledge of FastAPI",
            "Experience with async programming",
        ],
        "url": "https://example.com/job/123",
        "platform": "LinkedIn",
        "remote": True,
        "experience_level": "Senior",
        "employment_type": "Full-time",
        "created_at": "2025-05-26T12:00:00Z",
        "raw_data": {"original": "data"},
    }


class TestJobPosting:
    """Tests for JobPosting model."""

    def test_minimal_job_creation(self, minimal_job_data: dict[str, Any]) -> None:
        """Test creating job posting with minimal required fields."""
        posting = JobPosting(**minimal_job_data)
        assert posting.title == minimal_job_data["title"]
        assert posting.company == minimal_job_data["company"]
        assert posting.location == minimal_job_data["location"]
        assert posting.description == minimal_job_data["description"]
        assert posting.requirements == minimal_job_data["requirements"]
        assert posting.url == minimal_job_data["url"]
        assert posting.platform == minimal_job_data["platform"]
        assert isinstance(posting.id, UUID)

    def test_full_job_creation(self, full_job_data: dict[str, Any]) -> None:
        """Test creating job posting with all fields."""
        posting = JobPosting(**full_job_data)
        for key, value in full_job_data.items():
            assert getattr(posting, key) == value
        assert isinstance(posting.id, UUID)

    def test_requirements_validation(self, minimal_job_data: dict[str, Any]) -> None:
        """Test requirements field validation."""
        # Empty requirements should fail
        minimal_job_data["requirements"] = []
        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**minimal_job_data)
        assert "requirements cannot be empty" in str(exc_info.value)

        # Requirements with empty strings should fail
        minimal_job_data["requirements"] = ["Python", "", "FastAPI"]
        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**minimal_job_data)
        assert "all requirements must be non-empty strings" in str(exc_info.value)

        # Requirements with non-string values should fail
        minimal_job_data["requirements"] = ["Python", 123, "FastAPI"]
        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**minimal_job_data)
        # Pydantic's error message for type validation is different
        assert "Input should be a valid string" in str(exc_info.value)

    def test_url_validation(self, minimal_job_data: dict[str, Any]) -> None:
        """Test URL format validation."""
        # Valid URLs
        valid_urls = [
            "https://example.com",
            "http://sub.example.com/path?param=1",
            "https://example.com/path#section",
        ]

        for url in valid_urls:
            minimal_job_data["url"] = url
            posting = JobPosting(**minimal_job_data)
            assert posting.url == url

        # Invalid URLs based on the actual validation logic
        invalid_urls = [
            "not-a-url",  # No scheme
            "://example.com",  # Missing scheme
            "https://",  # Missing domain
        ]

        for url in invalid_urls:
            minimal_job_data["url"] = url
            with pytest.raises(ValidationError) as exc_info:
                JobPosting(**minimal_job_data)
            assert "invalid URL format" in str(exc_info.value)

        # FTP URLs are actually valid according to urlparse, but our validator only allows http/https
        minimal_job_data["url"] = "ftp://example.com"
        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**minimal_job_data)
        assert "invalid URL format" in str(exc_info.value)

    def test_optional_fields_default_to_none(self, minimal_job_data: dict[str, Any]) -> None:
        """Test that optional fields default to None."""
        posting = JobPosting(**minimal_job_data)
        assert posting.salary is None
        assert posting.remote is None
        assert posting.experience_level is None
        assert posting.employment_type is None
        assert posting.created_at is None
        assert posting.raw_data is None

    def test_id_auto_generation(self, minimal_job_data: dict[str, Any]) -> None:
        """Test that ID is automatically generated if not provided."""
        posting1 = JobPosting(**minimal_job_data)
        posting2 = JobPosting(**minimal_job_data)
        assert isinstance(posting1.id, UUID)
        assert isinstance(posting2.id, UUID)
        assert posting1.id != posting2.id

    def test_model_config_example(self) -> None:
        """Test that the model config example is valid."""
        example_data = JobPosting.model_config["json_schema_extra"]["example"]
        posting = JobPosting(**example_data)
        assert posting.title == "Senior Python Developer"
        assert posting.remote is True
