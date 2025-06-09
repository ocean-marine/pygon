"""Example user service demonstrating Pygon style with both legacy and rich error handling."""

from dataclasses import dataclass
from src.types.result_types import (
    Result, ValidationResult, MultipleErrorResult,
    LegacyResult, LegacyValidationResult, LegacyMultipleErrorResult,
    PygonError, create_validation_error, create_not_found_error
)

# Domain-specific type aliases using rich errors
UserResult = Result[User]
UsersResult = Result[list[User]]

# Legacy type aliases for backward compatibility examples
LegacyUserResult = LegacyResult[User]

@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str

def validate_email(email: str, field_name: str = "email") -> ValidationResult:
    """Validate email format - single error pattern with rich errors.
    
    Args:
        email: Email address to validate.
        field_name: Name of the field being validated (for context).
        
    Returns:
        A tuple of (validation result, PygonError if any).
    """
    if not email:
        error = create_validation_error(
            message="email is required",
            context={
                "field_name": field_name,
                "provided_value": email,
                "validation_step": "required_check"
            },
            metadata={
                "validation_rule": "non_empty",
                "expected_type": "non-empty string"
            }
        )
        return False, error
        
    if "@" not in email:
        error = create_validation_error(
            message="invalid email format",
            context={
                "field_name": field_name,
                "provided_value": email,
                "validation_step": "format_check"
            },
            metadata={
                "validation_rule": "contains_at_symbol",
                "expected_format": "user@domain.com",
                "provided_length": len(email)
            }
        )
        return False, error
        
    return True, None

def validate_email_legacy(email: str) -> LegacyValidationResult:
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

def validate_user_data(name: str, email: str, form_context: str = "user_registration") -> MultipleErrorResult:
    """Validate user registration data - multiple error pattern with rich errors.
    
    Args:
        name: User name to validate.
        email: Email address to validate.
        form_context: Context of the form being validated.
        
    Returns:
        A tuple of (validation result, list of PygonErrors).
    """
    errors = []
    
    if not name.strip():
        errors.append(create_validation_error(
            message="name is required",
            context={
                "field_name": "name",
                "form_context": form_context,
                "provided_value": repr(name),
                "validation_step": "required_check"
            },
            metadata={
                "validation_rule": "non_empty_after_strip",
                "original_length": len(name),
                "stripped_length": len(name.strip())
            }
        ))
    
    if len(name) > 50:
        errors.append(create_validation_error(
            message="name must be 50 characters or less",
            context={
                "field_name": "name",
                "form_context": form_context,
                "provided_length": len(name),
                "validation_step": "length_check"
            },
            metadata={
                "validation_rule": "max_length",
                "max_allowed": 50,
                "actual_length": len(name)
            }
        ))
    
    if not email:
        errors.append(create_validation_error(
            message="email is required",
            context={
                "field_name": "email",
                "form_context": form_context,
                "provided_value": email,
                "validation_step": "required_check"
            },
            metadata={
                "validation_rule": "non_empty",
                "expected_type": "non-empty string"
            }
        ))
    elif "@" not in email:
        errors.append(create_validation_error(
            message="invalid email format",
            context={
                "field_name": "email",
                "form_context": form_context,
                "provided_value": email,
                "validation_step": "format_check"
            },
            metadata={
                "validation_rule": "contains_at_symbol",
                "expected_format": "user@domain.com",
                "provided_length": len(email)
            }
        ))
    
    return len(errors) == 0, errors

def validate_user_data_legacy(name: str, email: str) -> LegacyMultipleErrorResult:
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

def create_user(name: str, email: str, context: str = "api_registration") -> UserResult:
    """Create a new user with rich error validation.
    
    Args:
        name: User name.
        email: User email address.
        context: Context where user creation is happening.
        
    Returns:
        A tuple of (created user, PygonError if any).
    """
    # Validate inputs using multiple error pattern for better UX
    is_valid, validation_errors = validate_user_data(name, email, context)
    if not is_valid:
        # Convert multiple validation errors to single error for this context
        error_messages = [error.message for error in validation_errors]
        error = create_validation_error(
            message=f"User creation failed: {', '.join(error_messages)}",
            context={
                "operation": "create_user",
                "context": context,
                "provided_name": name,
                "provided_email": email,
                "validation_error_count": len(validation_errors)
            },
            metadata={
                "validation_errors": [err.to_string() for err in validation_errors],
                "operation_type": "user_creation"
            }
        )
        return None, error
    
    # Create user (in real implementation, this would save to database)
    user = User(
        id=1,  # In real app, this would be generated
        name=name.strip(),
        email=email.lower()
    )
    
    return user, None

def create_user_legacy(name: str, email: str) -> LegacyUserResult:
    """Legacy user creation function for backward compatibility.
    
    Args:
        name: User name.
        email: User email address.
        
    Returns:
        A tuple of (created user, error string if any).
    """
    # Validate inputs using legacy validation
    is_valid, errors = validate_user_data_legacy(name, email)
    if not is_valid:
        return None, f"validation_error: {', '.join(errors)}"
    
    # Create user (in real implementation, this would save to database)
    user = User(
        id=1,  # In real app, this would be generated
        name=name.strip(),
        email=email.lower()
    )
    
    return user, None

def find_user_by_email(users: list[User], email: str, search_context: str = "user_lookup") -> UserResult:
    """Find user by email address with rich error information.
    
    Args:
        users: List of User objects to search.
        email: Email address to search for.
        search_context: Context of the search operation.
        
    Returns:
        A tuple of (User object if found, PygonError if any).
    """
    # First validate the email format
    is_valid, validation_error = validate_email(email, "search_email")
    if validation_error:
        return None, validation_error
    
    # Search for user
    normalized_email = email.lower()
    for user in users:
        if user.email == normalized_email:
            return user, None
    
    # Create rich not found error
    error = create_not_found_error(
        message="user not found",
        context={
            "operation": "find_user_by_email",
            "search_context": search_context,
            "searched_email": email,
            "normalized_email": normalized_email,
            "total_users_searched": len(users)
        },
        metadata={
            "available_emails": [user.email for user in users],
            "search_method": "email_lookup",
            "case_sensitive": False
        }
    )
    
    return None, error

def find_user_by_email_legacy(users: list[User], email: str) -> LegacyUserResult:
    """Legacy user search function for backward compatibility.
    
    Args:
        users: List of User objects to search.
        email: Email address to search for.
        
    Returns:
        A tuple of (User object if found, error string if any).
    """
    # First validate the email format
    is_valid, validation_error = validate_email_legacy(email)
    if validation_error:
        return None, validation_error
    
    # Search for user
    normalized_email = email.lower()
    for user in users:
        if user.email == normalized_email:
            return user, None
    
    return None, "not_found_error: user not found"

# Demonstration of error handling patterns

def demonstrate_rich_vs_legacy_errors():
    """Example showing the difference between rich and legacy error handling."""
    
    # Test data
    invalid_email = "not-an-email"
    users = [
        User(1, "Alice", "alice@example.com"),
        User(2, "Bob", "bob@example.com")
    ]
    
    print("=== Rich Error Handling ===")
    
    # Rich error validation
    is_valid, rich_error = validate_email(invalid_email, "user_registration_email")
    if rich_error:
        print(f"Simple format: {rich_error.to_string()}")
        print(f"Detailed format: {rich_error.to_detailed_string()}")
    
    # Rich error user search
    user, search_error = find_user_by_email(users, "nonexistent@example.com", "admin_search")
    if search_error:
        print(f"Search error (simple): {search_error.to_string()}")
        print(f"Search error (detailed): {search_error.to_detailed_string()}")
    
    print("\n=== Legacy Error Handling ===")
    
    # Legacy error validation
    is_valid_legacy, legacy_error = validate_email_legacy(invalid_email)
    if legacy_error:
        print(f"Legacy error: {legacy_error}")
    
    # Legacy error user search
    user_legacy, search_error_legacy = find_user_by_email_legacy(users, "nonexistent@example.com")
    if search_error_legacy:
        print(f"Legacy search error: {search_error_legacy}")

if __name__ == "__main__":
    demonstrate_rich_vs_legacy_errors()