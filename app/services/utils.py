import json
from fastapi import HTTPException
import httpx

from app.redis_client import Redis_Client


async def send_request(url: str, key: str, redis: Redis_Client):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Resource not found on external API."
            )
        response.raise_for_status()
        await redis.client.set(
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
