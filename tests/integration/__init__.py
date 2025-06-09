"""Integration tests for component interactions and end-to-end workflows.

This package contains integration tests that verify how different components
work together and test complete workflows from input to output, including
interactions with external systems.

Integration Test Characteristics:
- Test multiple components working together
- May involve real external systems (test databases, APIs)
- Slower execution than unit tests but still reasonable
- Test realistic workflows and user scenarios
- Verify data flow between different layers

Test Organization:
- test_workflows/: Complete business process testing
- test_api/: API endpoint integration testing
- test_database/: Database integration and transaction testing
- test_external/: Third-party service integration testing

Integration Test Categories:

1. Workflow Tests:
   - User registration workflow (validation → service → repository)
   - Data processing pipelines (input → validation → processing → output)
   - Error propagation through multiple layers
   - Transaction rollback scenarios

2. API Integration Tests:
   - HTTP endpoint testing with real request/response cycles
   - Authentication and authorization workflows
   - Input validation and error response formatting
   - Content type handling and serialization

3. Database Integration Tests:
   - Repository functions with real database connections
   - Transaction boundaries and rollback behavior
   - Data consistency across multiple operations
   - Migration and schema validation

Example Integration Test:
    def test_user_registration_workflow(self):
        # Test complete workflow from API input to database storage
        request_data = {"email": "test@example.com", "name": "Test User"}
        
        # Call through service layer (validates → creates → stores)
        user, error = register_new_user(request_data["email"], request_data["name"])
        
        assert error is None, f"Registration failed: {error}"
        assert user.email == request_data["email"]
        
        # Verify data was actually stored
        stored_user, error = load_user_from_repository(user.id)
        assert error is None
        assert stored_user.email == user.email

Test Environment Setup:
- Use test databases (separate from development/production)
- Set up clean test data before each test
- Clean up test data after each test
- Use configuration that points to test systems

Performance Considerations:
- Keep integration tests focused and efficient
- Use database transactions for rollback where possible
- Minimize external API calls in tests
- Consider using docker containers for isolated test environments

Error Scenario Testing:
- Network failures and timeouts
- Database connection issues
- Invalid external API responses
- Partial failure scenarios

This integration testing approach ensures that components work correctly
together and that the complete system functions as expected in realistic
scenarios.
"""