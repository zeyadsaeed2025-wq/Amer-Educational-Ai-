"""
Redis cache manager for API responses.
"""
import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL")
USE_REDIS = bool(REDIS_URL)


class CacheManager:
    """Redis cache manager with fallback to no-cache."""
    
    def __init__(self):
        self._client = None
        
        if USE_REDIS:
            try:
                import redis
                self._client = redis.from_url(REDIS_URL, decode_responses=True)
                self._client.ping()
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.warning(f"Redis init error: {e}")
                self._client = None
    
    def get(self, key: str) -> Optional[dict]:
        """Get cached data."""
        if not self._client:
            return None
        
        try:
            data = self._client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None
    
    def set(self, key: str, data: dict, ttl: int = 3600):
        """Set cached data with TTL (default 1 hour)."""
        if not self._client:
            return
        
        try:
            self._client.setex(key, ttl, json.dumps(data))
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete cached data."""
        if not self._client:
            return
        
        try:
            self._client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def clear(self):
        """Clear all cache."""
        if not self._client:
            return
        
        try:
            self._client.flushdb()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


# Global cache manager
cache_manager = CacheManager()
