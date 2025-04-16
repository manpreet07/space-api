import json
import os
import pathlib
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx

from app.redis_client import Redis_Client

BASE_DIR = pathlib.Path(__file__).parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)


class Nasa:
    base_url: str

    def __init__(self):
        base_url = os.getenv('NASA_API_BASE_URL')
        api_key = os.getenv('NASA_API_KEY')

        if base_url is None:
            raise EnvironmentError("NASA_API_BASE_URL must be set")

        if base_url is None:
            raise EnvironmentError("NASA_API_KEY must be set")

        print(f"🔌 Connecting NASA Api at: {base_url}")

        self.base_url = base_url
        self.api_key = api_key
        self.redis = Redis_Client()

    async def get_planetary_apod(self):
        url = f"{self.base_url}/planetary/apod?api_key={self.api_key}"
        key = 'apod:photo'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await self.send_request(url, key)

    async def get_rover_manifests(self, r):
        url = (
            f"{self.base_url}/mars-photos/api/v1/manifests/{r}"
            f"?api_key={self.api_key}"
        )
        key = f'{r}:manifests'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await self.send_request(url, key)

    async def get_rover_latest_photos(self, r):
        url = (
            f"{self.base_url}/mars-photos/api/v1/rovers/{r}/latest_photos"
            f"?api_key={self.api_key}"
        )
        key = f'{r}:latest_photos'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await self.send_request(url, key)

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

        key = f'{r}:{final_param}'
        cached = await self.redis.client.get(key)

        if cached:
            return json.loads(cached)

        return await self.send_request(url, key)

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

        return await self.send_request(url, final_param)

    async def send_request(self, url: str, key: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Resource not found on external API."
                )
            response.raise_for_status()
            await self.redis.client.set(
                f'{key}',
                json.dumps(response.json())
            )
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Error contacting external API: {exc}"
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=str(exc)
            )
