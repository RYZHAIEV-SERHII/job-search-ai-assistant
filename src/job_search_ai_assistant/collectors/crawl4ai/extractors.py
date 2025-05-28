"""Custom extraction strategies for job scraping."""

from crawl4ai.extraction_strategy import JsonCssExtractionStrategy


class JobExtractionStrategy(JsonCssExtractionStrategy):
    """Custom extraction strategy for job listings."""

    def __init__(self, config: dict) -> None:
        """Initialize the extraction strategy.

        Args:
            config: Base configuration including selectors and fields.
        """
        super().__init__(config)
        self._base_config = config.copy()

    def configure_for_platform(self, platform_selectors: dict[str, str]) -> None:
        """Configure the strategy for a specific platform.

        Args:
            platform_selectors: Platform-specific CSS selectors.
        """
        updated_config = self._base_config.copy()
        if "baseSelector" in platform_selectors:
            updated_config["baseSelector"] = platform_selectors["baseSelector"]
        if "fields" in platform_selectors:
            updated_config["fields"] = platform_selectors["fields"]

        # Re-initialize with updated config by calling parent class constructor
        super().__init__(updated_config)
