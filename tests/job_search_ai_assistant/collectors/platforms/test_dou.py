"""Tests for DOU platform adapter."""

import pytest

from src.job_search_ai_assistant.collectors.platforms import (
    DOUAdapter,
)


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


@pytest.mark.parametrize(
    "adapter_class,expected_fields",
    [
        (DOUAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
    ],
)
def test_adapter_selectors_completeness(adapter_class, expected_fields):
    """Test that all adapters have required field selectors."""
    adapter = adapter_class()
    fields = [field["name"] for field in adapter.get_extraction_config()["fields"]]

    for field in expected_fields:
        assert field in fields, f"{adapter_class.__name__} missing selector for {field}"
