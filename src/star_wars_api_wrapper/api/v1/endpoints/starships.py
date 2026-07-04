import asyncio
import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request

from star_wars_api_wrapper import get_logger

from ..utils.utils import fetch_from_api

load_dotenv()

logger = get_logger(__name__)

STAR_WARS_BASE_ENDPOINT = os.getenv("star_wars_api_endpoint")

"""
People Input Format

{
  "name": "Luke Skywalker",
  "height": 172,
  "mass": 77,
  "hair_color": "blond",
  "skin_color": "fair",
  "eye_color": "blue",
  "birth_year": "19BBY",
  "gender": "male",
  "homeworld": "https://swapi.info/api/planets/1",
  "films": [
    "https://swapi.info/api/films/1",
    "https://swapi.info/api/films/2",
    "https://swapi.info/api/films/3",
    "https://swapi.info/api/films/6"
  ],
  "species": [],
  "vehicles": [
    "https://swapi.info/api/vehicles/14",
    "https://swapi.info/api/vehicles/30"
  ],
  "starships": [
    "https://swapi.info/api/starships/12",
    "https://swapi.info/api/starships/22"
  ],
  "created": "2014-12-09T13:50:51.644000Z",
  "edited": "2014-12-20T21:17:56.891000Z",
  "url": "https://swapi.info/api/people/1"
}

"""


router = APIRouter()


@router.get("/starships/{id}")
async def get_by_id(id: int, request: Request) -> Any:
    client = request.state.http_client
    input_url = f"{STAR_WARS_BASE_ENDPOINT}/people/{id}/"
    try:
        if input_url in request.state.cache:
            logger.info("loaded from cache")
            return request.state.cache[input_url]
        person = await fetch_from_api(client, input_url)
        request.state.cache[input_url] = person
    except httpx.TimeoutException:
        logger.warning("SWAPI took too long to respond (2.0s limit reached).")
        raise
    except httpx.NetworkError:
        logger.warning("Network failed after initial attempt and 2 retries.")
        raise
    except httpx.HTTPStatusError as e:
        logger.warning(f"SWAPI returned a bad status code: {e.response.status_code}")
        raise

    starships = person.get("starships")
    starship_tasks = list()

    if starships:
        starship_tasks = [fetch_from_api(client, starship) for starship in starships]
        starship_results = await asyncio.gather(*starship_tasks)
    else:
        return [None]
    starship_results = [starship for starship in starship_results]
    for starship, starship_result in zip(starships, starship_results, strict=True):
        request.state.cache[starship] = starship_result
    return starship_results
