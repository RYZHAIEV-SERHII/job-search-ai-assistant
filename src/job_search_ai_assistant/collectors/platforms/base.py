"""Base configuration and utilities for platform-specific scrapers."""

from typing import Optional, Protocol

from pydantic import BaseModel, Field


class SelectorConfig(BaseModel):
    """Configuration for CSS selectors."""

    base_selector: str = Field(..., description="Base selector for job listings container")
    title: str = Field(..., description="Selector for job title")
    company: str = Field(..., description="Selector for company name")
    location: str = Field(..., description="Selector for job location")
    salary: Optional[str] = Field(None, description="Selector for salary information")
    description: str = Field(..., description="Selector for job description")
    requirements: str = Field(..., description="Selector for job requirements")
    url: Optional[str] = Field(None, description="Selector for job posting URL")
    apply_link: Optional[str] = Field(None, description="Selector for apply button/link")


class PlatformConfig(BaseModel):
    """Configuration for job platform."""

    name: str = Field(..., description="Platform name")
    base_url: str = Field(..., description="Base URL for job search")
    selectors: SelectorConfig = Field(..., description="CSS selectors for job data extraction")
    wait_for: Optional[str] = Field(None, description="Element to wait for before extraction")
    dynamic_wait: Optional[float] = Field(None, description="Additional wait time for dynamic content")
    pagination_selector: Optional[str] = Field(None, description="Selector for pagination element")
    max_pages: Optional[int] = Field(10, description="Maximum number of pages to scrape")


class PlatformAdapter(Protocol):
    """Protocol for platform-specific adapters."""

    @property
    def config(self) -> PlatformConfig:
        """Get platform configuration.

        Returns:
            PlatformConfig: Platform-specific configuration
        """
        ...

    def build_search_url(self, keywords: list[str], location: Optional[str] = None) -> str:
        """Build search URL with parameters.

        Args:
            keywords: Search keywords
            location: Optional location filter

        Returns:
            str: Complete search URL
        """
        ...

    def get_extraction_config(self) -> dict:
        """Get extraction configuration for Crawl4AI.

        Returns:
            dict: Configuration for JobExtractionStrategy
        """
        ...
