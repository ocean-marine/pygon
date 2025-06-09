"""Input validation and data integrity functions package.

This package contains all validation logic organized by domain and validation type.
All validation functions follow Pygon patterns with explicit error reporting
and consistent return value conventions.

Validation Patterns:
- Single validation (ValidationResult): Fail-fast for general business logic
- Multiple validation (MultipleErrorResult): Collect all errors for user feedback
- Range validation: Numeric bounds, string length, date ranges
- Format validation: Email, phone, URL, identifier patterns
- Business rule validation: Domain-specific constraints

Typical Organization:
- common.py: Generic validation functions (range, length, format)
- domain.py: Business-specific validation rules
- forms.py: Form data validation with multiple error collection
- api.py: API input validation and sanitization

Validation Functions Always:
- Return ValidationResult or MultipleErrorResult types
- Include descriptive error messages with error_type prefix
- Handle edge cases explicitly (empty strings, None values)
- Are stateless and pure (no side effects)
- Can be easily composed and combined

Example Patterns:
    def validate_email(email: str) -> ValidationResult:
        if not email:
            return False, "validation_error: email is required"
        if "@" not in email:
            return False, "validation_error: invalid email format"
        return True, None
    
    def validate_registration_form(data: dict) -> MultipleErrorResult:
        errors = []
        # Collect all validation errors
        return len(errors) == 0, errors

This approach supports large-scale development by centralizing validation logic,
making validation rules discoverable, and ensuring consistent error reporting
across all input validation scenarios.
"""