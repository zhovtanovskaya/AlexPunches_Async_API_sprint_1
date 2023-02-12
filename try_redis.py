from datetime import timedelta

import redis

jwt_redis_blocklist = redis.StrictRedis(
    host='localhost', port=6379, db=0, decode_responses=True,
)
jti = 'try_redis_jwt_id'
print('set', jwt_redis_blocklist.set(jti, '', ex=timedelta(seconds=30)))
