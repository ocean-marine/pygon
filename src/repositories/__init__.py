"""Data access and persistence layer functions package.

This package contains all data access logic, abstracting database operations,
file I/O, external API calls, and other persistence mechanisms from the
business logic layer.

Repository Responsibilities:
- Encapsulate all data access operations (CRUD)
- Handle database connections and transactions
- Manage data serialization/deserialization
- Provide consistent error handling for I/O failures
- Abstract storage implementation details from business logic

Repository Organization:
- storage.py: Database operations and persistence
- cache.py: Caching layer operations (Redis, in-memory)
- files.py: File system operations and document handling
- external.py: External API integrations and third-party services

Repository Function Patterns:
- Accept domain objects and primitive types as parameters
- Return Result types with data or error information
- Handle all I/O exceptions and convert to Pygon error patterns
- Use connection pooling and resource management
- Implement retry logic for transient failures

Example Repository Functions:
    def save_user_to_db(user: User) -> ErrorResult:
        try:
            # Database operation
            cursor.execute("INSERT INTO users...", user)
            return True, None
        except DatabaseError as e:
            return False, f"database_error: {e}"
    
    def load_user_by_id(user_id: int) -> UserResult:
        try:
            # Query operation
            row = cursor.fetchone("SELECT * FROM users WHERE id = ?", user_id)
            if not row:
                return None, "not_found_error: user not found"
            return User.from_row(row), None
        except DatabaseError as e:
            return None, f"database_error: {e}"

Data Access Principles:
- No business logic in repository functions
- Consistent error patterns for all I/O operations
- Clear separation between different storage mechanisms
- Easy testing through dependency injection

This separation supports large-scale development by isolating data access
concerns, enabling easy testing with mocks, and allowing storage technology
changes without affecting business logic.
"""