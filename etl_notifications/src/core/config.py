from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    topic = 'my_topic'
    bootstrap_servers = 'localhost:9092'
    group_id = "my-group"
