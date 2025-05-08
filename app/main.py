import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

import logging

from app.proxy_headers import ProxyHeaderFixMiddleware
from app.routers import apod, images, rovers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

is_prod = os.getenv("ENV") == "production"

app = FastAPI(
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
    openapi_url=None if is_prod else "/openapi.json",
)

app.add_middleware(ProxyHeaderFixMiddleware)

origins = [
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:5002",
    "https://manpreet-singh.me"
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
app.include_router(images.router, prefix="/api/v1")
