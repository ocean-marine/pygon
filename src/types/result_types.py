"""Reusable Result type definitions for Pygon style programming.

This module provides standardized return value patterns that make error handling
explicit and consistent across the entire codebase.

Error handling is consolidated to use the result library for robust Result patterns.
"""

from typing import TypeAlias, TypeVar

# Generic Result type for any value
T = TypeVar('T')

# Basic tuple-based types for simple error handling
Result: TypeAlias = tuple[T | None, str | None]
ValidationResult: TypeAlias = tuple[bool, str | None]
MultipleErrorResult: TypeAlias = tuple[bool, list[str]]

# Usage examples in docstring:
"""
Usage Examples:

```python
from src.types.result_types import Result, ValidationResult, MultipleErrorResult
from result import Result as ResultLib, Ok, Err

# Basic tuple-based Result for simple cases
UserResult = Result[User]  # Domain-specific type alias

def find_user_by_email(users: list[User], email: str) -> UserResult:
    for user in users:
        if user.email == email:
            return user, None
    return None, "user not found"

# Single validation with simple error
def validate_email_format(email: str) -> ValidationResult:
    if not email:
        return False, "validation_error: email is required"
    if "@" not in email:
        return False, "validation_error: invalid email format"
    return True, None

# Multiple validation for UX
def validate_user_registration(form_data: dict) -> MultipleErrorResult:
    errors = []
    if not form_data.get("name", "").strip():
        errors.append("validation_error: name is required")
    if "@" not in form_data.get("email", ""):
        errors.append("validation_error: invalid email format")
    return len(errors) == 0, errors

# For more advanced error handling, use the result library directly:
def parse_json_with_result(data: str) -> ResultLib[dict, str]:
    try:
        import json
        return Ok(json.loads(data))
    except json.JSONDecodeError as e:
        return Err(f"json_parse_error: {e}")

def validate_email_with_result(email: str) -> ResultLib[bool, str]:
    if not email:
        return Err("validation_error: email is required")
    if "@" not in email:
        return Err("validation_error: invalid email format")
    return Ok(True)
```

The type system provides:
- **Simple tuple-based patterns**: For basic error handling and legacy compatibility
- **Result library integration**: For advanced functional programming patterns
- **Consistent error messaging**: Standardized error type prefixes
"""