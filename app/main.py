from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import nasa

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nasa APIs
app.include_router(nasa.router, prefix="/api/v1")
