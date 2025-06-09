"""Pygon project main package.

This is the root package of a Pygon-style Python project that emphasizes
explicit error handling, type safety, and human-AI collaborative development.

The src/ directory contains the core application modules organized by responsibility:

- types/: Centralized type definitions and Result patterns for consistent error handling
- models/: Immutable data structures using @dataclass with no methods
- validators/: Input validation functions with explicit error reporting
- services/: Business logic functions implementing core application functionality
- repositories/: Data access and persistence layer functions
- protocols/: Interface definitions using typing.Protocol for loose coupling
- config/: Application settings, constants, and configuration management
- utils/: Generic utility functions that don't belong to specific domains
- examples/: Reference implementations demonstrating proper Pygon patterns

All modules follow Pygon principles:
- Explicit error handling via return values (no exceptions for business logic)
- TypeAlias for clear, consistent return patterns
- Single-responsibility functions with clear, descriptive names
- Immutable data structures that separate data from behavior
- Comprehensive type annotations for better tooling and AI assistance

This structure supports large-scale development by making dependencies clear,
responsibilities explicit, and facilitating both human understanding and
AI-assisted development workflows.
"""