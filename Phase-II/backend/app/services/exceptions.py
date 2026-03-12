"""
Custom Exceptions for LLM Service

Raised when LLM API calls fail or return invalid responses.
"""


class LLMParseError(Exception):
    """
    Raised when LLM response is not valid JSON.
    
    This happens when Claude returns malformed JSON that cannot be parsed.
    The calling service should catch this and return a 500 error.
    """
    
    def __init__(self, message: str, raw_response: str = None):
        self.message = message
        self.raw_response = raw_response
        super().__init__(self.message)


class LLMUnavailableError(Exception):
    """
    Raised when LLM API times out or is unavailable.
    
    This happens when:
    - Anthropic API times out (>15 seconds)
    - Anthropic API returns 5xx error
    - Rate limit exceeded (429)
    
    The calling router should catch this and return a 503 error
    with a graceful fallback message.
    """
    
    def __init__(self, message: str, retry_after: int = None):
        self.message = message
        self.retry_after = retry_after  # Seconds to wait before retry (if provided)
        super().__init__(self.message)
