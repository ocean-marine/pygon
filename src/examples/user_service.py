"""Example user service demonstrating Pygon style with result library error handling."""

from dataclasses import dataclass
from result import Result, Ok, Err
from src.types.result_types import ValidationResult, MultipleErrorResult

# Domain-specific type aliases using result library
UserResult = Result[User, str]
UsersResult = Result[list[User], str]
MultipleErrorsResult = Result[bool, list[str]]

@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str

def validate_email(email: str) -> Result[bool, str]:
    """Validate email format using result library.
    
    Args:
        email: Email address to validate.
        
    Returns:
        Result containing validation success or error message.
    """
    if not email:
        return Err("validation_error: email is required")
        
    if "@" not in email:
        return Err("validation_error: invalid email format")
        
    return Ok(True)

def validate_email_legacy(email: str) -> ValidationResult:
    """Legacy validation function for backward compatibility.
    
    Args:
        email: Email address to validate.
        
    Returns:
        A tuple of (validation result, error string if any).
    """
    if not email:
        return False, "validation_error: email is required"
    if "@" not in email:
        return False, "validation_error: invalid email format"
    return True, None

def validate_user_data(name: str, email: str) -> Result[bool, list[str]]:
    """Validate user registration data using result library.
    
    Args:
        name: User name to validate.
        email: Email address to validate.
        
    Returns:
        Result containing validation success or list of error messages.
    """
    errors = []
    
    if not name.strip():
        errors.append("validation_error: name is required")
    
    if len(name) > 50:
        errors.append("validation_error: name must be 50 characters or less")
    
    if not email:
        errors.append("validation_error: email is required")
    elif "@" not in email:
        errors.append("validation_error: invalid email format")
    
    if errors:
        return Err(errors)
    return Ok(True)

def validate_user_data_legacy(name: str, email: str) -> MultipleErrorResult:
    """Legacy validation function for backward compatibility.
    
    Args:
        name: User name to validate.
        email: Email address to validate.
        
    Returns:
        A tuple of (validation result, list of error strings).
    """
    errors = []
    
    if not name.strip():
        errors.append("validation_error: name is required")
    
    if len(name) > 50:
        errors.append("validation_error: name must be 50 characters or less")
    
    if not email:
        errors.append("validation_error: email is required")
    elif "@" not in email:
        errors.append("validation_error: invalid email format")
    
    return len(errors) == 0, errors

def create_user(name: str, email: str) -> UserResult:
    """Create a new user with result library validation.
    
    Args:
        name: User name.
        email: User email address.
        
    Returns:
        Result containing created user or error message.
    """
    # Validate inputs using result library pattern
    validation_result = validate_user_data(name, email)
    
    if validation_result.is_err():
        error_messages = validation_result.unwrap_err()
        error_msg = f"User creation failed: {', '.join(error_messages)}"
        return Err(error_msg)
    
    # Create user (in real implementation, this would save to database)
    user = User(
        id=1,  # In real app, this would be generated
        name=name.strip(),
        email=email.lower()
    )
    
    return Ok(user)

def find_user_by_email(users: list[User], email: str) -> UserResult:
    """Find user by email address using result library.
    
    Args:
        users: List of User objects to search.
        email: Email address to search for.
        
    Returns:
        Result containing User object if found or error message.
    """
    # First validate the email format
    email_validation = validate_email(email)
    if email_validation.is_err():
        return Err(email_validation.unwrap_err())
    
    # Search for user
    normalized_email = email.lower()
    for user in users:
        if user.email == normalized_email:
            return Ok(user)
    
    return Err("not_found_error: user not found")

def create_multiple_users(user_data_list: list[dict]) -> Result[list[User], str]:
    """Create multiple users with comprehensive error handling.
    
    Args:
        user_data_list: List of dictionaries containing user data.
        
    Returns:
        Result containing list of created users or error message.
    """
    users = []
    
    for i, user_data in enumerate(user_data_list):
        name = user_data.get("name", "")
        email = user_data.get("email", "")
        
        user_result = create_user(name, email)
        if user_result.is_err():
            return Err(f"Failed to create user at index {i}: {user_result.unwrap_err()}")
        
        users.append(user_result.unwrap())
    
    return Ok(users)

def process_user_registration(form_data: dict) -> Result[User, str]:
    """Process user registration with chained validation using result library.
    
    Args:
        form_data: Dictionary containing registration form data.
        
    Returns:
        Result containing created user or error message.
    """
    name = form_data.get("name", "")
    email = form_data.get("email", "")
    
    # Chain validation and user creation
    return (
        validate_email(email)
        .and_then(lambda _: validate_user_data(name, email))
        .and_then(lambda _: create_user(name, email))
    )

# Demonstration of error handling patterns

def demonstrate_result_library_usage():
    """Example showing result library error handling patterns."""
    
    # Test data
    invalid_email = "not-an-email"
    users = [
        User(1, "Alice", "alice@example.com"),
        User(2, "Bob", "bob@example.com")
    ]
    
    print("=== Result Library Error Handling ===")
    
    # Email validation
    email_result = validate_email(invalid_email)
    match email_result:
        case Ok(_):
            print("Email is valid")
        case Err(error):
            print(f"Email validation error: {error}")
    
    # User search
    search_result = find_user_by_email(users, "nonexistent@example.com")
    if search_result.is_err():
        print(f"User search error: {search_result.unwrap_err()}")
    
    # User creation with chaining
    registration_data = {"name": "", "email": invalid_email}
    registration_result = process_user_registration(registration_data)
    if registration_result.is_err():
        print(f"Registration error: {registration_result.unwrap_err()}")
    
    # Multiple user creation
    user_data_list = [
        {"name": "Charlie", "email": "charlie@example.com"},
        {"name": "", "email": "invalid-email"},  # This will cause failure
        {"name": "David", "email": "david@example.com"}
    ]
    
    multiple_users_result = create_multiple_users(user_data_list)
    if multiple_users_result.is_err():
        print(f"Multiple users creation error: {multiple_users_result.unwrap_err()}")
    else:
        users_created = multiple_users_result.unwrap()
        print(f"Successfully created {len(users_created)} users")

def demonstrate_legacy_compatibility():
    """Example showing legacy tuple-based error handling for compatibility."""
    
    print("\n=== Legacy Tuple-based Error Handling ===")
    
    # Legacy validation
    is_valid, error = validate_email_legacy("invalid-email")
    if not is_valid:
        print(f"Legacy validation error: {error}")
    
    # Legacy multiple validation
    is_valid_multi, errors = validate_user_data_legacy("", "invalid-email")
    if not is_valid_multi:
        print(f"Legacy multiple validation errors: {errors}")

if __name__ == "__main__":
    demonstrate_result_library_usage()
    demonstrate_legacy_compatibility()