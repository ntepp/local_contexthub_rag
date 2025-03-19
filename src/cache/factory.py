from enum import Enum
from typing import Optional, Any

from .base import CacheConfig
from .redis_cache import RedisCacheManager, RedisCacheConfig

class CacheType(Enum):
    """Enum for cache types."""
    REDIS = "redis"
    # Add more cache types as needed

class CacheFactory:
    """Factory for creating cache managers."""
    
    @staticmethod
    def create_cache_manager(
        cache_type: CacheType = CacheType.REDIS,
        config: Optional[CacheConfig] = None
    ) -> Any:
        """
        Create a cache manager.
        
        Args:
            cache_type (CacheType): Type of cache.
            config (Optional[CacheConfig]): Configuration for cache.
        
        Returns:
            Cache manager instance.
        
        Raises:
            ValueError: If unsupported cache type is requested.
        """
        managers = {
            CacheType.REDIS: RedisCacheManager
        }
        
        manager_class = managers.get(cache_type)
        if not manager_class:
            raise ValueError(f"Unsupported cache type: {cache_type}")
        
        # Use default config if not provided
        if config is None:
            config = RedisCacheConfig()
        
        return manager_class(config)

# Convenience functions
def get_redis_client(
    host: Optional[str] = None, 
    port: Optional[int] = None,
    **kwargs
) -> Any:
    """
    Convenience function to get a Redis client.
    
    Args:
        host (Optional[str]): Redis host.
        port (Optional[int]): Redis port.
        **kwargs: Additional Redis configuration parameters.
    
    Returns:
        Redis client instance.
    """
    # Create configuration
    config = RedisCacheConfig(
        host=host, 
        port=port,
        **kwargs
    )
    
    # Create cache manager
    manager = CacheFactory.create_cache_manager(
        CacheType.REDIS,
        config
    )
    
    return manager._client

def is_url_cached(client, url: str) -> bool:
    """
    Check if a URL is cached.
    
    Args:
        client: Cache client.
        url (str): URL to check.
    
    Returns:
        bool: True if URL is cached, False otherwise.
    """
    return client.exists(url)

def cache_url(client, url: str, value: Optional[str] = None) -> None:
    """
    Cache a URL.
    
    Args:
        client: Cache client.
        url (str): URL to cache.
        value (Optional[str]): Value to cache.
    """
    client.set(url, value or "cached")