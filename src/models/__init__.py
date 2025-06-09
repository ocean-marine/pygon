"""Immutable data structures and domain entities package.

Contains @dataclass(frozen=True) objects with no methods, separating data from behavior.

Modules: entities.py (core business entities), enums.py (status values), value_objects.py (concepts like Money),
errors.py (domain error types).

Design: Pure data containers with all operations implemented as functions in other packages.
Supports explicit data flow, reduced coupling, easier testing and functional programming patterns.
"""