import os
import sys

from elasticsearch import Elasticsearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from functional.settings import logger, test_settings
from functional.utils.backoff import backoff


class ElasticPingError(Exception):
    ...


@backoff(ElasticPingError, logger=logger)
def ping_elastic(es_client):
    if not es_client.ping():
        raise ElasticPingError()


if __name__ == '__main__':
    _es_client = Elasticsearch(hosts=test_settings.es_url)

    ping_elastic(es_client=_es_client)
