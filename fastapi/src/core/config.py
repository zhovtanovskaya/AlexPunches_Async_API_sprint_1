import logging
import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ApiSettings(BaseSettings):
    project_name: str = Field('movies', env='project_name')
    redis_host: str = Field('127.0.0.1', env='redis_host')
    redis_port: str = Field('6379', env='redis_port')
    elastic_host: str = Field('127.0.0.1', env='es_host')
    elastic_port: str = Field('9200', env='es_port')
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    redis_cache_expire_in_seconds: int = 60 * 5
    use_cache: bool = Field(True, env='use_cache')


config = ApiSettings()
logger = logging.getLogger(config.project_name)
