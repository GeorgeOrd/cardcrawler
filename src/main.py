from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.routers.main import api_router
from src.models.user import create_db_and_tables

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

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(
    api_router,
    prefix=settings.api_prefix
)
