"""Tests for JobScraperClient."""

import pytest
from crawl4ai import BrowserConfig
from pytest_mock import MockerFixture

from src.job_search_ai_assistant.api.schemas.search import SearchFilters
from src.job_search_ai_assistant.collectors.crawl4ai.client import JobScraperClient
from src.job_search_ai_assistant.collectors.crawl4ai.exceptions import ScrapingError
from src.job_search_ai_assistant.collectors.crawl4ai.extractors import JobExtractionStrategy

# Import the mock from conftest
from tests.conftest import MockJobPosting as JobPosting


class TestJobScraperClient:
    """Test cases for JobScraperClient."""

    def test_init_default_config(self):
        """Test initialization with default configuration."""
        client = JobScraperClient()

        assert client.browser_config.headless is True
        assert client.browser_config.viewport_width == 1920
        assert client.browser_config.viewport_height == 1080
        assert isinstance(client.css_strategy, JobExtractionStrategy)
        assert client.llm_strategy is None

    def test_init_custom_browser_config(self):
        """Test initialization with custom browser configuration."""
        custom_config = BrowserConfig(
            headless=False,
            viewport_width=1366,
            viewport_height=768,
        )
        client = JobScraperClient(browser_config=custom_config)

        assert client.browser_config == custom_config
        assert client.browser_config.headless is False
        assert client.browser_config.viewport_width == 1366

    def test_init_with_llm(self, mocker: MockerFixture):
        """Test initialization with LLM enabled."""
        # Mock LLMExtractionStrategy
        mock_llm_strategy = mocker.patch("src.job_search_ai_assistant.collectors.crawl4ai.client.LLMExtractionStrategy")

        client = JobScraperClient(use_llm=True)

        assert client.llm_strategy is not None
        mock_llm_strategy.assert_called_once()

    def test_update_css_selectors(self):
        """Test updating CSS selectors for a platform."""
        client = JobScraperClient()

        platform_selectors = {
            "baseSelector": "div.custom-job",
            "fields": {
                "title": "h3.job-title-custom",
                "company": "span.company-custom",
            },
        }

        client.update_css_selectors(platform_selectors)

        # Verify the strategy was configured
        assert isinstance(client.css_strategy, JobExtractionStrategy)

    def test_get_extraction_strategy_css_only(self):
        """Test getting extraction strategy when only CSS is available."""
        client = JobScraperClient(use_llm=False)

        strategy = client._get_extraction_strategy(llm_fallback=True)
        assert strategy == client.css_strategy

        strategy = client._get_extraction_strategy(llm_fallback=False)
        assert strategy == client.css_strategy

    def test_get_extraction_strategy_with_llm_fallback(self, mocker: MockerFixture):
        """Test getting extraction strategy with LLM fallback."""
        mocker.patch("src.job_search_ai_assistant.collectors.crawl4ai.client.LLMExtractionStrategy")

        client = JobScraperClient(use_llm=True)

        # Should return CSS strategy when llm_fallback is False
        strategy = client._get_extraction_strategy(llm_fallback=False)
        assert strategy == client.css_strategy

        # Should return LLM strategy when llm_fallback is True
        strategy = client._get_extraction_strategy(llm_fallback=True)
        assert strategy == client.llm_strategy

    @pytest.mark.asyncio
    async def test_scrape_jobs_success(self, mocker: MockerFixture):
        """Test successful job scraping."""
        # Create a mock result dict with proper get method
        mock_result_dict = {
            "success": True,
            "content": [
                {
                    "title": "Python Developer",
                    "company": "Tech Corp",
                    "location": "Kyiv",
                    "salary": "$5000",
                    "description": "Python developer needed",
                    "requirements": ["Python", "FastAPI"],
                    "url": "https://example.com/job/1",
                }
            ],
        }

        # Create a proper async generator
        async def mock_async_generator():
            yield mock_result_dict

        # Create a mock crawler with proper async context manager support
        class MockCrawler:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

            async def arun(self, url, config):
                return mock_async_generator()

        mocker.patch(
            "src.job_search_ai_assistant.collectors.crawl4ai.client.AsyncWebCrawler", return_value=MockCrawler()
        )

        client = JobScraperClient()
        criteria = SearchFilters(keywords=["Python"])

        jobs = await client.scrape_jobs(
            url="https://example.com",
            platform="test_platform",
            criteria=criteria,
        )

        assert len(jobs) == 1
        assert jobs[0].title == "Python Developer"
        assert jobs[0].platform == "test_platform"

    @pytest.mark.asyncio
    async def test_scrape_jobs_with_wait_params(self, mocker: MockerFixture):
        """Test job scraping with wait parameters."""
        # Create a mock result dict
        mock_result_dict = {"success": True, "content": []}

        # Create a proper async generator
        async def mock_async_generator():
            yield mock_result_dict

        # Create a mock crawler with proper async context manager support
        class MockCrawler:
            def __init__(self):
                self.arun_calls = []

            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

            async def arun(self, url, config):
                self.arun_calls.append((url, config))
                return mock_async_generator()

        mock_crawler = MockCrawler()
        mocker.patch(
            "src.job_search_ai_assistant.collectors.crawl4ai.client.AsyncWebCrawler", return_value=mock_crawler
        )

        client = JobScraperClient()
        criteria = SearchFilters()

        await client.scrape_jobs(
            url="https://example.com",
            platform="test",
            criteria=criteria,
            wait_for=".job-list",
            wait_timeout=5000,
        )

        # Verify the config was created with wait parameters
        assert len(mock_crawler.arun_calls) == 1
        _, config = mock_crawler.arun_calls[0]
        assert config.wait_for == ".job-list"
        # Note: wait_timeout is not a direct attribute of CrawlerRunConfig

    @pytest.mark.asyncio
    async def test_scrape_jobs_css_failure_llm_fallback(self, mocker: MockerFixture):
        """Test LLM fallback when CSS extraction fails."""
        # Create mock result dicts
        first_result = {"success": False, "error": "CSS extraction failed"}
        second_result = {
            "success": True,
            "content": [
                {
                    "title": "LLM Extracted Job",
                    "company": "Company",
                    "location": "Location",
                    "description": "Description",
                    "requirements": ["Req1"],
                    "url": "https://example.com/job",
                }
            ],
        }

        # Create proper async generators for both calls
        async def first_gen():
            yield first_result

        async def second_gen():
            yield second_result

        # Create a mock crawler with proper async context manager support
        class MockCrawler:
            def __init__(self):
                self.call_count = 0
                self.generators = [first_gen(), second_gen()]

            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

            async def arun(self, url, config):
                result = self.generators[self.call_count]
                self.call_count += 1
                return result

        mock_crawler = MockCrawler()
        mocker.patch(
            "src.job_search_ai_assistant.collectors.crawl4ai.client.AsyncWebCrawler", return_value=mock_crawler
        )

        # Mock LLMExtractionStrategy to return a proper instance
        from crawl4ai.extraction_strategy import ExtractionStrategy

        mock_llm_instance = mocker.MagicMock(spec=ExtractionStrategy)
        mocker.patch(
            "src.job_search_ai_assistant.collectors.crawl4ai.client.LLMExtractionStrategy",
            return_value=mock_llm_instance,
        )

        client = JobScraperClient(use_llm=True)
        criteria = SearchFilters()

        jobs = await client.scrape_jobs(
            url="https://example.com",
            platform="test",
            criteria=criteria,
            llm_fallback=True,
        )

        assert len(jobs) == 1
        assert jobs[0].title == "LLM Extracted Job"
        assert mock_crawler.call_count == 2

    @pytest.mark.asyncio
    async def test_scrape_jobs_total_failure(self, mocker: MockerFixture):
        """Test scraping failure with both strategies."""
        # Create a mock result dict
        failed_result = {"success": False, "error": "Total failure"}

        # Create a proper async generator
        async def failed_gen():
            yield failed_result

        # Create a mock crawler with proper async context manager support
        class MockCrawler:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

            async def arun(self, url, config):
                return failed_gen()

        mocker.patch(
            "src.job_search_ai_assistant.collectors.crawl4ai.client.AsyncWebCrawler", return_value=MockCrawler()
        )

        client = JobScraperClient()
        criteria = SearchFilters()

        with pytest.raises(ScrapingError) as exc_info:
            await client.scrape_jobs(
                url="https://example.com",
                platform="test",
                criteria=criteria,
            )

        assert exc_info.value.error_type == "EXTRACTION_ERROR"
        assert "test" in exc_info.value.details["platform"]

    def test_filter_jobs_by_keywords(self):
        """Test filtering jobs by keywords."""
        client = JobScraperClient()

        jobs = [
            JobPosting(
                title="Python Developer",
                company="Company A",
                location="Kyiv",
                description="Python and Django developer",
                requirements=["Python"],
                url="https://example.com/1",
            ),
            JobPosting(
                title="Java Developer",
                company="Company B",
                location="Kyiv",
                description="Java Spring developer",
                requirements=["Java"],
                url="https://example.com/2",
            ),
            JobPosting(
                title="Full Stack Developer",
                company="Company C",
                location="Kyiv",
                description="Python and React developer",
                requirements=["Python", "React"],
                url="https://example.com/3",
            ),
        ]

        criteria = SearchFilters(keywords=["Python"])
        filtered = client._filter_jobs(jobs, criteria)

        assert len(filtered) == 2
        assert all("Python" in job.title or "Python" in job.description for job in filtered)

    def test_filter_jobs_by_location(self):
        """Test filtering jobs by location."""
        client = JobScraperClient()

        jobs = [
            JobPosting(
                title="Developer",
                company="Company A",
                location="Kyiv, Ukraine",
                description="Developer needed",
                requirements=["Python"],
                url="https://example.com/1",
            ),
            JobPosting(
                title="Developer",
                company="Company B",
                location="Lviv, Ukraine",
                description="Developer needed",
                requirements=["Python"],
                url="https://example.com/2",
            ),
        ]

        criteria = SearchFilters(location="Kyiv")
        filtered = client._filter_jobs(jobs, criteria)

        assert len(filtered) == 1
        assert filtered[0].location == "Kyiv, Ukraine"

    def test_filter_jobs_remote(self):
        """Test filtering remote jobs."""
        client = JobScraperClient()

        jobs = [
            JobPosting(
                title="Remote Developer",
                company="Company A",
                location="Anywhere",
                description="Remote work available",
                requirements=["Python"],
                url="https://example.com/1",
            ),
            JobPosting(
                title="Office Developer",
                company="Company B",
                location="Kyiv",
                description="Office work only",
                requirements=["Python"],
                url="https://example.com/2",
            ),
            JobPosting(
                title="Hybrid Developer",
                company="Company C",
                location="Kyiv",
                description="Remote or office work",
                requirements=["Python"],
                url="https://example.com/3",
            ),
        ]

        criteria = SearchFilters(remote=True)
        filtered = client._filter_jobs(jobs, criteria)

        assert len(filtered) == 2
        assert any("remote" in job.description.lower() or "віддалено" in job.description.lower() for job in filtered)

    def test_filter_jobs_combined_criteria(self):
        """Test filtering with multiple criteria."""
        client = JobScraperClient()

        jobs = [
            JobPosting(
                title="Python Developer",
                company="Company A",
                location="Kyiv, Ukraine",
                description="Remote Python developer",
                requirements=["Python"],
                url="https://example.com/1",
            ),
            JobPosting(
                title="Python Developer",
                company="Company B",
                location="Lviv, Ukraine",
                description="Remote Python developer",
                requirements=["Python"],
                url="https://example.com/2",
            ),
            JobPosting(
                title="Java Developer",
                company="Company C",
                location="Kyiv, Ukraine",
                description="Remote Java developer",
                requirements=["Java"],
                url="https://example.com/3",
            ),
        ]

        criteria = SearchFilters(
            keywords=["Python"],
            location="Kyiv",
            remote=True,
        )
        filtered = client._filter_jobs(jobs, criteria)

        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"
        assert filtered[0].location == "Kyiv, Ukraine"

    def test_filter_jobs_no_criteria(self):
        """Test filtering with no criteria returns all jobs."""
        client = JobScraperClient()

        jobs = [
            JobPosting(
                title="Developer 1",
                company="Company A",
                location="Kyiv",
                description="Description",
                requirements=["Req"],
                url="https://example.com/1",
            ),
            JobPosting(
                title="Developer 2",
                company="Company B",
                location="Lviv",
                description="Description",
                requirements=["Req"],
                url="https://example.com/2",
            ),
        ]

        criteria = SearchFilters()
        filtered = client._filter_jobs(jobs, criteria)

        assert len(filtered) == len(jobs)
        assert filtered == jobs
