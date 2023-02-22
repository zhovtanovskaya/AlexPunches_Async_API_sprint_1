from ipaddress import IPv4Address

from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    notifications_topic: str
    event_store_host: IPv4Address | str
    event_store_port: int = 9092
    notifications_group_id: str

    @property
    def bootstrap_servers(self):
        return f'{self.event_store_host}:{self.event_store_port}'


class Settings(BaseSettings):
    kafka = KafkaSettings()


settings = Settings()
