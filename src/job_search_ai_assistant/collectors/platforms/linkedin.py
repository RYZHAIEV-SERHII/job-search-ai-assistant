"""LinkedIn platform adapter implementation."""

from typing import Any
from urllib.parse import urlencode

from .base import PlatformAdapter, PlatformConfig, SelectorConfig


class LinkedInAdapter(PlatformAdapter):
    """LinkedIn platform adapter."""

    def __init__(self) -> None:
        """Initialize LinkedIn adapter."""
        self._config = PlatformConfig(
            name="LinkedIn",
            base_url="https://www.linkedin.com/jobs/search",
            selectors=SelectorConfig(
                base_selector="div.jobs-search__results-list li.jobs-search-results__list-item",
                title="h3.base-search-card__title",
                company="h4.base-search-card__subtitle",
                location="span.job-search-card__location",
                salary="span.job-search-card__salary-info",
                description="div.show-more-less-html__markup",
                requirements="div.description__text",
                url="a.base-card__full-link",
                apply_link="button.jobs-apply-button",
            ),
            # Wait for the job listings container to be present
            wait_for="div.jobs-search__results-list",
            # LinkedIn uses infinite scroll, so we need additional time for dynamic loading
            dynamic_wait=1.0,
            # "Show more jobs" button selector for pagination
            pagination_selector="button.infinite-scroller__show-more-button",
            max_pages=10,
        )

    @property
    def config(self) -> PlatformConfig:
        """Get LinkedIn configuration.

        Returns:
            PlatformConfig: LinkedIn-specific configuration
        """
        return self._config

    def build_search_url(self, keywords: list[str], location: str | None = None) -> str:
        """Build LinkedIn search URL.

        Args:
            keywords: Search keywords
            location: Optional location filter

        Returns:
            str: Complete LinkedIn search URL
        """
        params = {
            "keywords": " ".join(keywords),
            "f_TPR": "r86400",  # Last 24 hours
            "position": 1,
            "pageNum": 0,
        }

        if location:
            params["location"] = location

        url = f"{self.config.base_url!s}?{urlencode(params)}"
        return url

    def get_extraction_config(self) -> dict[str, Any]:
        """Get extraction configuration for Crawl4AI.

        Returns:
            dict[str, Any]: Configuration for JobExtractionStrategy
        """
        selectors = self.config.selectors
        return {
            "name": "LinkedIn Jobs",
            "baseSelector": selectors.base_selector,
            "fields": [
                {"name": "title", "selector": selectors.title, "type": "text"},
                {"name": "company", "selector": selectors.company, "type": "text"},
                {"name": "location", "selector": selectors.location, "type": "text"},
                {"name": "salary", "selector": selectors.salary, "type": "text", "optional": True},
                {"name": "description", "selector": selectors.description, "type": "text"},
                {"name": "requirements", "selector": selectors.requirements, "type": "text"},
                {"name": "url", "selector": selectors.url, "type": "attribute", "attribute": "href"},
                {
                    "name": "apply_url",
                    "selector": selectors.apply_link,
                    "type": "attribute",
                    "attribute": "href",
                    "optional": True,
                },
            ],
        }
