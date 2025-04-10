

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.services.nasa import get_planetary_apod


router = APIRouter(prefix="/nasa", tags=["Nasa"])


@router.get("/", response_class=PlainTextResponse)
def health_check():
    return "OK"


# Nasa APIs
@router.get("/apod")
async def get_apod():
    return await get_planetary_apod()
