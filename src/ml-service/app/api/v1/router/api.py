from fastapi import APIRouter
from ..endpoints.training_endpoints import router as training_router

api_router = APIRouter()

api_router.include_router(training_router)