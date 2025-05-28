"""Job search request and response schemas."""

from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field


class SalaryRange(BaseModel):
    """Salary range model."""

    min_amount: Optional[float] = Field(None, description="Minimum salary amount")
    max_amount: Optional[float] = Field(None, description="Maximum salary amount")
    currency: Optional[str] = Field(None, description="Salary currency (e.g., USD, EUR)")


class SearchCriteria(BaseModel):
    """Job search criteria model."""

    keywords: list[str] = Field(..., description="List of search keywords (e.g., ['python', 'fastapi'])")
    location: Optional[str] = Field(None, description="Desired job location")
    salary_range: Optional[SalaryRange] = Field(None, description="Target salary range")
    remote: bool = Field(False, description="Whether to search for remote positions only")
    experience_level: Optional[str] = Field(
        None,
        description="Required experience level",
        examples=["entry", "mid", "senior", "lead"],
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra: ClassVar[dict[str, Any]] = {
            "example": {
                "keywords": ["python", "fastapi", "postgresql"],
                "location": "Kyiv",
                "salary_range": {
                    "min_amount": 100000,
                    "max_amount": 150000,
                    "currency": "USD",
                },
                "remote": True,
                "experience_level": "senior",
            }
        }
