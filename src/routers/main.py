from fastapi import APIRouter

from src.routers import scg
from src.routers import user
from src.core.config import settings

api_router = APIRouter()
api_router.include_router(scg.router)
api_router.include_router(user.router)