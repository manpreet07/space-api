import pathlib
from dotenv import load_dotenv
import redis.asyncio as redis
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

REDIS_URL = os.getenv("REDIS_URL", f"redis://{redis_host}:{redis_port}")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
