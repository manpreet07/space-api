

from fastapi import APIRouter, Query

from app.services.mars_rovers_photos import MarsRoverPhotos


router = APIRouter(prefix="/rovers", tags=["Rovers"])

nasa_api = MarsRoverPhotos()


# Rovers API
@router.get("/manifests/{rover}")
async def get_manifests_by_rover(rover):
    return await nasa_api.get_rover_manifests(rover)


@router.get("/{rover}/latest_photos")
async def get_latest_photos_by_rover(rover):
    return await nasa_api.get_rover_latest_photos(rover)


@router.get("/{rover}/photos/by_sol")
async def get_photos_by_sol(
    rover,
    sol,
    camera=Query(None),
    page=Query(None)
):
    return await nasa_api.get_rover_photos_by_sol(rover, sol, camera, page)


@router.get("/{rover}/photos/by_earth_date")
async def get_photos_by_earth_date(
    rover,
    earth_date=Query(..., description="YYYY-MM-DD"),
    camera=Query(None),
    page=Query(None)
):
    return await nasa_api.get_rover_photos_by_earth_date(
        rover,
        earth_date,
        camera,
        page
    )
