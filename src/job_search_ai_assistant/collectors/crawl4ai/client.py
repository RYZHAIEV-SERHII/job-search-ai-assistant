"""AsyncWebCrawler setup and configuration for job scraping."""

from typing import Optional

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMConfig,
)
from crawl4ai.extraction_strategy import (
    ExtractionStrategy,
    LLMExtractionStrategy,
)

from ...api.schemas.search import SearchFilters
from .exceptions import ScrapingError
from .extractors import JobExtractionStrategy
from .models import JobPosting


class JobScraperClient:
    """Crawl4AI-based job scraping client."""

    def __init__(
        self,
        browser_config: Optional[BrowserConfig] = None,
        use_llm: bool = False,
    ) -> None:
        """Initialize the job scraper client.

        Args:
            browser_config: Custom browser configuration. If None, uses default settings.
            use_llm: Whether to use LLM-based extraction as fallback.
        """
        self.browser_config = browser_config or BrowserConfig(
            headless=True,
            viewport_width=1920,
            viewport_height=1080,
        )

        # CSS-based extraction strategy (primary)
        self.css_strategy = JobExtractionStrategy(
            {
                "name": "Job Listings",
                "baseSelector": "div.job-posting",  # Default selector, updated per platform
                "fields": [
                    {"name": "title", "selector": "h2.job-title", "type": "text"},
                    {"name": "company", "selector": "div.company-name", "type": "text"},
                    {"name": "location", "selector": "div.job-location", "type": "text"},
                    {"name": "salary", "selector": "div.salary", "type": "text", "optional": True},
                    {"name": "description", "selector": "div.job-description", "type": "text"},
                    {"name": "requirements", "selector": "ul.requirements li", "type": "text_array"},
                    {"name": "url", "selector": "a.job-link", "type": "attribute", "attribute": "href"},
                ],
            }
        )

        # Optional LLM-based extraction strategy (fallback)
        self.llm_strategy = None
        if use_llm:
            self.llm_strategy = LLMExtractionStrategy(
                llm_config=LLMConfig(provider="openai/gpt-4"),
                schema=JobPosting.model_json_schema(),
                extraction_type="schema",
                instruction="""
                Extract detailed job posting information including:
                - Job title and company name
                - Location and salary details if available
                - Complete job description
                - List of requirements and qualifications
                - Job posting URL
                """,
            )

    def update_css_selectors(self, platform_selectors: dict[str, str]) -> None:
        """Update CSS selectors for a specific platform.

        Args:
            platform_selectors: Platform-specific CSS selectors.
        """
        if isinstance(self.css_strategy, JobExtractionStrategy):
            self.css_strategy.configure_for_platform(platform_selectors)

    def _get_extraction_strategy(self, llm_fallback: bool = True) -> ExtractionStrategy:
        """Get the appropriate extraction strategy.

        Args:
            llm_fallback: Whether to try LLM extraction if CSS extraction fails.

        Returns:
            The selected extraction strategy.
        """
        return self.llm_strategy if llm_fallback and self.llm_strategy else self.css_strategy

    async def scrape_jobs(  # noqa: PLR0913
        self,
        url: str,
        platform: str,
        criteria: SearchFilters,
        wait_for: Optional[str] = None,
        wait_timeout: Optional[int] = None,
        llm_fallback: bool = True,
    ) -> list[JobPosting]:
        """Execute job scraping with fallback strategies.

        Args:
            url: The URL to scrape.
            platform: Platform name for metadata.
            criteria: Search criteria for filtering.
            wait_for: CSS selector to wait for before extraction.
            wait_timeout: Timeout in milliseconds to wait for selector.
            llm_fallback: Whether to try LLM extraction if CSS extraction fails.

        Returns:
            List of extracted job postings.

        Raises:
            ScrapingError: If scraping fails with both strategies.
        """
        # Build config based on provided parameters
        config_args = {
            "extraction_strategy": self._get_extraction_strategy(llm_fallback),
            "cache_mode": CacheMode.BYPASS,  # Always fetch fresh data
        }

        if wait_for is not None:
            config_args["wait_for"] = wait_for

        config = CrawlerRunConfig(**config_args)

        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(url=url, config=config)
            result_dict = await result.__anext__()  # Get first result from AsyncGenerator

            if not result_dict.get("success") and llm_fallback and self.llm_strategy:
                # Try LLM extraction as fallback
                config.extraction_strategy = self.llm_strategy
                result = await crawler.arun(url=url, config=config)
                result_dict = await result.__anext__()

            if not result_dict.get("success"):
                raise ScrapingError(
                    message=f"Failed to scrape {platform}: {result_dict.get('error', 'Unknown error')}",
                    error_type="EXTRACTION_ERROR",
                    details={
                        "platform": platform,
                        "url": url,
                        "error": result_dict.get("error", "Unknown error"),
                    },
                )

            extracted_content = result_dict.get("content", [])
            jobs = [JobPosting.model_validate({**job, "platform": platform}) for job in extracted_content]

            # Filter jobs based on search criteria
            filtered_jobs = self._filter_jobs(jobs, criteria)
            return filtered_jobs

    def _filter_jobs(
        self,
        jobs: list[JobPosting],
        criteria: SearchFilters,
    ) -> list[JobPosting]:
        """Filter jobs based on search criteria.

        Args:
            jobs: List of job postings to filter.
            criteria: Search criteria to apply.

        Returns:
            Filtered list of job postings.
        """
        filtered = jobs

        # Apply filters based on search criteria
        if criteria.keywords:
            filtered = [
                job
                for job in filtered
                if any(
                    keyword.lower() in job.title.lower() or keyword.lower() in job.description.lower()
                    for keyword in criteria.keywords
                )
            ]

        if criteria.location:
            filtered = [job for job in filtered if criteria.location.lower() in job.location.lower()]

        if criteria.salary_range:
            # TODO: Implement salary range filtering
            # This requires parsing salary strings into comparable values
            pass

        if criteria.remote:
            filtered = [
                job
                for job in filtered
                if any(term.lower() in job.description.lower() for term in ["remote", "віддалено", "дистанційно"])
            ]

        return filtered
