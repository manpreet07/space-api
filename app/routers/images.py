

import os
import pathlib
from dotenv import load_dotenv
from fastapi import APIRouter
from openai import OpenAI

from app.services.nasa_images import NasaImages

BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

open_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=open_api_key)

router = APIRouter(prefix="/images", tags=["Images"])


# Nasa APIs
@router.get("/")
async def get_images(q):
    nasa_api = NasaImages()
    response = await nasa_api.get_images(q)

    if response and len(response["collection"]["items"]) > 0:
        for item in response["collection"]["items"]:
            for d in item["data"]:
                links = await nasa_api.get_images_links(d["nasa_id"])
                d["links"] = links["collection"]["items"]
        return response["collection"]["items"]
    else:
        prompt = "provide user list of space related keyowrds, " \
            "also mention this app only to search " \
            "space related images and videos from NASA"

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        return {"content": completion.choices[0].message.content}