"""Interface definitions and protocol contracts package.

Defines abstract interfaces using typing.Protocol for loose coupling without inheritance.

Protocol types: Storage (data access), Validator (input validation), Processor (data transformation),
Notifier (notification mechanisms).

Benefits: behavioral contracts, dependency inversion, easy mocking, type safety, composition over inheritance.
All protocol methods return Result types for consistent Pygon error handling patterns.
"""