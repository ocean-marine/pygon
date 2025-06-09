"""Core business logic and application services package.

Implements primary business functionality by orchestrating validation, models, and repositories.

Organization: Domain-based modules (user.py, order.py) with single-responsibility functions.

Patterns: validate inputs → check business rules → coordinate operations → return Result types.
Separates concerns, enforces business invariants, handles transactions, enables isolated testing.
"""