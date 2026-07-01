import asyncio
import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from star_wars_api_wrapper import get_logger

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
    async with httpx.AsyncClient() as client:
        input_url = f"{STAR_WARS_BASE_ENDPOINT}/people/{id}/"
        if input_url in request.state.cache.keys():
            logger.info("loaded from cache")
            return request.state.cache[input_url]
        r = await client.get(input_url)
        if r.status_code != 200:
            raise HTTPException(
                status_code=r.status_code, detail=f"Swapi returned an error {r.text}"
            )
        person = r.json()
        starships = person.get("starships")
        starship_tasks = list()

        if starships:
            async with httpx.AsyncClient() as client:
                starship_tasks = [client.get(starship) for starship in starships]
                starship_results = await asyncio.gather(*starship_tasks)
        else:
            return [None]
        startship_results = [starship.json() for starship in starship_results]
        request.state.cache[input_url] = startship_results
        return startship_results
