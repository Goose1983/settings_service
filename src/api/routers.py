from fastapi import APIRouter
from src.api.controllers import template


api_router = APIRouter()
api_router.include_router(template.router, prefix="/template")