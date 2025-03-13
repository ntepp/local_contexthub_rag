import redis
import os

def get_redis_client():
    """Returns a Redis client."""
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

def is_url_cached(client, url):
    """Checks if a URL is cached."""
    return client.exists(url)

def cache_url(client, url):
    """Caches a URL."""
    client.set(url, "cached")
