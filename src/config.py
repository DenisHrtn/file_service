from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AWSConfig(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_CONTAINER: str
    MINIO_PORT_LOCAL: str
    BUCKET_NAME: str

    @property
    def url(self) -> str:
        return f"http://{self.AWS_CONTAINER}:{self.MINIO_PORT_LOCAL}"

    @property
    def local_url(self) -> str:
        return f"http://localhost:{self.MINIO_PORT_LOCAL}"


class KafkaConfig(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str


class BaseSettings(BaseSettings):
    class Config:
        env_file = ".env"

    AWS_CONFIG: AWSConfig = AWSConfig()
    KAFKA_CONFIG: AWS_CONFIG = KafkaConfig()
