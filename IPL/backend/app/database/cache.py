"""Redis cache utilities"""

import redis
import json
from typing import Any, Optional
from app.config import get_settings
from app.logger import logger

settings = get_settings()


class RedisCache:
    """Redis caching utility"""

    def __init__(self):
        self.redis_client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True,
        )

    def set(self, key: str, value: Any, ex: int = None) -> bool:
        """Set a cache value"""
        try:
            json_value = json.dumps(value)
            self.redis_client.set(
                key, json_value, ex=ex or settings.redis_cache_expiry
            )
            logger.debug(f"Cache set: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache set failed for key {key}: {str(e)}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """Get a cache value"""
        try:
            value = self.redis_client.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                return json.loads(value)
            logger.debug(f"Cache miss: {key}")
            return None
        except Exception as e:
            logger.error(f"Cache get failed for key {key}: {str(e)}")
            return None

    def delete(self, key: str) -> bool:
        """Delete a cache entry"""
        try:
            self.redis_client.delete(key)
            logger.debug(f"Cache deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete failed for key {key}: {str(e)}")
            return False

    def clear(self) -> bool:
        """Clear all cache"""
        try:
            self.redis_client.flushdb()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Cache clear failed: {str(e)}")
            return False

    def health_check(self) -> bool:
        """Check Redis connection"""
        try:
            self.redis_client.ping()
            logger.info("Redis connection healthy")
            return True
        except Exception as e:
            logger.error(f"Redis connection failed: {str(e)}")
            return False


# Singleton instance
cache = RedisCache()
