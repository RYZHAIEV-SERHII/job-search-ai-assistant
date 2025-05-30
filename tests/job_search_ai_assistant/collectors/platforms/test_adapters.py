"""Tests for platform-specific adapters."""

import pytest

from src.job_search_ai_assistant.collectors.platforms import (
    DjinniAdapter,
    DOUAdapter,
    LinkedInAdapter,
    WorkUaAdapter,
)


class TestLinkedInAdapter:
    """Tests for LinkedIn platform adapter."""

    def test_config_initialization(self):
        """Test adapter initialization and config."""
        adapter = LinkedInAdapter()
        config = adapter.config

        assert config.name == "LinkedIn"
        assert config.base_url == "https://www.linkedin.com/jobs/search"
        assert "jobs-search__results-list" in config.selectors.base_selector
        assert config.wait_for == "div.jobs-search__results-list"
        assert config.dynamic_wait == 1.0  # LinkedIn uses infinite scroll

    def test_build_search_url(self):
        """Test search URL construction."""
        adapter = LinkedInAdapter()

        # Basic search
        url = adapter.build_search_url(keywords=["python", "developer"])
        url_str = str(url)
        assert "keywords=python+developer" in url_str
        assert "f_TPR=r86400" in url_str  # Last 24 hours filter

        # Search with location
        url = adapter.build_search_url(keywords=["python"], location="Kyiv")
        url_str = str(url)
        assert "keywords=python" in url_str
        assert "location=Kyiv" in url_str


class TestDjinniAdapter:
    """Tests for Djinni platform adapter."""

    def test_config_initialization(self):
        """Test adapter initialization and config."""
        adapter = DjinniAdapter()
        config = adapter.config

        assert config.name == "Djinni"
        assert config.base_url == "https://djinni.co/jobs/"
        assert "list-jobs__item" in config.selectors.base_selector
        assert config.wait_for == "div.list-jobs"
        assert config.dynamic_wait is None  # Djinni uses regular pagination

    def test_build_search_url(self):
        """Test search URL construction."""
        adapter = DjinniAdapter()

        # Basic search
        url = adapter.build_search_url(keywords=["python", "developer"])
        url_str = str(url)
        assert "primary_keyword=python-developer" in url_str

        # Search with Ukrainian location
        url = adapter.build_search_url(keywords=["python"], location="Київ")
        url_str = str(url)
        assert "primary_keyword=python" in url_str
        assert "location=kyiv" in url_str


class TestDOUAdapter:
    """Tests for DOU platform adapter."""

    def test_config_initialization(self):
        """Test adapter initialization and config."""
        adapter = DOUAdapter()
        config = adapter.config

        assert config.name == "DOU"
        assert config.base_url == "https://jobs.dou.ua/vacancies/"
        assert config.selectors.base_selector == "li.l-vacancy"
        assert config.wait_for == "ul.lt"
        assert config.dynamic_wait == 1.0  # DOU uses AJAX loading
        assert config.pagination_selector == "a.more-btn"

    def test_build_search_url(self):
        """Test search URL construction."""
        adapter = DOUAdapter()

        # Test with category match
        url = adapter.build_search_url(keywords=["python"])
        url_str = str(url)
        assert "category=Python" in url_str
        assert "descr=1" in url_str  # Search in description

        # Test with location
        url = adapter.build_search_url(keywords=["devops"], location="Львів")
        url_str = str(url)
        assert "category=DevOps" in url_str
        assert "city=Lviv" in url_str


class TestWorkUaAdapter:
    """Tests for Work.ua platform adapter."""

    def test_config_initialization(self):
        """Test adapter initialization and config."""
        adapter = WorkUaAdapter()
        config = adapter.config

        assert config.name == "Work.ua"
        assert config.base_url == "https://www.work.ua/jobs-it-"
        assert "job-link" in config.selectors.base_selector
        assert config.wait_for == "div#pjax-job-list"
        assert config.dynamic_wait is None  # Work.ua uses standard pagination

    def test_build_search_url(self):
        """Test search URL construction."""
        adapter = WorkUaAdapter()

        # Basic IT job search
        url = adapter.build_search_url(keywords=["python", "developer"])
        url_str = str(url)
        assert "jobs-it-python+developer" in url_str
        assert "page=1" in url_str

        # Search with location
        url = adapter.build_search_url(keywords=["python"], location="Харків")
        url_str = str(url)
        assert "jobs-it-python" in url_str
        assert "city=kharkiv" in url_str


@pytest.mark.parametrize(
    "adapter_class,expected_fields",
    [
        (LinkedInAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
        (DjinniAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
        (DOUAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
        (WorkUaAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
    ],
)
def test_adapter_selectors_completeness(adapter_class, expected_fields):
    """Test that all adapters have required field selectors."""
    adapter = adapter_class()
    fields = [field["name"] for field in adapter.get_extraction_config()["fields"]]

    for field in expected_fields:
        assert field in fields, f"{adapter_class.__name__} missing selector for {field}"
