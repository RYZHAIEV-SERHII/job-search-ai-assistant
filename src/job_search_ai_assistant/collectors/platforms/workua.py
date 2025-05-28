"""Work.ua platform adapter implementation."""

from typing import Optional
from urllib.parse import urlencode

from .base import PlatformAdapter, PlatformConfig, SelectorConfig


class WorkUaAdapter(PlatformAdapter):
    """Work.ua platform adapter."""

    def __init__(self) -> None:
        """Initialize Work.ua adapter."""
        self._config = PlatformConfig(
            name="Work.ua",
            base_url="https://www.work.ua/jobs-it-",
            selectors=SelectorConfig(
                base_selector="div#pjax-job-list div.job-link",
                title="h2 > a",
                company="div.add-top-xs > span > b",
                location="div.add-top-xs span.middot + span:not(.nowrap)",
                salary="span.middot + span.nowrap",
                description="div#job-description",
                requirements="div.text-muted ul",
                url="h2 > a",
                apply_link="div.pull-right a.btn-default",
            ),
            # Wait for job listings container
            wait_for="div#pjax-job-list",
            # No dynamic loading
            dynamic_wait=None,
            # Work.ua uses standard pagination
            pagination_selector="ul.pagination li:last-child:not(.active) a",
            max_pages=10,
        )

    @property
    def config(self) -> PlatformConfig:
        """Get Work.ua configuration.

        Returns:
            PlatformConfig: Work-specific configuration
        """
        return self._config

    def build_search_url(self, keywords: list[str], location: Optional[str] = None) -> str:
        """Build Work.ua search URL.

        Args:
            keywords: Search keywords
            location: Optional location filter

        Returns:
            str: Complete Work.ua search URL
        """
        # Work.ua uses specific URL structure for IT jobs
        # Normalize keywords for URL
        keywords_param = "+".join(w.lower() for w in keywords)

        params = {
            "page": "1",  # Work.ua expects page as string
        }

        if location:
            # Work.ua uses city IDs, mapping common cities
            city_mapping = {
                "Київ": "kyiv",
                "Львів": "lviv",
                "Харків": "kharkiv",
                "Дніпро": "dnipro",
                "Одеса": "odesa",
            }
            normalized_city = city_mapping.get(location, location.lower())
            params["city"] = normalized_city

        # Work.ua URL structure: /jobs-it-[keywords]/?[params]
        base_url = f"{self.config.base_url}{keywords_param}/"
        if params:
            return f"{base_url}?{urlencode(params)}"
        return base_url

    def get_extraction_config(self) -> dict:
        """Get extraction configuration for Crawl4AI.

        Returns:
            dict: Configuration for JobExtractionStrategy
        """
        selectors = self.config.selectors
        return {
            "name": "Work.ua Jobs",
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
