import json
import os
from fastapi import HTTPException
import pathlib
from dotenv import load_dotenv
import httpx

from app.redis_client import redis_client

BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)

base_url = os.getenv('NASA_API_BASE_URL')

if base_url is None:
    raise EnvironmentError("NASA_API_BASE_URL must be set")


async def get_planetary_apod():
    url = f"{base_url}/planetary/apod"
    key = 'apod:photo'
    cached = await redis_client.get(key)

    if cached:
        return json.loads(cached)

    return await send_request(url, key)


async def get_rover_manifests(r):
    url = f"{base_url}/api/v1/manifests/{r}"
    key = f'{r}:manifests'
    cached = await redis_client.get(key)

    if cached:
        return json.loads(cached)

    return await send_request(url, key)


async def get_rover_latest_photos(r):
    url = f"{base_url}/api/v1/rovers/{r}/latest_photos"
    key = f'{r}:latest_photos'
    cached = await redis_client.get(key)

    if cached:
        return json.loads(cached)

    return await send_request(url, key)


async def get_rover_photos_by_sol(r, sol, camera, page):
    query_param = []

    if (sol):
        query_param.append(f"?sol={sol}")
    else:
        raise HTTPException(
            status_code=404,
            detail="sol is required query param"
        )

    if (camera):
        query_param.append(f"&camera={camera}")

    if (page):
        query_param.append(f"&page={page}")

    url = f"{base_url}/api/v1/rovers/{r}/photos"

    final_param = "".join(query_param)
    url = url + final_param

    key = f'{r}:{final_param}'
    cached = await redis_client.get(key)

    if cached:
        return json.loads(cached)

    return await send_request(url, key)


async def get_rover_photos_by_earth_date(rover, earth_date, camera, page):
    query_param = []

    if (earth_date):
        query_param.append(f"?earth_date={earth_date}")
    else:
        raise HTTPException(
            status_code=404,
            detail="earth_date is required query param"
        )

    if (camera):
        query_param.append(f"&camera={camera}")

    if (page):
        query_param.append(f"&page={page}")

    url = f"{base_url}/api/v1/rovers/{rover}/photos"

    final_param = "".join(query_param)
    url = url + final_param

    cached = await redis_client.get(f'{final_param}')

    if cached:
        return json.load(cached)

    return await send_request(url, final_param)


async def send_request(url: str, key: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Resource not found on external API."
            )
        response.raise_for_status()
        await redis_client.set(
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
