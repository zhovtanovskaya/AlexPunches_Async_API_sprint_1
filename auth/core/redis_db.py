import redis
from core.config import config

redis_db = redis.Redis(
    host=config.redis_host,
    port=config.redis_port,
    db=1,
)
