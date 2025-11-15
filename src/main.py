import os
# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.external_services.scg_requests import StacityGamesAPI
from src.core.config import settings
from src.routers.main import api_router
# load_dotenv()
# scg_url = os.getenv("SCG_URL")
# allow_origins = os.getenv("ALLOW_ORIGINS")

app = FastAPI(
    title=settings.app_name,
    description="API to get card prices from different TCG vendors",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix=settings.api_prefix
)

