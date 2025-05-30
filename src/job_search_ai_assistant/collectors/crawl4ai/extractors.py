"""Custom extraction strategies for job scraping."""

from typing import Any

from crawl4ai import LLMConfig
from crawl4ai.extraction_strategy import (
    ExtractionStrategy,
    JsonCssExtractionStrategy,
)
from crawl4ai.extraction_strategy import (
    LLMExtractionStrategy as BaseLLMExtractionStrategy,
)

from .models import JobPosting


class JobExtractionStrategy(JsonCssExtractionStrategy):
    """Custom extraction strategy for job listings using CSS selectors."""

    def __init__(self, config: dict[str, Any]) -> None:
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


class JobLLMExtractionStrategy(BaseLLMExtractionStrategy):
    """Custom LLM-based extraction strategy for job listings."""

    def __init__(
        self,
        llm_config: LLMConfig | None = None,
    ) -> None:
        """Initialize the LLM extraction strategy.

        Args:
            llm_config: Optional custom LLM configuration
        """
        default_config = LLMConfig(
            provider="openai/gpt-4",
            max_tokens=4096,  # Large enough for job listings
        )

        super().__init__(
            llm_config=llm_config or default_config,
            schema=JobPosting.model_json_schema(),
            extraction_type="schema",
            instruction="""Extract job posting information from the provided HTML content.

Important Guidelines:
1. Extract facts exactly as presented in the content
2. Keep titles and company names in their original form
3. Use complete sentences for description and requirements
4. Preserve exact salary information if available
5. Include complete URLs for job links
6. Extract all listed requirements without modification
7. Leave optional fields empty if information is not present
8. Ensure location follows [City, Country] format when possible

Expected Fields:
- title: Exact job title as shown
- company: Complete company name
- location: Primary job location(s)
- salary: Original salary format if available
- description: Complete job description
- requirements: List of all required skills and qualifications
- url: Full job posting URL if available
- apply_url: Direct application link if available

Important: Extract only information explicitly stated in the content.
Do not make assumptions or add information not present in the HTML.""",
            chunk_token_threshold=1400,  # Reasonable size for job listings
            apply_chunking=True,
            input_format="html",
            extra_args={"temperature": 0.1},  # Low temperature for factual extraction
        )

    async def extract_with_retries(
        self,
        html: str,
        url: str,
        ix: int = 0,
        max_retries: int = 2,
        fallback_provider: str | None = "openai/gpt-3.5-turbo",
    ) -> dict[str, Any]:
        """Extract job information with retry logic.

        Args:
            html: HTML content to extract from
            url: URL of the page being processed
            ix: Index of the current item being processed
            max_retries: Maximum number of retry attempts
            fallback_provider: Optional fallback LLM provider

        Returns:
            dict[str, Any]: Extracted job information
        """
        for attempt in range(max_retries):
            try:
                # Call parent's extract method but override the non-async extract
                result = super().extract(ix=ix, html=html, url=url)
                if result:
                    return result[0] if isinstance(result, list) else result
                else:
                    return {}
            except Exception:
                if attempt == max_retries - 1 and fallback_provider:
                    # Try fallback provider on last attempt
                    self.llm_config.provider = fallback_provider
                    result = super().extract(ix=ix, html=html, url=url)
                    if result:
                        return result[0] if isinstance(result, list) else result
                    else:
                        return {}
                elif attempt < max_retries - 1:
                    continue
                raise
        return {}  # Return empty dict if all attempts fail


def create_extraction_strategy(
    strategy_type: str = "css",
    css_config: dict[str, Any] | None = None,
    llm_config: LLMConfig | None = None,
) -> ExtractionStrategy:
    """Factory function to create appropriate extraction strategy.

    Args:
        strategy_type: Type of strategy ("css" or "llm")
        css_config: Configuration for CSS-based extraction
        llm_config: Configuration for LLM-based extraction

    Returns:
        Configured extraction strategy
    """
    if strategy_type == "llm":
        return JobLLMExtractionStrategy(llm_config=llm_config)
    else:
        return JobExtractionStrategy(config=css_config or {})
