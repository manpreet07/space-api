import json
import os
from fastapi import HTTPException
import requests
import pathlib
from dotenv import load_dotenv

from app.redis_client import redis_client

BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path, override=True)

base_url = os.getenv('NASA_API_BASE_URL')
api_key = os.getenv('NASA_API_KEY')

if base_url is None:
    raise EnvironmentError("NASA_API_BASE_URL must be set")

if api_key is None:
    raise EnvironmentError("NASA_API_KEY must be set")


async def get_planetary_apod():
    cached = await redis_client.get('apod:photo')

    if cached:
        return json.loads(cached)
    else:
        url = f"{base_url}/planetary/apod?api_key={api_key}"

        response = requests.get(f'{url}',
                                headers={"Content-Type": "application/json"},
                                timeout=2000)
        await redis_client.set(
            'apod:photo',
            json.dumps(response.json()), ex=60 * 60 * 24
        )
        return response.json()


async def get_rover_photos_by_sol(r, sol, camera, page):
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
        f"{base_url}/mars-photos/api/v1/rovers/{r}/photos?api_key={api_key}"
    )

    final_param = "".join(query_param)
    url = url + final_param

    cached = await redis_client.get(f'{final_param}')

    if cached:
        return json.loads(cached)
    else:
        response = requests.get(f'{url}',
                                headers={"Content-Type": "application/json"},
                                timeout=2000)
        await redis_client.set(f'{final_param}', json.dumps(response.json()))
        return response.json()


async def get_rover_photos_by_earth_date(rover, earth_date, camera, page):
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
        f"{base_url}/mars-photos/api/v1/rovers/{rover}/photos"
        f"?api_key={api_key}"
    )

    final_param = "".join(query_param)
    url = url + final_param

    cached = await redis_client.get(f'{final_param}')

    if cached:
        return json.load(cached)
    else:
        res = requests.get(f'{url}',
                           headers={"Content-Type": "application/json"},
                           timeout=2000)
        await redis_client.set(f'{final_param}', json.dumps(res.json()))
        return res.json()
