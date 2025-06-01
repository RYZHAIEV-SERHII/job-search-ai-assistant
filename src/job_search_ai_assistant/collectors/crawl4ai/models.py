"""Job posting data models."""

from typing import Any, ClassVar

from pydantic import BaseModel, Field, HttpUrl, field_validator


class JobPosting(BaseModel):
    """Job posting schema."""

    title: str = Field(..., min_length=1, description="Job title")
    company: str = Field(..., min_length=1, description="Company name")
    location: str = Field(..., min_length=1, description="Job location")
    salary: str | None = Field(None, description="Salary information")
    description: str = Field(..., min_length=1, description="Job description")
    requirements: list[str] = Field(..., min_length=1, description="List of job requirements and qualifications")
    url: HttpUrl = Field(..., description="Original job posting URL")
    apply_url: HttpUrl | None = Field(None, description="Direct application URL")
    platform: str | None = Field(None, description="Source platform name (e.g., LinkedIn, Djinni)")

    @field_validator("requirements")
    @classmethod
    def validate_requirements(cls, v: list[str]) -> list[str]:
        """Validate job requirements.

        Args:
            v: List of requirement strings

        Returns:
            list[str]: Cleaned requirements list

        Raises:
            ValueError: If requirements are empty or only whitespace
        """
        requirements = [req.strip() for req in v if req and req.strip()]
        if not requirements:
            raise ValueError("At least one non-empty requirement must be provided")
        return requirements

    @field_validator("url", "apply_url")
    @classmethod
    def validate_url_scheme(cls, v: HttpUrl | None) -> HttpUrl | None:
        """Validate URL scheme.

        Args:
            v: URL to validate

        Returns:
            HttpUrl | None: Validated URL

        Raises:
            ValueError: If URL scheme is not http/https
        """
        if v is None:
            return None
        if str(v).startswith(("http://", "https://")):
            return v
        raise ValueError("URL must use http or https scheme")

    @field_validator("title", "company", "location", "description")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip whitespace from string fields.

        Args:
            v: String value to clean

        Returns:
            str: Cleaned string

        Raises:
            ValueError: If string is empty after stripping
        """
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty or whitespace")
        return v

    class Config:
        """Pydantic model configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
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
        }
