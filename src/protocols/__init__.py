"""Interface definitions and protocol contracts package.

This package defines abstract interfaces using Python's typing.Protocol
to establish contracts between different layers and components without
creating tight coupling through inheritance.

Protocol Purpose:
- Define behavioral contracts without implementation inheritance
- Enable loose coupling between components
- Support dependency inversion and testability
- Provide clear documentation of expected behaviors
- Enable duck typing with type safety

Common Protocol Categories:
- Storage protocols: Define how data access should behave
- Validator protocols: Standardize validation interfaces
- Processor protocols: Define data transformation contracts
- Notifier protocols: Abstract notification mechanisms

Example Protocol Definitions:
    class Storable(Protocol):
        def save(self, data: dict) -> ErrorResult: ...
        def load(self, id: str) -> Result[dict]: ...
    
    class Validatable(Protocol):
        def validate(self, data: Any) -> ValidationResult: ...
    
    class Processable(Protocol):
        def process(self, input_data: Any) -> Result[Any]: ...

Usage Benefits:
- Functions can accept protocol types instead of concrete classes
- Easy to create test doubles and mocks
- Clear documentation of what behaviors are required
- Type checking ensures protocol compliance
- Supports both structural and nominal typing

Integration with Pygon:
- All protocol methods return Result types for consistent error handling
- Protocols define the minimal interface needed for functionality
- Implementation classes can be simple, focused on single responsibilities
- Enables composition over inheritance patterns

This approach supports large-scale development by establishing clear contracts,
reducing coupling between components, and making the system more modular
and testable.
"""