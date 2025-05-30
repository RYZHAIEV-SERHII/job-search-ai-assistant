"""Base configuration and utilities for platform-specific scrapers."""

from typing import Any, Protocol

from pydantic import BaseModel, Field


class SelectorConfig(BaseModel):
    """Configuration for CSS selectors."""

    base_selector: str = Field(..., description="Base selector for job listings container")
    title: str = Field(..., description="Selector for job title")
    company: str = Field(..., description="Selector for company name")
    location: str = Field(..., description="Selector for job location")
    salary: str | None = Field(None, description="Selector for salary information")
    description: str = Field(..., description="Selector for job description")
    requirements: str = Field(..., description="Selector for job requirements")
    url: str | None = Field(None, description="Selector for job posting URL")
    apply_link: str | None = Field(None, description="Selector for apply button/link")


class PlatformConfig(BaseModel):
    """Configuration for job platform."""

    name: str = Field(..., description="Platform name")
    base_url: str = Field(..., description="Base URL for job search")
    selectors: SelectorConfig = Field(..., description="CSS selectors for job data extraction")
    wait_for: str | None = Field(None, description="Element to wait for before extraction")
    dynamic_wait: float | None = Field(None, description="Additional wait time for dynamic content")
    pagination_selector: str | None = Field(None, description="Selector for pagination element")
    max_pages: int | None = Field(10, description="Maximum number of pages to scrape")

    class Config:
        """Model configuration."""

        protected_namespaces = ()  # Allow arbitrary fields
        arbitrary_types_allowed = True  # Allow HttpUrl type


class PlatformAdapter(Protocol):
    """Protocol for platform-specific adapters."""

    @property
    def config(self) -> PlatformConfig:
        """Get platform configuration.

        Returns:
            PlatformConfig: Platform-specific configuration
        """
        ...

    def build_search_url(self, keywords: list[str], location: str | None = None) -> str:
        """Build search URL with parameters.

        Args:
            keywords: Search keywords
            location: Optional location filter

        Returns:
            str: Complete search URL
        """
        ...

    def get_extraction_config(self) -> dict[str, Any]:
        """Get extraction configuration for Crawl4AI.

        Returns:
            dict[str, Any]: Configuration for JobExtractionStrategy
        """
        ...
