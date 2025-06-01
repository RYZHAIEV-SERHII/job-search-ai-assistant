"""Tests for LinkedIn platform adapter."""

import pytest

from src.job_search_ai_assistant.collectors.platforms import (
    LinkedInAdapter,
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


@pytest.mark.parametrize(
    "adapter_class,expected_fields",
    [
        (LinkedInAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
    ],
)
def test_adapter_selectors_completeness(adapter_class, expected_fields):
    """Test that all adapters have required field selectors."""
    adapter = adapter_class()
    fields = [field["name"] for field in adapter.get_extraction_config()["fields"]]

    for field in expected_fields:
        assert field in fields, f"{adapter_class.__name__} missing selector for {field}"
