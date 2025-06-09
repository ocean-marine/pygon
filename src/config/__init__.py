"""Application configuration and constants management package.

Centralizes all application settings using type-safe @dataclass(frozen=True) patterns.

Modules: settings.py (app config), constants.py (immutable values), environments.py (env loading), 
secrets.py (credential management).

Features: environment variable validation, type conversion, explicit error handling via Result types,
default values, clear separation of concerns. Prevents config drift between environments.
"""