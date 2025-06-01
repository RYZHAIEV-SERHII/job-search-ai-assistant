"""Tests for job posting data models."""

import pytest
from pydantic import ValidationError

from src.job_search_ai_assistant.collectors.crawl4ai.models import JobPosting


class TestJobPosting:
    """Test JobPosting model."""

    def test_valid_job_posting_creation(self):
        """Test creating a valid job posting."""
        job_data = {
            "title": "Senior Python Developer",
            "company": "Tech Corp",
            "location": "Kyiv, Ukraine",
            "salary": "$100,000 - $130,000",
            "description": "We are looking for an experienced Python developer...",
            "requirements": [
                "5+ years Python experience",
                "Strong knowledge of FastAPI",
                "Experience with async programming",
            ],
            "url": "https://example.com/jobs/123",
            "apply_url": "https://example.com/jobs/123/apply",
            "platform": "LinkedIn",
        }

        job = JobPosting(**job_data)

        assert job.title == "Senior Python Developer"
        assert job.company == "Tech Corp"
        assert job.location == "Kyiv, Ukraine"
        assert job.salary == "$100,000 - $130,000"
        assert job.description == "We are looking for an experienced Python developer..."
        assert len(job.requirements) == 3
        assert str(job.url) == "https://example.com/jobs/123"
        assert str(job.apply_url) == "https://example.com/jobs/123/apply"
        assert job.platform == "LinkedIn"

    def test_minimal_job_posting(self):
        """Test creating job posting with only required fields."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Job description",
            "requirements": ["Requirement 1"],
            "url": "https://example.com/job",
        }

        job = JobPosting(**job_data)

        assert job.title == "Developer"
        assert job.salary is None
        assert job.apply_url is None
        assert job.platform is None

    def test_whitespace_stripping(self):
        """Test that whitespace is stripped from string fields."""
        job_data = {
            "title": "  Senior Developer  ",
            "company": "\tCompany Name\n",
            "location": " Remote ",
            "description": "  Description  ",
            "requirements": ["  Requirement 1  ", "\tRequirement 2\n"],
            "url": "https://example.com/job",
        }

        job = JobPosting(**job_data)

        assert job.title == "Senior Developer"
        assert job.company == "Company Name"
        assert job.location == "Remote"
        assert job.description == "Description"
        assert job.requirements == ["Requirement 1", "Requirement 2"]

    def test_empty_title_validation(self):
        """Test that empty title raises validation error."""
        job_data = {
            "title": "",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement"],
            "url": "https://example.com/job",
        }

        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**job_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

    def test_whitespace_only_fields_validation(self):
        """Test that whitespace-only fields raise validation error."""
        job_data = {
            "title": "   ",
            "company": "\t\n",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement"],
            "url": "https://example.com/job",
        }

        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**job_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)
        assert any(error["loc"] == ("company",) for error in errors)

    def test_empty_requirements_validation(self):
        """Test that empty requirements list raises validation error."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": [],
            "url": "https://example.com/job",
        }

        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**job_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("requirements",) for error in errors)

    def test_requirements_with_empty_strings(self):
        """Test that requirements with only empty strings raises validation error."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["", "   ", "\t\n"],
            "url": "https://example.com/job",
        }

        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**job_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("requirements",) for error in errors)

    def test_mixed_requirements_validation(self):
        """Test that requirements with mixed empty and valid strings are cleaned."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["", "Valid requirement", "   ", "Another requirement"],
            "url": "https://example.com/job",
        }

        job = JobPosting(**job_data)

        assert len(job.requirements) == 2
        assert job.requirements == ["Valid requirement", "Another requirement"]

    def test_valid_url_schemes(self):
        """Test that http and https URLs are accepted."""
        # Test with https
        job_data_https = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement"],
            "url": "https://example.com/job",
            "apply_url": "https://example.com/apply",
        }

        job_https = JobPosting(**job_data_https)
        assert str(job_https.url) == "https://example.com/job"
        assert str(job_https.apply_url) == "https://example.com/apply"

        # Test with http
        job_data_http = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement"],
            "url": "http://example.com/job",
            "apply_url": "http://example.com/apply",
        }

        job_http = JobPosting(**job_data_http)
        assert str(job_http.url) == "http://example.com/job"
        assert str(job_http.apply_url) == "http://example.com/apply"

    def test_invalid_url_scheme(self):
        """Test that non-http/https URLs raise validation error."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement"],
            "url": "ftp://example.com/job",
        }

        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**job_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("url",) for error in errors)

    def test_invalid_apply_url_scheme(self):
        """Test that invalid apply_url scheme raises validation error."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement"],
            "url": "https://example.com/job",
            "apply_url": "ftp://example.com/apply",
        }

        with pytest.raises(ValidationError) as exc_info:
            JobPosting(**job_data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("apply_url",) for error in errors)

    def test_none_apply_url(self):
        """Test that None apply_url is accepted."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement"],
            "url": "https://example.com/job",
            "apply_url": None,
        }

        job = JobPosting(**job_data)
        assert job.apply_url is None

    def test_missing_required_fields(self):
        """Test that missing required fields raise validation error."""
        # Test missing title
        with pytest.raises(ValidationError) as exc_info:
            JobPosting(
                company="Company",
                location="Remote",
                description="Description",
                requirements=["Requirement"],
                url="https://example.com/job",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("title",) for error in errors)

        # Test missing company
        with pytest.raises(ValidationError) as exc_info:
            JobPosting(
                title="Title",
                location="Remote",
                description="Description",
                requirements=["Requirement"],
                url="https://example.com/job",
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("company",) for error in errors)

        # Test missing url
        with pytest.raises(ValidationError) as exc_info:
            JobPosting(
                title="Title",
                company="Company",
                location="Remote",
                description="Description",
                requirements=["Requirement"],
            )
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("url",) for error in errors)

    def test_model_json_schema(self):
        """Test that model has correct JSON schema example."""
        schema = JobPosting.model_json_schema()

        # In Pydantic v2, examples are typically in the schema itself
        # The Config.json_schema_extra is merged into the schema
        assert "properties" in schema
        assert "title" in schema["properties"]
        assert "company" in schema["properties"]
        assert "requirements" in schema["properties"]

        # Check that the model has the expected structure
        assert schema["properties"]["title"]["type"] == "string"
        assert schema["properties"]["requirements"]["type"] == "array"
        assert schema["properties"]["url"]["format"] == "uri"

    def test_model_serialization(self):
        """Test model serialization to dict and JSON."""
        job_data = {
            "title": "Developer",
            "company": "Company",
            "location": "Remote",
            "description": "Description",
            "requirements": ["Requirement 1", "Requirement 2"],
            "url": "https://example.com/job",
            "platform": "TestPlatform",
        }

        job = JobPosting(**job_data)

        # Test dict serialization
        job_dict = job.model_dump()
        assert job_dict["title"] == "Developer"
        assert job_dict["company"] == "Company"
        assert job_dict["salary"] is None
        assert job_dict["apply_url"] is None
        assert len(job_dict["requirements"]) == 2

        # Test JSON serialization
        job_json = job.model_dump_json()
        assert isinstance(job_json, str)
        assert "Developer" in job_json
        assert "Company" in job_json
