

from fastapi import APIRouter

from app.services.nasa import get_planetary_apod


router = APIRouter(prefix="/apod", tags=["APod"])


# APod
@router.get("/")
async def get_apod():
    return await get_planetary_apod()
