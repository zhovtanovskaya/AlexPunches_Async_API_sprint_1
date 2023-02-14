from typing import Generator

import more_itertools
from pymongo import MongoClient

from config import logger, settings
from utils.generator_fakes_guc import generate_user_content
from utils.timer import timed


@timed
def load_data(chunk_size: int, data: Generator):
    """Загрузить данные в Монгу."""
    db = MongoClient(
        settings.mongo_conn,
        serverSelectionTimeoutMS=5000,
        tlsCAFile=settings.mongo_tls_ca_file,
    )['sprint-9']
    collection = db['reactions']
    chunks = 0
    for documents in more_itertools.ichunked(data, chunk_size):
        collection.insert_many(
            [
                document.dict(exclude_none=True, by_alias=True)
                for document in documents
            ]
        )
        chunks += 1
        logger.info(f'chunk #{chunks}', )


def run(users_count: int, films_count: int, chunk_size: int) -> None:
    """Запуск."""
    load_data(chunk_size, generate_user_content(users_count, films_count))
