from datetime import date
import json
import os
import pathlib
from dotenv import load_dotenv
from fastapi import HTTPException

from app.redis_client import Redis_Client
from app.services.utils import send_request

BASE_DIR = pathlib.Path(__file__).parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)


class MarsRoverPhotos:
    base_url: str

    def __init__(self):
        base_url = os.getenv('NASA_API_BASE_URL')
        api_key = os.getenv('NASA_API_KEY')

        if base_url is None:
            raise EnvironmentError("NASA_API_BASE_URL must be set")

        if api_key is None:
            raise EnvironmentError("NASA_API_KEY must be set")

        print(f"Connecting NASA Api at: {base_url}")

        self.base_url = base_url
        self.api_key = api_key
        self.redis = Redis_Client()

    async def get_planetary_apod(self):
        url = f"{self.base_url}/planetary/apod?api_key={self.api_key}"
        key = f'apod:photo:{date.today()}'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await send_request(url, key, self.redis)

    async def get_rover_manifests(self, r):
        url = (
            f"{self.base_url}/mars-photos/api/v1/manifests/{r}"
            f"?api_key={self.api_key}"
        )
        key = f'{r}:manifests:{date.today()}'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await send_request(url, key, self.redis)

    async def get_rover_latest_photos(self, r):
        url = (
            f"{self.base_url}/mars-photos/api/v1/rovers/{r}/latest_photos"
            f"?api_key={self.api_key}"
        )
        key = f'{r}:latest_photos:{date.today()}'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await send_request(url, key, self.redis)

    async def get_rover_photos_by_sol(self, r, sol, camera, page):
        query_param = []

        if (sol):
            query_param.append(f"&sol={sol}")
        else:
            raise HTTPException(
                status_code=404,
                detail="sol is required query param"
            )

        if (camera):
            query_param.append(f"&camera={camera}")

        if (page):
            query_param.append(f"&page={page}")

        url = (
            f"{self.base_url}/mars-photos/api/v1/rovers/{r}/photos"
            f"?api_key={self.api_key}"
        )

        final_param = "".join(query_param)
        url = url + final_param

        key = f'{r}:{final_param}:{date.today()}'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await send_request(url, key, self.redis)

    async def get_rover_photos_by_earth_date(
            self,
            rover,
            earth_date,
            camera,
            page
    ):
        query_param = []

        if (earth_date):
            query_param.append(f"&earth_date={earth_date}")
        else:
            raise HTTPException(
                status_code=404,
                detail="earth_date is required query param"
            )

        if (camera):
            query_param.append(f"&camera={camera}")

        if (page):
            query_param.append(f"&page={page}")

        url = (
            f"{self.base_url}/mars-photos/api/v1/rovers/{rover}/photos"
            f"?api_key={self.api_key}"
        )

        final_param = "".join(query_param)
        url = url + final_param

        cached = await self.redis.client.get(f'{final_param}')

        if cached:
            return json.load(cached)

        return await send_request(url, final_param, self.redis)
