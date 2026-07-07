# https://swapi.dev/api/people/?search=luke

import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, Request
from rank_bm25 import BM25Okapi  # type: ignore[import-untyped]

from star_wars_api_wrapper import get_logger
from star_wars_api_wrapper.schemas.people import Person

from ..utils.utils import fetch_from_api

load_dotenv()

logger = get_logger(__name__)

STAR_WARS_BASE_ENDPOINT = os.getenv("star_wars_api_endpoint")

router = APIRouter()


@router.get("/people_search/", response_model=Person)
async def get_by_id(request: Request, person_name: str = "luke") -> Any:
    cache = request.state.cache
    client = request.state.http_client

    input_url = f"{STAR_WARS_BASE_ENDPOINT}/people/?search={person_name}"
    if input_url in cache:
        logger.info("Loaded from Cache")
        return cache[input_url]
    try:
        r = await fetch_from_api(client, input_url)
    except httpx.TimeoutException:
        logger.warning("SWAPI took too long to respond (2.0s limit reached).")
        raise
    except httpx.NetworkError:
        logger.warning("Network failed after initial attempt and 2 retries.")
        raise
    except httpx.HTTPStatusError as e:
        logger.warning(f"SWAPI returned a bad status code: {e.response.status_code}")
        raise

    people = r
    people_list = people.get("results", []) if isinstance(people, dict) else people

    tokenized_corpus = [person.get("name").lower().split(" ") for person in people_list]

    names = [person.get("name") for person in people_list]

    bm25 = BM25Okapi(tokenized_corpus)

    query = person_name
    tokenized_query = query.lower().split(" ")

    top_n_results = bm25.get_top_n(tokenized_query, names, n=1)

    matched_people = [p for p in people_list if p.get("name") in top_n_results][0]
    cache[input_url] = matched_people
    return matched_people


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
