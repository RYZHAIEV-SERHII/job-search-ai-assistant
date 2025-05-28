"""Custom exceptions for job scraping operations."""

from typing import Optional


class ScrapingError(Exception):
    """Base exception for scraping operations."""

    def __init__(
        self,
        message: str,
        error_type: str,
        details: Optional[dict] = None,
    ) -> None:
        """Initialize scraping error.

        Args:
            message: Error description
            error_type: Type of error (e.g., EXTRACTION_ERROR, NETWORK_ERROR)
            details: Additional error context
        """
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the error."""
        return f"{self.error_type}: {self.message}"

    def to_dict(self) -> dict:
        """Convert error to dictionary format.

        Returns:
            Dictionary containing error details.
        """
        return {
            "error_type": self.error_type,
            "message": self.message,
            "details": self.details,
        }


class ExtractionError(ScrapingError):
    """Error during content extraction."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        """Initialize extraction error.

        Args:
            message: Error description
            details: Additional error context
        """
        super().__init__(
            message=message,
            error_type="EXTRACTION_ERROR",
            details=details,
        )


class NetworkError(ScrapingError):
    """Error during network operations."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        """Initialize network error.

        Args:
            message: Error description
            details: Additional error context
        """
        super().__init__(
            message=message,
            error_type="NETWORK_ERROR",
            details=details,
        )


class RateLimitError(ScrapingError):
    """Error when rate limit is exceeded."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        """Initialize rate limit error.

        Args:
            message: Error description
            details: Additional error context
        """
        super().__init__(
            message=message,
            error_type="RATE_LIMIT_ERROR",
            details=details,
        )


class ValidationError(ScrapingError):
    """Error during data validation."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        """Initialize validation error.

        Args:
            message: Error description
            details: Additional error context
        """
        super().__init__(
            message=message,
            error_type="VALIDATION_ERROR",
            details=details,
        )
