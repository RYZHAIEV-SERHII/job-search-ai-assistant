"""Tests for Djinni platform adapter."""

import pytest

from src.job_search_ai_assistant.collectors.platforms import (
    DjinniAdapter,
)


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


@pytest.mark.parametrize(
    "adapter_class,expected_fields",
    [
        (DjinniAdapter, ["title", "company", "location", "salary", "description", "requirements", "url"]),
    ],
)
def test_adapter_selectors_completeness(adapter_class, expected_fields):
    """Test that all adapters have required field selectors."""
    adapter = adapter_class()
    fields = [field["name"] for field in adapter.get_extraction_config()["fields"]]

    for field in expected_fields:
        assert field in fields, f"{adapter_class.__name__} missing selector for {field}"
