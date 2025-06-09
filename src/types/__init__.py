"""Centralized type definitions for consistent Pygon-style programming.

This package provides standardized type aliases and patterns that ensure
consistent error handling and return value conventions across the entire codebase.

Key Components:
- result_types.py: Core Result type definitions and error handling patterns

Exported Types:
- Result[T]: Generic result type for operations that may fail (T | None, str | None)
- ErrorResult: Boolean result with optional error message (bool, str | None)
- ValidationResult: Validation-specific result pattern (bool, str | None)
- MultipleErrorResult: For operations that collect multiple errors (bool, list[str])

Purpose:
These centralized types eliminate inconsistency in error handling patterns,
provide clear expectations for function return values, and make the codebase
more predictable for both human developers and AI tools.

Usage Example:
    from src.types import Result, ValidationResult
    
    def parse_data(raw: str) -> Result[dict]:
        # Implementation that returns (dict | None, str | None)
        pass
    
    def validate_input(value: str) -> ValidationResult:
        # Implementation that returns (bool, str | None)
        pass

This approach supports large-scale development by establishing clear contracts
between functions and making error conditions explicit and discoverable.
"""

from .result_types import Result, ErrorResult, ValidationResult, MultipleErrorResult

__all__ = [
    "Result",
    "ErrorResult", 
    "ValidationResult",
    "MultipleErrorResult",
]