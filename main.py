import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from controllers.scg_requests import StacityGamesAPI

load_dotenv()
scg_url = os.getenv("SCG_URL")
allow_origins = os.getenv("ALLOW_ORIGINS")

app = FastAPI()
scg_api = StacityGamesAPI(base_url=scg_url, cardlist=[], max_attemps=3)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/cardlist/get_prices")
async def get_cardlist_prices(request: Request):
    """
    Search all cards specified in list in the following pages
    1. Starcity Games
    """
    # TODO: implement card kingdom request

    # We must use async/await to prevent the event thread
    # to be blocked by reading the json request
    body_request = await request.json()
    source_list = body_request.get('list', [])
    scg_api.cardlist = source_list
    bdy = scg_api.get_cardlist()
    return bdy
