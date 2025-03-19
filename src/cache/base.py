from abc import ABC, abstractmethod
from typing import Any, Optional

class CacheConfig:
    """Configuration class for cache settings."""
    
    def __init__(
        self, 
        host: str = "localhost", 
        port: int = 6379,
        decode_responses: bool = True,
        **kwargs
    ):
        """
        Initialize cache configuration.
        
        Args:
            host (str): Cache server host.
            port (int): Cache server port.
            decode_responses (bool): Whether to decode responses.
            **kwargs: Additional configuration parameters.
        """
        self.host = host
        self.port = port
        self.decode_responses = decode_responses
        self.extra_params = kwargs

class BaseCacheManager(ABC):
    """Abstract base class for cache management."""
    
    def __init__(self, config: CacheConfig):
        """
        Initialize cache manager.
        
        Args:
            config (CacheConfig): Configuration for the cache.
        """
        self._config = config
        self._client = self._create_client()
    
    @abstractmethod
    def _create_client(self) -> Any:
        """
        Create and return a cache client.
        
        Returns:
            Cache client instance.
        """
        pass
    
    @abstractmethod
    def is_cached(self, key: str) -> bool:
        """
        Check if a key is cached.
        
        Args:
            key (str): Key to check.
        
        Returns:
            bool: True if key is cached, False otherwise.
        """
        pass
    
    @abstractmethod
    def cache(self, key: str, value: Optional[str] = None, **kwargs) -> None:
        """
        Cache a key-value pair.
        
        Args:
            key (str): Key to cache.
            value (Optional[str]): Value to cache.
            **kwargs: Additional caching parameters.
        """
        pass
    
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        """
        Retrieve a cached value.
        
        Args:
            key (str): Key to retrieve.
        
        Returns:
            Optional[str]: Cached value or None if not found.
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete a cached key.
        
        Args:
            key (str): Key to delete.
        """
        pass

    @abstractmethod
    def delete_all(self) -> int:
        """
        Delete all keys in the cache.
        
        Returns:
            int: Number of keys deleted.
        """
        pass
    