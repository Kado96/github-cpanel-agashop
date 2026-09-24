class StorageError(Exception):
    """Base exception for storage errors."""
    pass


class QuotaExceededError(StorageError):
    """Raised when the storage quota is exceeded."""
    pass


class RateLimitError(StorageError):
    """Raised when the API rate limit is exceeded."""
    pass


class FileNotFoundStorageError(StorageError):
    """Raised when a requested file is not found in the storage."""
    pass


class AuthenticationStorageError(StorageError):
    """Raised when authentication with the storage provider fails."""
    pass
