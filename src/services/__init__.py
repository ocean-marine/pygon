"""Core business logic and application services package.

This package contains the primary business logic functions that implement
the application's core functionality. Services orchestrate data validation,
business rule enforcement, and coordinate with repositories for data persistence.

Service Layer Responsibilities:
- Implement complex business workflows and use cases
- Coordinate between validators, models, and repositories
- Enforce business rules and invariants
- Handle transaction boundaries and data consistency
- Transform data between external and internal representations

Service Organization:
- Domain-based modules (user.py, order.py, payment.py)
- Each module contains related business operations
- Functions follow single-responsibility principle
- Clear dependency management through function parameters

Service Function Patterns:
- Accept primitive types and domain objects as parameters
- Validate inputs using validators/ functions
- Orchestrate business logic with explicit error handling
- Use repositories/ for data access operations
- Return Result types with success data or error messages

Example Service Structure:
    def create_user_account(email: str, name: str) -> UserResult:
        # 1. Validate inputs
        is_valid, errors = validate_user_registration_data(email, name)
        if not is_valid:
            return None, f"validation_error: {', '.join(errors)}"
        
        # 2. Check business rules
        exists, err = check_user_email_exists(email)
        if err:
            return None, err
        if exists:
            return None, "business_error: email already registered"
        
        # 3. Create and persist
        user = User(id=generate_id(), email=email, name=name)
        success, err = save_user_to_repository(user)
        if err:
            return None, err
        
        return user, None

This layered approach supports large-scale development by separating concerns,
making business logic testable in isolation, and providing clear boundaries
between different aspects of the application.
"""