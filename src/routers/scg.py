
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.external_services.scg_requests import StacityGamesAPI
from src.core.config import settings

router = APIRouter(
    tags=["scg_requests"],
    responses={404: {"description": "Content not found"}},
)

scg_api = StacityGamesAPI(base_url=settings.SCG_URL, cardlist=[], max_attemps=settings.max_attemps)

@router.post("/scg/cardlist/get_prices")
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
    return JSONResponse(content=bdy)
