import pathlib
from dotenv import load_dotenv
import redis.asyncio as redis
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)


class Redis_Client:
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST')
        redis_port = os.getenv('REDIS_PORT')

        if redis_host is None:
            raise EnvironmentError("REDIS_HOST must be set")

        if redis_port is None:
            raise EnvironmentError("REDIS_PORT must be set")

        redis_url = f"redis://{redis_host}:{redis_port}"
        print(f"🔌 Connecting to Redis at: {redis_url}")

        self._client = redis.Redis.from_url(
            redis_url,
            decode_responses=True
        )

    @property
    def client(self) -> redis.Redis:
        return self._client

    @client.setter
    def client(self, value):
        self._client = value
