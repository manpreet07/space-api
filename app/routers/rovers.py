

from fastapi import APIRouter, Query

from app.services.nasa import (
    get_rover_photos_by_sol,
    get_rover_photos_by_earth_date
)


router = APIRouter(prefix="/rovers", tags=["Rovers"])


# Rovers API
@router.get("/{rover}/photos/by_sol")
async def get_photos_by_sol(
    rover,
    sol,
    camera=Query(None),
    page=Query(None)
):
    return await get_rover_photos_by_sol(rover, sol, camera, page)


@router.get("/{rover}/photos/by_earth_date")
async def get_photos_by_earth_date(
    rover,
    earth_date=Query(..., description="YYYY-MM-DD"),
    camera=Query(None),
    page=Query(None)
):
    return await get_rover_photos_by_earth_date(
        rover,
        earth_date,
        camera,
        page
    )
