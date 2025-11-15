from fastapi import APIRouter

from src.routers import scg
from src.core.config import settings

api_router = APIRouter()
api_router.include_router(scg.router)