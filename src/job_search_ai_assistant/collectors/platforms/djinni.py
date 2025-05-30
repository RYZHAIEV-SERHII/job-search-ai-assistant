"""Djinni platform adapter implementation."""

from typing import Any
from urllib.parse import urlencode

from .base import PlatformAdapter, PlatformConfig, SelectorConfig


class DjinniAdapter(PlatformAdapter):
    """Djinni platform adapter."""

    def __init__(self) -> None:
        """Initialize Djinni adapter."""
        self._config = PlatformConfig(
            name="Djinni",
            base_url="https://djinni.co/jobs/",
            selectors=SelectorConfig(
                base_selector="div.list-jobs__item",
                title="div.job-list-item__title > a",
                company="a.mr-2",
                location="span.location-text",
                salary="span.public-salary-item",
                description="div.job-post__description-text",
                requirements="ul.job-additional-info--item-text",
                url="div.job-list-item__title > a",
                apply_link="a.btn-green",
            ),
            # Wait for job listings container
            wait_for="div.list-jobs",
            # Static page, no dynamic wait needed
            dynamic_wait=None,
            # Pagination button
            pagination_selector="li.page-item > a.page-link:not(.disabled)",
            max_pages=10,
        )

    @property
    def config(self) -> PlatformConfig:
        """Get Djinni configuration.

        Returns:
            PlatformConfig: Djinni-specific configuration
        """
        return self._config

    def build_search_url(self, keywords: list[str], location: str | None = None) -> str:
        """Build Djinni search URL.

        Args:
            keywords: Search keywords
            location: Optional location filter

        Returns:
            str: Complete Djinni search URL
        """
        # Djinni uses kebab-case for keywords in URL
        keywords_param = "-".join(keywords).lower()

        params = {
            "primary_keyword": keywords_param,
            "page": "1",  # Djinni expects page as string
        }

        if location:
            # Djinni uses specific location identifiers
            location_mapping = {
                "Київ": "kyiv",
                "Львів": "lviv",
                "Харків": "kharkiv",
                "Дніпро": "dnipro",
                "Одеса": "odesa",
            }
            normalized_location = location_mapping.get(location, location.lower())
            params["location"] = normalized_location

        url = f"{self.config.base_url!s}?{urlencode(params)}" if params else str(self.config.base_url)
        return url

    def get_extraction_config(self) -> dict[str, Any]:
        """Get extraction configuration for Crawl4AI.

        Returns:
            dict[str, Any]: Configuration for JobExtractionStrategy
        """
        selectors = self.config.selectors
        return {
            "name": "Djinni Jobs",
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
