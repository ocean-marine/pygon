"""Centralized type definitions for consistent Pygon-style programming.

Provides standardized Result type aliases ensuring consistent error handling across the codebase.

Exported types: Result[T] (generic operations), ErrorResult (boolean + error), ValidationResult (validation), 
MultipleErrorResult (multiple errors).

Makes error conditions explicit, eliminates inconsistency, provides clear function contracts.
"""

from src.types.result_types import Result, ErrorResult, ValidationResult, MultipleErrorResult

__all__ = [
    "Result",
    "ErrorResult", 
    "ValidationResult",
    "MultipleErrorResult",
]