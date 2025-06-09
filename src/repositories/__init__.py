"""Data access and persistence layer functions package.

Abstracts database operations, file I/O, and external APIs from business logic.

Modules: storage.py (database), cache.py (caching), files.py (file system), external.py (APIs).

Responsibilities: CRUD operations, connection management, serialization, consistent error handling,
transaction management. All functions return Result types and convert I/O exceptions to Pygon patterns.
"""