import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from star_wars_api_wrapper import get_logger
from star_wars_api_wrapper.schemas.characters_with_planets import CharacterWithPlanet
from star_wars_api_wrapper.schemas.planet import Planet

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
async def get_by_id(id: int, request:Request) -> Any:
  cache = request.state.cache
  input_url = f"{STAR_WARS_BASE_ENDPOINT}/people/{id}/"
  if input_url in cache.keys():
    return cache[input_url]
  
  async with httpx.AsyncClient() as client:
      person_response = await client.get(input_url)
      if person_response.status_code != 200:
          raise HTTPException(
              status_code=person_response.status_code,
              detail=f"Swapi returned an error {person_response.text}",
          )
      homeworld_url = person_response.json().get("homeworld")
      if homeworld_url:
        if homeworld_url in cache.keys():
          return cache[homeworld_url]
          planet_response = await client.get(homeworld_url)
          if planet_response.status_code != 200:
              raise HTTPException(
                  status_code=planet_response.status_code,
                  detail=f"Swapi returned an error {planet_response.text}",
              )
      else:
          return None
      cache[input_url] = person_response.json()
      cache[homeworld_url] = planet_response.json()
      character_with_planet = person_response.json()
      character_with_planet["homeworld"] = Planet(**planet_response.json())
      return character_with_planet
