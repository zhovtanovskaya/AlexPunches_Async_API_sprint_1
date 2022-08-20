from datetime import datetime

from postgres_to_es import DbConnect


class ElasticIndexStateError(Exception):
    ...


class ElasticIndexState(DbConnect):
    """Класс сохранения и получения состояния индексации Elastic's."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp_now = self._get_now()

    def _get_now(self):
        stmt = "SELECT NOW();"
        self.cursor.execute(stmt)
        now = self.cursor.fetchone()
        if now and len(now) > 0:
            return now[0]

    def get_last_time(self, entity: str):
        stmt = """
        SELECT timestamp FROM content.elastic_state
        WHERE namestamp = %s
        ;"""
        self.cursor.execute(stmt, ([entity]))
        timestamp = self.cursor.fetchone()
        if timestamp and len(timestamp) > 0:
            return timestamp[0]
        return datetime.fromtimestamp(0)

    def set_last_time(self, key: str) -> None:
        stmt = """
        INSERT INTO content.elastic_state (namestamp, timestamp)
            VALUES (%s, %s)
        ON CONFLICT (namestamp) DO UPDATE SET
            timestamp=EXCLUDED.timestamp
        ;"""
        self.cursor.execute(stmt, (key, self.timestamp_now))
        self.connection.commit()
