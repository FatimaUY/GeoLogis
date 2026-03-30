from fastapi import FastAPI, Request
from .api.v1.router.api import api_router
from pathlib import Path

app = FastAPI(
    version="1.0.0"
)

app.include_router(api_router)