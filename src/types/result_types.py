"""Reusable Result type definitions for Pygon style programming.

This module provides standardized return value patterns that make error handling
explicit and consistent across the entire codebase.
"""

from typing import TypeAlias, TypeVar

# Generic Result type for any value
T = TypeVar('T')
Result: TypeAlias = tuple[T | None, str | None]

# Common specific result patterns
ErrorResult: TypeAlias = tuple[bool, str | None]
ValidationResult: TypeAlias = tuple[bool, str | None]
MultipleErrorResult: TypeAlias = tuple[bool, list[str]]

# Usage examples in docstring:
"""
Usage Examples:

```python
from src.types.result_types import Result, ValidationResult, MultipleErrorResult

# Generic Result type
def parse_json(data: str) -> Result[dict]:
    try:
        return json.loads(data), None
    except json.JSONDecodeError as e:
        return None, f"json_parse_error: {e}"

# Single validation (fail fast)
def validate_email(email: str) -> ValidationResult:
    if not email or "@" not in email:
        return False, "validation_error: invalid email format"
    return True, None

# Multiple validation (collect all errors)
def validate_form(data: dict) -> MultipleErrorResult:
    errors = []
    if not data.get("name"):
        errors.append("validation_error: name is required")
    if not data.get("email"):
        errors.append("validation_error: email is required")
    return len(errors) == 0, errors
```
"""