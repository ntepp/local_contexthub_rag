import os
import redis
from typing import Optional, Any

from .base import BaseCacheManager, CacheConfig

class RedisCacheConfig(CacheConfig):
    """Configuration specific to Redis cache."""
    
    def __init__(
        self, 
        host: Optional[str] = None, 
        port: Optional[int] = None,
        **kwargs
    ):
        """
        Initialize Redis cache configuration.
        
        Args:
            host (Optional[str]): Redis host.
            port (Optional[int]): Redis port.
            **kwargs: Additional Redis configuration parameters.
        """
        # Use environment variables if not provided
        host = host or os.getenv("REDIS_HOST", "localhost")
        port = port or int(os.getenv("REDIS_PORT", 6379))
        
        super().__init__(host=host, port=port, **kwargs)

class RedisCacheManager(BaseCacheManager):
    """Manager for Redis cache."""
    
    def _create_client(self) -> redis.Redis:
        """
        Create a Redis client.
        
        Returns:
            redis.Redis: Configured Redis client.
        """
        
        return redis.Redis(
            host=self._config.host,
            port=self._config.port,
            decode_responses=self._config.decode_responses,
            **self._config.extra_params
        )
    
    def is_cached(self, key: str) -> bool:
        """
        Check if a key is cached in Redis.
        
        Args:
            key (str): Key to check.
        
        Returns:
            bool: True if key exists, False otherwise.
        """
        self.delete_all(self)
        return bool(self._client.exists(key))
    
    def cache(
        self, 
        key: str, 
        value: Optional[str] = None, 
        **kwargs
    ) -> None:
        """
        Cache a key-value pair in Redis.
        
        Args:
            key (str): Key to cache.
            value (Optional[str]): Value to cache. Defaults to "cached".
            **kwargs: Additional Redis set parameters.
        """
        # Use "cached" as default value if not provided
        cache_value = value or "cached"
        
        # Set with additional parameters
        self._client.set(key, cache_value, **kwargs)
    
    def get(self, key: str) -> Optional[str]:
        """
        Retrieve a cached value from Redis.
        
        Args:
            key (str): Key to retrieve.
        
        Returns:
            Optional[str]: Cached value or None if not found.
        """
        return self._client.get(key)
    
    def delete(self, key: str) -> None:
        """
        Delete a cached key from Redis.
        
        Args:
            key (str): Key to delete.
        """
        self._client.delete(key)
    
    def delete_all(self) -> int:
            """
            Delete all keys in the Redis database.
            
            Returns:
                int: Number of keys deleted.
            """
            # Get all keys
            keys = self._client.keys('*')
            
            # Delete all keys if any exist
            if keys:
                return self._client.delete(*keys)
            
            return 0