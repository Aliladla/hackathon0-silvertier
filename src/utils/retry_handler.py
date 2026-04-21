"""
Retry handler with exponential backoff for Personal AI Employee.

Provides retry logic for API calls with rate limit handling.
"""

import time
import logging
from typing import Callable, Any, Optional
from functools import wraps


class RetryHandler:
    """Handles retries with exponential backoff."""

    def __init__(self, max_retries: int = 5, base_delay: float = 1.0, max_delay: float = 60.0):
        """
        Initialize retry handler.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds (doubles each retry)
            max_delay: Maximum delay in seconds
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.logger = logging.getLogger(__name__)

    def retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with retry logic.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If all retries exhausted
        """
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                # Check if this is a rate limit error
                is_rate_limit = self._is_rate_limit_error(e)

                if attempt < self.max_retries - 1:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)

                    if is_rate_limit:
                        self.logger.warning(
                            f"Rate limit hit on attempt {attempt + 1}/{self.max_retries}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                    else:
                        self.logger.warning(
                            f"Error on attempt {attempt + 1}/{self.max_retries}: {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )

                    time.sleep(delay)
                else:
                    self.logger.error(
                        f"All {self.max_retries} retry attempts exhausted. Last error: {e}"
                    )

        # All retries exhausted
        raise last_exception

    def _is_rate_limit_error(self, exception: Exception) -> bool:
        """
        Check if exception is a rate limit error.

        Args:
            exception: Exception to check

        Returns:
            True if rate limit error, False otherwise
        """
        # Check for common rate limit indicators
        error_str = str(exception).lower()

        # HTTP 429 Too Many Requests
        if '429' in error_str:
            return True

        # Common rate limit messages
        rate_limit_keywords = [
            'rate limit',
            'too many requests',
            'quota exceeded',
            'throttled'
        ]

        return any(keyword in error_str for keyword in rate_limit_keywords)


def with_retry(max_retries: int = 5, base_delay: float = 1.0, max_delay: float = 60.0):
    """
    Decorator for automatic retry with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = RetryHandler(max_retries, base_delay, max_delay)
            return handler.retry(func, *args, **kwargs)
        return wrapper
    return decorator


# Convenience function for one-off retries
def retry_on_error(func: Callable, *args, max_retries: int = 5, **kwargs) -> Any:
    """
    Execute function with retry logic (convenience function).

    Args:
        func: Function to execute
        *args: Function arguments
        max_retries: Maximum retry attempts
        **kwargs: Function keyword arguments

    Returns:
        Function result
    """
    handler = RetryHandler(max_retries=max_retries)
    return handler.retry(func, *args, **kwargs)
