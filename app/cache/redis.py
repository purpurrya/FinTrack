import json
import logging
from typing import Any

from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.config import settings

logger = logging.getLogger(__name__)


class RedisCacheBackend:
    def __init__(self, redis_url: str) -> None:
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Any | None:
        try:
            value = await self.redis.get(key)
        except RedisError:
            logger.warning(
                "Redis is unavailable, no cache for key %s", key, exc_info=True
            )
            return None
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        try:
            await self.redis.set(key, json.dumps(value), ex=ttl_seconds)
        except RedisError:
            logger.warning(
                "Redis is unavailable, cannot set key %s", key, exc_info=True
            )

    async def delete(self, key: str) -> None:
        try:
            await self.redis.delete(key)
        except RedisError:
            logger.warning(
                "Redis is unavailable, cannot delete key %s", key, exc_info=True
            )


cache = RedisCacheBackend(settings.redis_url)
