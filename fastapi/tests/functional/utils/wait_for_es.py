import os
import sys
import time

from elasticsearch import Elasticsearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from functional.settings import test_settings

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=test_settings.es_url)

    while True:
        if es_client.ping():
            break
        time.sleep(1)
