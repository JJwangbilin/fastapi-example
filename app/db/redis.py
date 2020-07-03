import redis
from redis import Redis
from loguru import logger

from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWD


async def get_redis_database() -> Redis:
    rd = redis.Redis(connection_pool=redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT,
                                                          password=REDIS_PASSWD,
                                                          decode_responses=True))
    return rd
