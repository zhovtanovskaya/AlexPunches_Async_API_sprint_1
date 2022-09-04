import os
import sys
import time

from redis import Redis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from functional.settings import test_settings

if __name__ == '__main__':
    redis_client = Redis(test_settings.redis_url)

    while True:
        if redis_client.ping():
            redis_client.close()
            break
        time.sleep(1)
