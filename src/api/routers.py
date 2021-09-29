from fastapi import APIRouter
from src.api.controllers import settings


api_router = APIRouter()
api_router.include_router(settings.router, prefix="/matrix/settings")
