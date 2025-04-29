import json
import os
import pathlib
from dotenv import load_dotenv

from app.redis_client import Redis_Client
from app.services.utils import send_request

BASE_DIR = pathlib.Path(__file__).parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)


class NasaImages:
    base_url: str

    def __init__(self):
        base_url = os.getenv('NASA_IMAGES_API_BASE_URL')

        if base_url is None:
            raise EnvironmentError("NASA_IMAGES_API_BASE_URL must be set")

        print(f"Connecting NASA Api at: {base_url}")

        self.base_url = base_url
        self.redis = Redis_Client()

    async def get_images(self, q):
        url = f"{self.base_url}/search?q={q}"
        key = f'images:{q}'
        cached = await self.redis.client.get(key)

        if cached:
            parsed = json.loads(cached)
            if not parsed:
                return await send_request(url, key, self.redis)

        return await send_request(url, key, self.redis)

    async def get_images_links(self, nasa_id):
        url = f"{self.base_url}/asset/{nasa_id}"
        key = f'images:by_nasa_id:{nasa_id}'
        cached = await self.redis.client.get(key)

        if cached:
            parsed = json.loads(cached)
            if not parsed:
                return await send_request(url, key, self.redis)

        return await send_request(url, key, self.redis)
