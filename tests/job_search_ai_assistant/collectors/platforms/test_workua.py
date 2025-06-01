"""Tests for Work.ua platform adapter."""

import pytest

from src.job_search_ai_assistant.collectors.platforms import (
    WorkUaAdapter,
)


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
        (WorkUaAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
    ],
)
def test_adapter_selectors_completeness(adapter_class, expected_fields):
    """Test that all adapters have required field selectors."""
    adapter = adapter_class()
    fields = [field["name"] for field in adapter.get_extraction_config()["fields"]]

    for field in expected_fields:
        assert field in fields, f"{adapter_class.__name__} missing selector for {field}"
