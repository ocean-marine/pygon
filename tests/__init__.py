"""Comprehensive test suite for Pygon-style application.

This package contains all tests organized to mirror the src/ package structure
and ensure comprehensive coverage of all application functionality following
Pygon testing principles.

Test Organization:
- unit/: Isolated unit tests for individual functions and modules
- integration/: Integration tests for component interactions
- fixtures/: Test data and shared test utilities
- conftest.py: pytest configuration and shared fixtures

Testing Structure:
tests/
├── unit/
│   ├── test_models/     # Tests for data structures and entities
│   ├── test_validators/ # Tests for validation logic
│   ├── test_services/   # Tests for business logic
│   ├── test_repositories/ # Tests for data access (with mocks)
│   ├── test_utils/      # Tests for utility functions
│   └── test_types/      # Tests for type definitions
├── integration/
│   ├── test_workflows/  # End-to-end workflow tests
│   └── test_api/        # API integration tests
└── fixtures/
    ├── sample_data.json # Test data files
    └── test_config.py   # Test configuration

Pygon Testing Principles:
- Test both success and error paths for every function
- Verify error message content, not just error occurrence
- Use explicit assertions over generic ones
- Mock external dependencies (databases, APIs)
- Test Result tuple patterns consistently

Example Test Patterns:
    def test_function_success_case(self):
        result, error = function_under_test(valid_input)
        assert error is None, f"Unexpected error: {error}"
        assert result == expected_value
    
    def test_function_error_case(self):
        result, error = function_under_test(invalid_input)
        assert result is None
        assert error is not None
        assert "expected_error_type" in error

Test Coverage Goals:
- 100% line coverage for all src/ modules
- All error conditions tested explicitly
- All validation rules verified
- All business logic paths covered
- Integration points verified with mocks

Running Tests:
- pytest: Run all tests
- pytest tests/unit/: Run only unit tests
- pytest tests/integration/: Run only integration tests
- pytest --cov=src: Run with coverage reporting

This comprehensive testing approach supports large-scale development by
ensuring reliability, preventing regressions, and providing confidence
for refactoring and feature additions.
"""