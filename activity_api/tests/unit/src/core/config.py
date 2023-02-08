from pydantic import BaseSettings


class TestSettings(BaseSettings):
    test_mongo_url: str


settings = TestSettings()
