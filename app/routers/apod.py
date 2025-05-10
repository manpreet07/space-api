import os
from fastapi import APIRouter

from app.services.mars_rovers_photos import MarsRoverPhotos

router = APIRouter(prefix="/apod", tags=["APod"])

env = os.getenv("ENV")


# Nasa APIs
@router.get("/")
async def get_apod():
    nasa_api = MarsRoverPhotos()
    return await nasa_api.get_planetary_apod()
