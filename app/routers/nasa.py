

from fastapi import APIRouter

from app.services.nasa import get_planetary_apod


router = APIRouter(prefix="/nasa", tags=["Nasa"])


# Nasa APIs
@router.get("/apod")
async def get_apod():
    return await get_planetary_apod()
