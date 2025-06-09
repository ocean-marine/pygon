"""Reusable Result type definitions for Pygon style programming.

This module provides standardized return value patterns that make error handling
explicit and consistent across the entire codebase.

Now includes rich error support for enhanced debugging capabilities.
"""

import traceback
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeAlias, TypeVar, Any

# Generic Result type for any value
T = TypeVar('T')


@dataclass(frozen=True)
class PygonError:
    """Rich error class providing detailed debugging information.
    
    Attributes:
        error_type: Type/category of the error (e.g., 'validation_error', 'not_found_error')
        message: Human-readable error message
        context: Additional context information about where/how the error occurred
        timestamp: When the error occurred (ISO format)
        source_location: File and line information where error was created
        metadata: Additional debugging information as key-value pairs
        cause: Optional underlying exception that caused this error
    """
    error_type: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    source_location: str = field(default="")
    metadata: dict[str, Any] = field(default_factory=dict)
    cause: Exception | None = field(default=None)
    
    def __post_init__(self):
        """Automatically capture source location if not provided."""
        if not self.source_location:
            # Get the calling frame (skip __post_init__ and __init__)
            frame = traceback.extract_stack()[-3]
            object.__setattr__(
                self, 
                'source_location', 
                f"{frame.filename}:{frame.lineno}"
            )
    
    def to_string(self) -> str:
        """Convert to simple string format for backward compatibility."""
        return f"{self.error_type}: {self.message}"
    
    def to_detailed_string(self) -> str:
        """Convert to detailed string format for debugging."""
        details = [
            f"Error: {self.error_type}",
            f"Message: {self.message}",
            f"Timestamp: {self.timestamp}",
            f"Source: {self.source_location}"
        ]
        
        if self.context:
            details.append(f"Context: {self.context}")
        
        if self.metadata:
            details.append(f"Metadata: {self.metadata}")
        
        if self.cause:
            details.append(f"Cause: {self.cause}")
        
        return " | ".join(details)
    
    def __str__(self) -> str:
        """Default string representation uses simple format."""
        return self.to_string()


# Result types with rich error support
Result: TypeAlias = tuple[T | None, PygonError | None]
ErrorResult: TypeAlias = tuple[bool, PygonError | None]
ValidationResult: TypeAlias = tuple[bool, PygonError | None]
MultipleErrorResult: TypeAlias = tuple[bool, list[PygonError]]

# Legacy string-based types for backward compatibility
LegacyResult: TypeAlias = tuple[T | None, str | None]
LegacyErrorResult: TypeAlias = tuple[bool, str | None]
LegacyValidationResult: TypeAlias = tuple[bool, str | None]
LegacyMultipleErrorResult: TypeAlias = tuple[bool, list[str]]


def create_validation_error(
    message: str, 
    context: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None
) -> PygonError:
    """Helper function to create validation errors.
    
    Args:
        message: Error message
        context: Additional context information
        metadata: Additional debugging metadata
        
    Returns:
        PygonError instance with validation_error type
    """
    return PygonError(
        error_type="validation_error",
        message=message,
        context=context or {},
        metadata=metadata or {}
    )


def create_not_found_error(
    message: str,
    context: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None
) -> PygonError:
    """Helper function to create not found errors.
    
    Args:
        message: Error message
        context: Additional context information
        metadata: Additional debugging metadata
        
    Returns:
        PygonError instance with not_found_error type
    """
    return PygonError(
        error_type="not_found_error",
        message=message,
        context=context or {},
        metadata=metadata or {}
    )


def create_io_error(
    message: str,
    cause: Exception | None = None,
    context: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None
) -> PygonError:
    """Helper function to create I/O errors.
    
    Args:
        message: Error message
        cause: Underlying exception that caused this error
        context: Additional context information
        metadata: Additional debugging metadata
        
    Returns:
        PygonError instance with io_error type
    """
    return PygonError(
        error_type="io_error",
        message=message,
        context=context or {},
        metadata=metadata or {},
        cause=cause
    )


def create_network_error(
    message: str,
    cause: Exception | None = None,
    context: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None
) -> PygonError:
    """Helper function to create network errors.
    
    Args:
        message: Error message
        cause: Underlying exception that caused this error
        context: Additional context information
        metadata: Additional debugging metadata
        
    Returns:
        PygonError instance with network_error type
    """
    return PygonError(
        error_type="network_error",
        message=message,
        context=context or {},
        metadata=metadata or {},
        cause=cause
    )


# Usage examples in docstring:
"""
Usage Examples:

```python
from src.types.result_types import (
    Result, ValidationResult, MultipleErrorResult,
    PygonError, create_validation_error, create_io_error
)
import json

# Rich error example
def parse_json(data: str, source_file: str = "unknown") -> Result[dict]:
    try:
        return json.loads(data), None
    except json.JSONDecodeError as e:
        error = create_io_error(
            message=f"Failed to parse JSON: {e}",
            cause=e,
            context={"source_file": source_file, "data_length": len(data)},
            metadata={"parser": "json.loads", "encoding": "utf-8"}
        )
        return None, error

# Single validation with rich error
def validate_email(email: str, field_name: str = "email") -> ValidationResult:
    if not email:
        error = create_validation_error(
            message="email is required",
            context={"field_name": field_name, "provided_value": email}
        )
        return False, error
    
    if "@" not in email:
        error = create_validation_error(
            message="invalid email format",
            context={"field_name": field_name, "provided_value": email},
            metadata={"expected_format": "user@domain.com", "validation_rule": "contains_at_symbol"}
        )
        return False, error
    
    return True, None

# Multiple validation with rich errors
def validate_form(data: dict, form_name: str = "form") -> MultipleErrorResult:
    errors = []
    
    if not data.get("name"):
        errors.append(create_validation_error(
            message="name is required",
            context={"form_name": form_name, "field_name": "name"},
            metadata={"provided_data_keys": list(data.keys())}
        ))
    
    if not data.get("email"):
        errors.append(create_validation_error(
            message="email is required",
            context={"form_name": form_name, "field_name": "email"},
            metadata={"provided_data_keys": list(data.keys())}
        ))
    
    return len(errors) == 0, errors

# Backward compatibility with simple string errors
def simple_validation(value: str) -> LegacyValidationResult:
    if not value:
        return False, "validation_error: value is required"
    return True, None

# Converting between rich and simple formats
def convert_to_simple_error(rich_error: PygonError) -> str:
    return rich_error.to_string()

def get_detailed_error_info(rich_error: PygonError) -> str:
    return rich_error.to_detailed_string()
```

The rich error system provides:
- **Automatic source location tracking**: Know exactly where errors originated
- **Contextual information**: Additional data about the error circumstances
- **Metadata for debugging**: Technical details to help with troubleshooting
- **Exception chaining**: Preserve underlying exceptions that caused the error
- **Timestamps**: Know when errors occurred
- **Backward compatibility**: Legacy string-based error patterns still supported
"""