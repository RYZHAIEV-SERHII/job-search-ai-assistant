"""Tests for crawl4ai exceptions module."""

import pytest

from src.job_search_ai_assistant.collectors.crawl4ai.exceptions import (
    ExtractionError,
    NetworkError,
    RateLimitError,
    ScrapingError,
    ValidationError,
)


class TestScrapingError:
    """Test ScrapingError base exception."""

    def test_init_with_minimal_params(self):
        """Test initialization with minimal parameters."""
        error = ScrapingError(message="Test error", error_type="TEST_ERROR")

        assert error.message == "Test error"
        assert error.error_type == "TEST_ERROR"
        assert error.details == {}
        assert str(error) == "TEST_ERROR: Test error"

    def test_init_with_details(self):
        """Test initialization with details."""
        details = {"code": 404, "url": "https://example.com"}
        error = ScrapingError(message="Not found", error_type="HTTP_ERROR", details=details)

        assert error.message == "Not found"
        assert error.error_type == "HTTP_ERROR"
        assert error.details == details
        assert str(error) == "HTTP_ERROR: Not found"

    def test_str_representation(self):
        """Test string representation of the error."""
        error = ScrapingError(message="Test message", error_type="TEST_TYPE")
        assert str(error) == "TEST_TYPE: Test message"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        details = {"retry_count": 3, "timeout": 30}
        error = ScrapingError(message="Connection timeout", error_type="TIMEOUT_ERROR", details=details)

        result = error.to_dict()
        assert result == {"error_type": "TIMEOUT_ERROR", "message": "Connection timeout", "details": details}

    def test_to_dict_without_details(self):
        """Test conversion to dictionary without details."""
        error = ScrapingError(message="Simple error", error_type="SIMPLE_ERROR")

        result = error.to_dict()
        assert result == {"error_type": "SIMPLE_ERROR", "message": "Simple error", "details": {}}


class TestExtractionError:
    """Test ExtractionError exception."""

    def test_init_without_details(self):
        """Test initialization without details."""
        error = ExtractionError(message="Failed to extract data")

        assert error.message == "Failed to extract data"
        assert error.error_type == "EXTRACTION_ERROR"
        assert error.details == {}
        assert str(error) == "EXTRACTION_ERROR: Failed to extract data"

    def test_init_with_details(self):
        """Test initialization with details."""
        details = {"selector": ".job-title", "element_count": 0}
        error = ExtractionError(message="No elements found", details=details)

        assert error.message == "No elements found"
        assert error.error_type == "EXTRACTION_ERROR"
        assert error.details == details

    def test_inheritance(self):
        """Test that ExtractionError inherits from ScrapingError."""
        error = ExtractionError(message="Test")
        assert isinstance(error, ScrapingError)
        assert isinstance(error, Exception)


class TestNetworkError:
    """Test NetworkError exception."""

    def test_init_without_details(self):
        """Test initialization without details."""
        error = NetworkError(message="Connection refused")

        assert error.message == "Connection refused"
        assert error.error_type == "NETWORK_ERROR"
        assert error.details == {}
        assert str(error) == "NETWORK_ERROR: Connection refused"

    def test_init_with_details(self):
        """Test initialization with details."""
        details = {"status_code": 503, "retry_after": 60}
        error = NetworkError(message="Service unavailable", details=details)

        assert error.message == "Service unavailable"
        assert error.error_type == "NETWORK_ERROR"
        assert error.details == details

    def test_inheritance(self):
        """Test that NetworkError inherits from ScrapingError."""
        error = NetworkError(message="Test")
        assert isinstance(error, ScrapingError)
        assert isinstance(error, Exception)


class TestRateLimitError:
    """Test RateLimitError exception."""

    def test_init_without_details(self):
        """Test initialization without details."""
        error = RateLimitError(message="Rate limit exceeded")

        assert error.message == "Rate limit exceeded"
        assert error.error_type == "RATE_LIMIT_ERROR"
        assert error.details == {}
        assert str(error) == "RATE_LIMIT_ERROR: Rate limit exceeded"

    def test_init_with_details(self):
        """Test initialization with details."""
        details = {"limit": 100, "reset_time": "2024-01-01T00:00:00Z"}
        error = RateLimitError(message="API rate limit reached", details=details)

        assert error.message == "API rate limit reached"
        assert error.error_type == "RATE_LIMIT_ERROR"
        assert error.details == details

    def test_inheritance(self):
        """Test that RateLimitError inherits from ScrapingError."""
        error = RateLimitError(message="Test")
        assert isinstance(error, ScrapingError)
        assert isinstance(error, Exception)


class TestValidationError:
    """Test ValidationError exception."""

    def test_init_without_details(self):
        """Test initialization without details."""
        error = ValidationError(message="Invalid data format")

        assert error.message == "Invalid data format"
        assert error.error_type == "VALIDATION_ERROR"
        assert error.details == {}
        assert str(error) == "VALIDATION_ERROR: Invalid data format"

    def test_init_with_details(self):
        """Test initialization with details."""
        details = {"field": "email", "value": "invalid-email"}
        error = ValidationError(message="Invalid email format", details=details)

        assert error.message == "Invalid email format"
        assert error.error_type == "VALIDATION_ERROR"
        assert error.details == details

    def test_inheritance(self):
        """Test that ValidationError inherits from ScrapingError."""
        error = ValidationError(message="Test")
        assert isinstance(error, ScrapingError)
        assert isinstance(error, Exception)


class TestExceptionUsage:
    """Test real-world usage scenarios of exceptions."""

    def test_raising_and_catching_scraping_error(self):
        """Test raising and catching ScrapingError."""
        with pytest.raises(ScrapingError) as exc_info:
            raise ScrapingError(message="Generic scraping failure", error_type="GENERIC_ERROR", details={"attempt": 1})

        error = exc_info.value
        assert error.message == "Generic scraping failure"
        assert error.error_type == "GENERIC_ERROR"
        assert error.details == {"attempt": 1}

    def test_raising_and_catching_specific_errors(self):
        """Test raising and catching specific error types."""
        # Test ExtractionError
        with pytest.raises(ExtractionError) as exc_info:
            raise ExtractionError("No jobs found", {"page": 1})

        assert exc_info.value.error_type == "EXTRACTION_ERROR"
        assert exc_info.value.message == "No jobs found"
        assert exc_info.value.details == {"page": 1}

        # Test NetworkError
        with pytest.raises(NetworkError) as exc_info:
            raise NetworkError("Timeout", {"timeout": 30})

        assert exc_info.value.error_type == "NETWORK_ERROR"
        assert exc_info.value.message == "Timeout"
        assert exc_info.value.details == {"timeout": 30}

        # Test RateLimitError
        with pytest.raises(RateLimitError) as exc_info:
            raise RateLimitError("Too many requests", {"wait": 60})

        assert exc_info.value.error_type == "RATE_LIMIT_ERROR"
        assert exc_info.value.message == "Too many requests"
        assert exc_info.value.details == {"wait": 60}

        # Test ValidationError
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Invalid URL", {"url": "not-a-url"})

        assert exc_info.value.error_type == "VALIDATION_ERROR"
        assert exc_info.value.message == "Invalid URL"
        assert exc_info.value.details == {"url": "not-a-url"}

    def test_exception_chaining(self):
        """Test exception chaining with original exception."""
        original_error = ValueError("Original error")

        try:
            raise original_error
        except ValueError as e:
            with pytest.raises(NetworkError) as exc_info:
                raise NetworkError("Network operation failed", {"original_error": str(e)}) from e

        error = exc_info.value
        assert error.message == "Network operation failed"
        assert error.details == {"original_error": "Original error"}
        assert error.__cause__ == original_error
