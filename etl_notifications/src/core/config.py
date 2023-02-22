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


class RabbitMQSettings(BaseSettings):
    notifications_queue_user: str
    notifications_queue_password: str
    notifications_queue_host: str = '51.250.2.205'
    notifications_queue_port: str = '5672'
    queue_name: str = 'notifications'
    exchanger_name: str = 'notifications_exchanger'
    mq_timeout: int = 10
    queue_prefetch_count: int = 1
    max_priority: int = 10

    def get_conn_str(self) -> str:
        return str(
            f'amqp://{self.notifications_queue_user}'
            f':{self.notifications_queue_password}@'
            f'{self.notifications_queue_host}:{self.notifications_queue_port}/'
        )


class Settings(BaseSettings):
    kafka = KafkaSettings()
    rabbitmq = RabbitMQSettings()


settings = Settings()
