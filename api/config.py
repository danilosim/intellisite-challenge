from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_broker_url: str
    alerts_topic: str
    mongo_username: str
    mongo_password: str
    mongo_host: str
    mongo_port: int
    mongo_database: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()
