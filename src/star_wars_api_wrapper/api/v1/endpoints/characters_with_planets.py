import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request

from star_wars_api_wrapper import get_logger
from star_wars_api_wrapper.schemas.characters_with_planets import CharacterWithPlanet
from star_wars_api_wrapper.schemas.planet import Planet

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


@router.get("/character_with_planet/{id}", response_model=CharacterWithPlanet)
async def get_by_id(id: int, request: Request) -> Any:
    cache = request.state.cache
    client = request.state.http_client
    input_url = f"{STAR_WARS_BASE_ENDPOINT}/people/{id}/"
    character_with_planet_key = input_url + "with_planet"

    if character_with_planet_key in cache:
        logger.info("loaded from cache")
        return cache[character_with_planet_key]

    if input_url in cache:
        logger.info("loaded from cache")
        person_response = cache[input_url]
    else:
        try:
            person_response = await fetch_from_api(client, input_url)
            cache[input_url] = person_response
        except httpx.TimeoutException:
            logger.warning("SWAPI took too long to respond (2.0s limit reached.)")
            raise
        except httpx.NetworkError:
            logger.warning("Network failed after initial attempt and 2 retries.")
            raise
        except httpx.HTTPStatusError as e:
            logger.warning(
                f"SWAPI returned a bad status code: {e.response.status_code}"
            )
            raise

    homeworld_url = person_response.get("homeworld")

    if not homeworld_url:
        character_with_planet = {"person": person_response, "homeworld": None}
        cache[character_with_planet_key] = character_with_planet
        return character_with_planet

    try:
        planet_response = await fetch_from_api(client, homeworld_url)
    except httpx.TimeoutException:
        logger.warning("SWAPI took too long to respond (2.0s limit reached.)")
        raise
    except httpx.NetworkError:
        logger.warning("Network failed after initial attempt and 2 retries.")
        raise
    except httpx.HTTPStatusError as e:
        logger.warning(f"SWAPI returned a bad status code: {e.response.status_code}")
        raise

    character_with_planet = {
        "person": person_response,
        "homeworld": Planet(**planet_response),
    }
    cache[character_with_planet_key] = character_with_planet
    return character_with_planet
