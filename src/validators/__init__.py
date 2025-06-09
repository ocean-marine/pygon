"""Input validation and data integrity functions package.

Validation logic organized by domain with explicit error reporting and consistent patterns.

Modules: common.py (generic validation), domain.py (business rules), forms.py (form data), 
api.py (API input).

Patterns: ValidationResult (fail-fast), MultipleErrorResult (collect errors), stateless pure functions,
descriptive error messages. Centralizes validation logic with consistent error reporting.
"""