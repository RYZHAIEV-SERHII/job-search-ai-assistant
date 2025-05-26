"""Job posting collection and scraping functionality."""

from typing import Any, Optional
from urllib.parse import urlparse
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JobPosting(BaseModel):
    """Schema for standardized job listings across all platforms."""

    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the job posting")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    salary: Optional[str] = Field(default=None, description="Salary information if available")
    description: str = Field(..., description="Full job description")
    requirements: list[str] = Field(..., description="List of job requirements/qualifications")
    url: str = Field(..., description="Original job posting URL")
    platform: str = Field(..., description="Source platform name (e.g., LinkedIn, Djinni)")
    remote: Optional[bool] = Field(default=None, description="Whether the job is remote")
    experience_level: Optional[str] = Field(default=None, description="Required experience level")
    employment_type: Optional[str] = Field(
        default=None, description="Type of employment (full-time, part-time, contract)"
    )
    created_at: Optional[str] = Field(default=None, description="When the job was posted")
    raw_data: Optional[dict[str, Any]] = Field(default=None, description="Original raw data from the platform")

    @field_validator("requirements")
    @classmethod
    def validate_requirements(cls, v: list[str]) -> list[str]:
        """Validate that requirements is not empty and contains valid strings."""
        if not v:
            raise ValueError("requirements cannot be empty")  # noqa: TRY003
        if not all(isinstance(req, str) and req.strip() for req in v):
            raise ValueError("all requirements must be non-empty strings")  # noqa: TRY003
        return v

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format."""
        try:
            result = urlparse(v)
            if not all([result.scheme in ("http", "https"), result.netloc]):
                raise ValueError("invalid URL format")  # noqa: TRY003, TRY301
            else:
                return v
        except Exception as e:
            raise ValueError("invalid URL format") from e  # noqa: TRY003

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
            }
        }
    )
