

from fastapi import APIRouter

from app.services.nasa import Nasa


router = APIRouter(prefix="/apod", tags=["APod"])


# Nasa APIs
@router.get("/")
async def get_apod():
    nasa_api = Nasa()
    return await nasa_api.get_planetary_apod()
