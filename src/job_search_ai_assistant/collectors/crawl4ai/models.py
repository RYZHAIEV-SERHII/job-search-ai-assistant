"""Job posting data models."""

from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field


class JobPosting(BaseModel):
    """Job posting schema."""

    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    salary: Optional[str] = Field(None, description="Salary information")
    description: str = Field(..., description="Job description")
    requirements: list[str] = Field(..., description="List of job requirements and qualifications")
    url: str = Field(..., description="Original job posting URL")
    platform: str = Field(..., description="Source platform name (e.g., LinkedIn, Djinni)")

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
                "platform": "LinkedIn",
            }
        }
