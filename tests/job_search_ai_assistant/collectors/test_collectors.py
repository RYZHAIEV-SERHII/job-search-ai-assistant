"""Tests for job posting collection functionality."""

import uuid

import pytest
from pydantic import ValidationError

from src.job_search_ai_assistant.collectors import JobPosting


class TestJobPosting:
    """Test suite for JobPosting schema."""

    def test_minimal_job_posting(self):
        """Test creation with minimal required fields."""
        job = JobPosting(
            title="Python Developer",
            company="Test Company",
            location="Kyiv",
            description="Development role",
            requirements=["Python"],
            url="http://example.com/job/1",
            platform="Test Platform",
        )
        assert job.title == "Python Developer"
        assert job.company == "Test Company"
        assert job.location == "Kyiv"
        assert isinstance(job.id, uuid.UUID)

    def test_complete_job_posting(self):
        """Test creation with all fields."""
        job = JobPosting(
            title="Senior Python Developer",
            company="Tech Corp",
            location="Kyiv, Ukraine",
            salary="$100,000 - $130,000",
            description="We are looking for a Senior Python Developer...",
            requirements=[
                "5+ years of Python experience",
                "Strong knowledge of FastAPI",
                "Experience with async programming",
            ],
            url="http://example.com/job/123",
            platform="LinkedIn",
            remote=True,
            experience_level="Senior",
            employment_type="Full-time",
            created_at="2025-05-26T12:00:00Z",
            raw_data={"original": "data"},
        )
        assert job.salary == "$100,000 - $130,000"
        assert len(job.requirements) == 3  # noqa: PLR2004
        assert job.remote is True
        assert job.experience_level == "Senior"
        assert isinstance(job.raw_data, dict)

    def test_invalid_url(self):
        """Test validation fails with invalid URL."""
        with pytest.raises(ValidationError):
            JobPosting(
                title="Python Developer",
                company="Test Company",
                location="Kyiv",
                description="Development role",
                requirements=["Python"],
                url="invalid://example.com",  # Invalid URL format
                platform="Test Platform",
            )

    def test_missing_required_fields(self):
        """Test validation fails when required fields are missing."""
        with pytest.raises(ValidationError):
            JobPosting(  # type: ignore [call-arg]
                title="Python Developer",
                location="Kyiv",
                description="Development role",
                requirements=["Python"],
                url="http://example.com/job/1",
                platform="Test Platform",
                # Missing company field to test validation
            )

    def test_empty_requirements(self):
        """Test validation fails with empty requirements list."""
        with pytest.raises(ValidationError):
            JobPosting(
                title="Python Developer",
                company="Test Company",
                location="Kyiv",
                description="Development role",
                requirements=[],  # Empty list is invalid
                url="http://example.com/job/1",
                platform="Test Platform",
            )

    def test_whitespace_requirements(self):
        """Test validation fails with whitespace-only requirements."""
        with pytest.raises(ValidationError):
            JobPosting(
                title="Python Developer",
                company="Test Company",
                location="Kyiv",
                description="Development role",
                requirements=["  ", ""],  # Whitespace-only is invalid
                url="http://example.com/job/1",
                platform="Test Platform",
            )

    def test_url_validation(self):
        """Test various URL validation cases."""
        test_cases = [
            "not-a-url",  # Missing scheme
            "ftp://example.com",  # Invalid scheme
            "http://",  # Missing netloc
            "https://",  # Missing netloc
            "",  # Empty string
            "http:///path",  # Missing netloc with path
        ]

        for invalid_url in test_cases:
            with pytest.raises(ValidationError):
                JobPosting(
                    title="Python Developer",
                    company="Test Company",
                    location="Kyiv",
                    description="Development role",
                    requirements=["Python"],
                    url=invalid_url,
                    platform="Test Platform",
                )

    def test_optional_fields_default_none(self):
        """Test optional fields default to None."""
        job = JobPosting(
            title="Python Developer",
            company="Test Company",
            location="Kyiv",
            description="Development role",
            requirements=["Python"],
            url="http://example.com/job/1",
            platform="Test Platform",
        )
        assert job.salary is None
        assert job.remote is None
        assert job.experience_level is None
        assert job.employment_type is None
        assert job.created_at is None
        assert job.raw_data is None

    def test_defaults_and_types(self):
        """Test default values and type validations."""
        job = JobPosting(
            title="Python Developer",
            company="Test Company",
            location="Kyiv",
            description="Development role",
            requirements=["Python"],
            url="http://example.com/job/1",
            platform="Test Platform",
        )
        assert isinstance(job.id, uuid.UUID)
        assert isinstance(job.title, str)
        assert isinstance(job.requirements, list)
        assert all(isinstance(req, str) for req in job.requirements)
