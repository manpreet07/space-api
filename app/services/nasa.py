import os
import requests
import pathlib
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

base_url = os.getenv('NASA_API_BASE_URL')
api_key = os.getenv('NASA_API_KEY')


async def get_planetary_apod():
    url = f"{base_url}/planetary/apod?api_key={api_key}"
    response = requests.get(f'{url}',
                            headers={"Content-Type": "application/json"},
                            timeout=2000)
    return response.json()
