from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

import logging

from app.routers import apod, rovers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:5000",
    "http://localhost:5001",
]
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=PlainTextResponse)
def health_check():
    return "OK"


# Nasa APIs
app.include_router(apod.router, prefix="/api/v1")
app.include_router(rovers.router, prefix="/api/v1")


