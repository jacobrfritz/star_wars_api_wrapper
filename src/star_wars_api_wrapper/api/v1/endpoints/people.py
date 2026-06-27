import re
from datetime import datetime
from typing import Annotated, Any

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, BeforeValidator, HttpUrl

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


def coerce_number(number: Any) -> int | None:
    if isinstance(number, int):
        return number
    elif isinstance(number, str):
        match = re.search(r"\d+", number)
        if match:
            return int(match.group())
        else:
            return None
    else:
        return None


router = APIRouter()


class Person(BaseModel):
    name: str
    height: Annotated[int | None, BeforeValidator(coerce_number)]
    mass: Annotated[int | None, BeforeValidator(coerce_number)]
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: HttpUrl
    films: list[HttpUrl]
    species: list[HttpUrl]
    vehicles: list[HttpUrl]
    starships: list[HttpUrl]
    created: datetime
    edited: datetime
    url: HttpUrl


@router.get("/people/{id}", response_model=Person)
async def get_by_id(id: int) -> Any:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://swapi.info/api/people/{id}/")
        if r.status_code != 200:
            raise HTTPException(
                status_code=r.status_code, detail=f"Swapi returned an error {r.text}"
            )
        return r.json()
