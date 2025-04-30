

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
    message = "Sorry, this app only show space related images and videos " \
        "from NASA. Please ask about something in space."

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        store=True,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a space keyword extractor. Your job is to return"
                    " a list of space-related keywords "
                    "from the user's request. Only include terms related to"
                    " space, astronomy, planets, celestial bodies, "
                    "space missions, or related science. Return the result as"
                    " a plain, comma-separated string of keywords in "
                    "lowercase, without brackets. Do not include duplicates "
                    "or unrelated terms.if there are no"
                    f" space related words found return: {message}"
                )
            },
            {
                "role": "user",
                "content": q
            }
        ],
        temperature=0
    )

    query = completion.choices[0].message.content
    if query != message:
        nasa_api = NasaImages()
        response = await nasa_api.get_images(query)

        if response and len(response["collection"]["items"]) > 0:
            for item in response["collection"]["items"]:
                for d in item["data"]:
                    links = await nasa_api.get_images_links(d["nasa_id"])
                    d["links"] = links["collection"]["items"]
            return response["collection"]["items"]
    else:
        return {"content": completion.choices[0].message.content}
