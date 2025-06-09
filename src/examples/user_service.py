"""Example user service demonstrating Pygon style with centralized Result types."""

from dataclasses import dataclass
from src.types.result_types import Result, ValidationResult, MultipleErrorResult

# Domain-specific type aliases using centralized Result
UserResult = Result[User]
UsersResult = Result[list[User]]

@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str

def validate_email(email: str) -> ValidationResult:
    """Validate email format - single error pattern.
    
    Args:
        email: Email address to validate.
        
    Returns:
        A tuple of (validation result, error message if any).
    """
    if not email:
        return False, "validation_error: email is required"
    if "@" not in email:
        return False, "validation_error: invalid email format"
    return True, None

def validate_user_data(name: str, email: str) -> MultipleErrorResult:
    """Validate user registration data - multiple error pattern.
    
    Args:
        name: User name to validate.
        email: Email address to validate.
        
    Returns:
        A tuple of (validation result, list of error messages).
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
    """Create a new user with validation.
    
    Args:
        name: User name.
        email: User email address.
        
    Returns:
        A tuple of (created user, error message if any).
    """
    # Validate inputs using multiple error pattern for better UX
    is_valid, errors = validate_user_data(name, email)
    if not is_valid:
        # Convert multiple errors to single error for this context
        return None, f"validation_error: {', '.join(errors)}"
    
    # Create user (in real implementation, this would save to database)
    user = User(
        id=1,  # In real app, this would be generated
        name=name.strip(),
        email=email.lower()
    )
    
    return user, None

def find_user_by_email(users: list[User], email: str) -> UserResult:
    """Find user by email address.
    
    Args:
        users: List of User objects to search.
        email: Email address to search for.
        
    Returns:
        A tuple of (User object if found, error message if any).
    """
    # First validate the email format
    is_valid, validation_error = validate_email(email)
    if validation_error:
        return None, validation_error
    
    # Search for user
    normalized_email = email.lower()
    for user in users:
        if user.email == normalized_email:
            return user, None
    
    return None, "not_found_error: user not found"