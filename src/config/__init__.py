"""Application configuration and constants management package.

This package manages all application settings, environment-specific configurations,
and constant values in a centralized, type-safe manner following Pygon principles.

Configuration Organization:
- settings.py: Main application configuration using @dataclass
- constants.py: Immutable constant definitions and enums
- environments.py: Environment-specific configuration loading
- secrets.py: Secure credential management (never commit actual secrets)

Configuration Patterns:
- Use @dataclass(frozen=True) for configuration objects
- Environment variable loading with validation
- Type-safe configuration with comprehensive annotations
- Default values and validation for all settings
- Clear separation between different configuration concerns

Example Configuration Structure:
    @dataclass(frozen=True)
    class DatabaseConfig:
        host: str
        port: int
        database: str
        pool_size: int = 10
        timeout_seconds: int = 30
    
    @dataclass(frozen=True)
    class AppConfig:
        debug: bool
        database: DatabaseConfig
        api_key: str
        max_upload_size: int
    
    def load_config_from_env() -> Result[AppConfig]:
        # Load and validate environment variables
        # Return validated configuration or error
        pass

Configuration Loading Functions:
- Explicit error handling for missing or invalid configuration
- Environment variable validation and type conversion
- Support for different deployment environments
- Clear error messages for configuration problems

Constants Organization:
    class HttpStatus(Enum):
        OK = 200
        NOT_FOUND = 404
        SERVER_ERROR = 500
    
    DEFAULT_PAGE_SIZE = 20
    MAX_FILE_SIZE_MB = 100
    SUPPORTED_FILE_TYPES = frozenset(['.jpg', '.png', '.pdf'])

This centralized approach supports large-scale development by making
configuration explicit, preventing configuration drift between environments,
and ensuring all settings are validated and type-safe.
"""