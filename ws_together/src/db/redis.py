import redis.asyncio as ioredis

redis_db: ioredis.Redis | None = None


async def get_redis() -> ioredis.Redis:
    return redis_db
