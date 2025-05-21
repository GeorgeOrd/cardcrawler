import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from controllers.scg_requests import StacityGamesAPI

load_dotenv()
app = FastAPI()
scg_api = StacityGamesAPI(base_url=os.getenv("SCG_URL"), cardlist=[], max_attemps=3)

@app.post("/cardlist/get_prices")
async def get_cardlist_prices(request: Request):
    """
    Search all cards specified in list in the following pages
    1. Starcity Games
    2. Card Kingdom
    """
    body_request = await request.json()
    source_list = body_request.get('list', [])
    scg_api.cardlist = source_list
    bdy = scg_api.get_cardlist()
    return bdy
