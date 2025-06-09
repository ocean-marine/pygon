"""Isolated unit tests for individual functions and modules.

This package contains unit tests that test individual functions in isolation,
mocking all external dependencies to ensure tests are fast, reliable, and
focused on single units of functionality.

Unit Test Characteristics:
- Test single functions or methods in isolation
- Mock all external dependencies (databases, APIs, file systems)
- Fast execution (entire unit test suite should run in seconds)
- Deterministic results (no flaky tests due to external factors)
- Clear, descriptive test names that document expected behavior

Test Organization by Module:
- test_models/: Tests for data structures, validation of dataclass constraints
- test_validators/: Tests for all validation functions with edge cases
- test_services/: Tests for business logic with mocked dependencies
- test_repositories/: Tests for data access logic with mocked I/O
- test_utils/: Tests for utility functions with comprehensive coverage
- test_types/: Tests for type definitions and Result pattern usage

Pygon Unit Testing Patterns:
Every function test should cover:
1. Happy path with valid inputs
2. Error cases with invalid inputs
3. Edge cases (empty strings, None values, boundary conditions)
4. Error message content verification

Example Unit Test Structure:
    class TestUserValidation:
        def test_validate_email_with_valid_email_returns_success(self):
            result, error = validate_email("user@example.com")
            assert error is None
            assert result is True
        
        def test_validate_email_with_empty_email_returns_error(self):
            result, error = validate_email("")
            assert result is False
            assert error == "validation_error: email is required"
        
        def test_validate_email_with_invalid_format_returns_error(self):
            result, error = validate_email("invalid-email")
            assert result is False
            assert "validation_error" in error

Mocking Guidelines:
- Mock all external systems (databases, APIs, file systems)
- Use pytest fixtures for common mock setups
- Verify mock calls to ensure correct integration
- Keep mocks simple and focused on the test scenario

Test Data Management:
- Use fixtures for reusable test data
- Create factory functions for complex objects
- Keep test data minimal and focused on the test case
- Use descriptive variable names for test data

This unit testing approach ensures individual components work correctly
in isolation and provides fast feedback during development.
"""