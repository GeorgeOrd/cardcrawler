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

# @app.post("/cardlist/get_prices")
# async def get_cardlist_prices(request: Request):
#     """
#     Search all cards specified in list in the following pages
#     1. Starcity Games
#     """
#     # TODO: implement card kingdom request

#     # We must use async/await to prevent the event thread
#     # to be blocked by reading the json request
#     body_request = await request.json()
#     source_list = body_request.get('list', [])
#     scg_api.cardlist = source_list
#     bdy = scg_api.get_cardlist()
#     return bdy
