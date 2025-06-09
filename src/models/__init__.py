"""Immutable data structures and domain entities package.

This package contains all data structure definitions following Pygon principles:
immutable @dataclass objects with no methods, separating data from behavior.

Structure Guidelines:
- All dataclasses use frozen=True for immutability
- No methods in dataclasses - data only
- Clear field types with comprehensive annotations
- Enum classes for controlled vocabularies and status values
- Domain entity definitions (User, Product, Order, etc.)

Typical Contents:
- entities.py: Core business entities (User, Product, etc.)
- enums.py: Status values, categories, and controlled vocabularies
- value_objects.py: Small immutable objects representing concepts (Money, Address)
- errors.py: Error type definitions for domain-specific errors

Design Philosophy:
Data structures are pure data containers. All operations on these structures
are implemented as functions in other packages (services/, validators/, etc.).
This separation makes the code more testable, easier to reason about, and
better suited for functional programming patterns.

Example Structure:
    @dataclass(frozen=True)
    class User:
        id: int
        name: str
        email: str
        created_at: str
        # No methods - behavior is separate

Processing functions for these structures live in services/ or utils/ packages.

This approach supports large-scale development by making data flow explicit,
reducing coupling between data and behavior, and enabling easier testing
and modification of business logic.
"""