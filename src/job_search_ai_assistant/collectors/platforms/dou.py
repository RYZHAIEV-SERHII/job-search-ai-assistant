"""DOU platform adapter implementation."""

from typing import Any
from urllib.parse import urlencode

from .base import PlatformAdapter, PlatformConfig, SelectorConfig


class DOUAdapter(PlatformAdapter):
    """DOU platform adapter."""

    def __init__(self) -> None:
        """Initialize DOU adapter."""
        self._config = PlatformConfig(
            name="DOU",
            base_url="https://jobs.dou.ua/vacancies/",
            selectors=SelectorConfig(
                base_selector="li.l-vacancy",
                title="div.title > a",
                company="a.company",
                location="span.cities",
                salary="span.salary",
                description="div.text",
                requirements="div.requirements",
                url="div.title > a",
                apply_link="a.btn-apply",
            ),
            # Wait for job listings container
            wait_for="ul.lt",
            # DOU uses AJAX loading, need to wait for content
            dynamic_wait=1.0,
            # "More" button for loading additional jobs
            pagination_selector="a.more-btn",
            max_pages=10,
        )

    @property
    def config(self) -> PlatformConfig:
        """Get DOU configuration.

        Returns:
            PlatformConfig: DOU-specific configuration
        """
        return self._config

    def build_search_url(self, keywords: list[str], location: str | None = None) -> str:
        """Build DOU search URL.

        Args:
            keywords: Search keywords
            location: Optional location filter

        Returns:
            str: Complete DOU search URL
        """
        # DOU uses category system, map common keywords to their categories
        category_mapping = {
            "python": "Python",
            "javascript": "JavaScript",
            "java": "Java",
            "nodejs": "Node.js",
            "react": "React",
            "angular": "Angular",
            "devops": "DevOps",
            "qa": "QA",
            "android": "Android",
            "ios": "iOS",
        }

        params = {
            "search": " ".join(keywords),
            "descr": "1",  # Search in description
        }

        # Check if any keyword matches a category
        for keyword in keywords:
            if category := category_mapping.get(keyword.lower()):
                params["category"] = category
                break

        if location:
            # DOU uses specific city names
            city_mapping = {
                "Київ": "Kyiv",
                "Львів": "Lviv",
                "Харків": "Kharkiv",
                "Дніпро": "Dnipro",
                "Одеса": "Odesa",
            }
            normalized_city = city_mapping.get(location, location)
            params["city"] = normalized_city

        url = f"{self.config.base_url!s}?{urlencode(params)}"
        return url

    def get_extraction_config(self) -> dict[str, Any]:
        """Get extraction configuration for Crawl4AI.

        Returns:
            dict[str, Any]: Configuration for JobExtractionStrategy
        """
        selectors = self.config.selectors
        return {
            "name": "DOU Jobs",
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
