"""redis.py"""
import os
from typing import Tuple
from urllib.parse import urlparse

import redis

from fastapi_redis_cache.enums import RedisStatus


def redis_connect(host_url: str) -> Tuple[RedisStatus, redis.client.Redis]:
    """Attempt to connect to `host_url` and return a Redis client instance if successful."""
    return _connect(host_url) if os.environ.get("CACHE_ENV") != "TEST" else _connect_fake()


def _connect(host_url: str) -> Tuple[RedisStatus, redis.client.Redis]:  # pragma: no cover
    try:
        url = urlparse(host_url)
        redis_client = redis.Redis(
            host=url.hostname,
            port=url.port,
            username=url.username,
            password=url.password,
            ssl=True
        )
        if redis_client.ping():
            return (RedisStatus.CONNECTED, redis_client)
        return (RedisStatus.CONN_ERROR, None)
    except redis.AuthenticationError:
        return (RedisStatus.AUTH_ERROR, None)
    except redis.ConnectionError:
        return (RedisStatus.CONN_ERROR, None)


def _connect_fake() -> Tuple[RedisStatus, redis.client.Redis]:
    from fakeredis import FakeRedis

    return (RedisStatus.CONNECTED, FakeRedis())
