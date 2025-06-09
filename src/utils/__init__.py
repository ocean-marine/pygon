"""Generic utility functions and helper modules package.

This package contains reusable utility functions that don't belong to any
specific domain but are used across multiple parts of the application.
All utilities follow Pygon principles with explicit error handling.

Utility Categories:
- helpers.py: Generic helper functions for common operations
- formatters.py: Data formatting and presentation utilities
- converters.py: Type conversion and data transformation functions
- decorators.py: Function decorators and higher-order functions
- datetime_utils.py: Date and time manipulation utilities

Utility Function Principles:
- Pure functions with no side effects
- Explicit error handling with Result types
- Comprehensive type annotations
- Clear, descriptive function names
- Single responsibility per function
- Easy to test in isolation

Example Utility Functions:
    def safe_parse_int(value: str) -> Result[int]:
        \"\"\"Parse string to integer with explicit error handling.\"\"\"
        try:
            return int(value), None
        except ValueError:
            return None, f"parse_error: invalid integer format: {value}"
    
    def format_currency(amount: float, currency: str) -> Result[str]:
        \"\"\"Format amount as currency string.\"\"\"
        if amount < 0:
            return None, "format_error: amount cannot be negative"
        try:
            formatted = f"{amount:.2f} {currency}"
            return formatted, None
        except Exception as e:
            return None, f"format_error: {e}"
    
    def safe_divide(a: float, b: float) -> Result[float]:
        \"\"\"Perform division with zero-division protection.\"\"\"
        if b == 0:
            return None, "math_error: division by zero"
        return a / b, None

Common Utility Patterns:
- String manipulation with validation
- Mathematical operations with bounds checking
- Collection operations with empty handling
- File path manipulation with existence checking
- Date/time operations with timezone awareness

Testing Strategy:
All utility functions should have comprehensive unit tests covering:
- Happy path scenarios
- Edge cases and boundary conditions
- Error conditions and invalid inputs
- Type checking and validation

This collection supports large-scale development by providing reliable,
well-tested building blocks that reduce code duplication and establish
consistent patterns for common operations.
"""