"""Reference implementations and Pygon style examples package.

This package contains example code that demonstrates proper Pygon patterns
and serves as reference implementations for new team members and AI tools
learning the codebase conventions.

Example Categories:
- user_service.py: Complete user management example with validation
- api_patterns.py: Examples of API endpoint implementations
- data_processing.py: Data transformation and processing examples
- error_handling.py: Comprehensive error handling pattern examples
- testing_examples.py: Unit test patterns and best practices

Purpose of Examples:
- Onboard new developers quickly with concrete patterns
- Provide AI tools with reference implementations to learn from
- Document the "right way" to implement common functionality
- Serve as templates for new feature development
- Demonstrate integration between different Pygon packages

Example Content Structure:
Each example module includes:
- Complete, working implementations
- Comprehensive docstrings explaining design decisions
- Both success and error handling paths
- Integration with other Pygon packages (types, validators, etc.)
- Comments highlighting key Pygon principles

Key Demonstrated Patterns:
- Explicit error handling with Result types
- Data validation using validators/ package
- Immutable data structures from models/ package
- Service layer orchestration
- Repository integration for data access
- Type-safe function signatures with TypeAlias

Learning Progression:
1. Start with user_service.py for basic patterns
2. Review data_processing.py for complex operations
3. Study error_handling.py for edge case management
4. Examine testing_examples.py for test strategy

Maintenance Guidelines:
- Keep examples current with project standards
- Update when new patterns are established
- Ensure all examples compile and run correctly
- Review examples during code review for consistency

This package supports large-scale development by providing concrete reference
implementations that ensure consistency across the team and serve as learning
resources for both human developers and AI development tools.
"""