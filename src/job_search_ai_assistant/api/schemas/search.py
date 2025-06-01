"""Job search request and response schemas."""

from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field, HttpUrl


class SalaryRange(BaseModel):
    """Salary range model."""

    min_amount: Optional[float] = Field(None, description="Minimum salary amount")
    max_amount: Optional[float] = Field(None, description="Maximum salary amount")
    currency: Optional[str] = Field(None, description="Salary currency (e.g., USD, EUR)")


class SearchFilters(BaseModel):
    """Unified search filters and criteria for job queries."""

    # Core search fields
    keywords: Optional[list[str]] = Field(None, description="List of search keywords (e.g., ['python', 'fastapi'])")
    location: Optional[str] = Field(None, description="Job location filter")
    salary_range: Optional[SalaryRange] = Field(None, description="Target salary range")
    remote: Optional[bool] = Field(None, description="Remote work filter")
    experience_level: Optional[str] = Field(
        None, description="Experience level filter", examples=["entry", "mid", "senior", "lead"]
    )
    job_type: Optional[str] = Field(
        None, description="Job type filter", examples=["full-time", "part-time", "contract", "internship"]
    )
    salary_min: Optional[float] = Field(None, description="Minimum salary filter")
    salary_max: Optional[float] = Field(None, description="Maximum salary filter")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "keywords": ["python", "fastapi", "postgresql"],
                "location": "Kyiv, Ukraine",
                "salary_range": {"min_amount": 100000, "max_amount": 150000, "currency": "USD"},
                "remote": True,
                "experience_level": "senior",
                "job_type": "full-time",
                "salary_min": 3000,
                "salary_max": 5000,
            }
        }


class JobListing(BaseModel):
    """Individual job listing in search results."""

    id: str = Field(..., description="Unique job identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    url: HttpUrl = Field(..., description="Job posting URL")
    source: str = Field(..., description="Source platform (e.g., linkedin, dou, djinni, workua)")
    location: Optional[str] = Field(None, description="Job location")
    description: Optional[str] = Field(None, description="Job description")
    posted_date: Optional[str] = Field(None, description="Date when job was posted (ISO format)")
    salary: Optional[str] = Field(None, description="Salary information as text")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "id": "job-123",
                "title": "Senior Python Developer",
                "company": "Tech Corp",
                "url": "https://example.com/jobs/123",
                "source": "linkedin",
                "location": "Kyiv, Ukraine",
                "description": "We are looking for an experienced Python developer...",
                "posted_date": "2024-01-15",
                "salary": "$100,000 - $150,000",
            }
        }


class SearchRequest(BaseModel):
    """Job search request model."""

    query: str = Field(..., description="Search query string", min_length=1)
    platforms: list[str] = Field(
        default=["all"],
        description="Platforms to search on",
        examples=[["all"], ["linkedin", "dou"], ["djinni", "workua"]],
    )
    filters: Optional[SearchFilters] = Field(None, description="Advanced search filters")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "query": "python developer",
                "platforms": ["linkedin", "dou"],
                "filters": {
                    "keywords": ["python", "django"],
                    "location": "Kyiv",
                    "remote": True,
                    "experience_level": "senior",
                    "job_type": "full-time",
                },
            }
        }


class SearchResponse(BaseModel):
    """Job search response model."""

    jobs: list[JobListing] = Field(..., description="List of job listings found")
    total_count: int = Field(..., ge=0, description="Total number of jobs found")
    query: str = Field(..., description="Original search query")
    platforms: list[str] = Field(..., description="Platforms that were searched")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "jobs": [
                    {
                        "id": "1",
                        "title": "Backend Developer",
                        "company": "Company A",
                        "url": "https://example.com/job/1",
                        "source": "linkedin",
                        "location": "Remote",
                        "salary": "$80k-$120k",
                    }
                ],
                "total_count": 1,
                "query": "backend developer",
                "platforms": ["linkedin", "dou"],
            }
        }
