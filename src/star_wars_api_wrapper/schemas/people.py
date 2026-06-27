import re
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, HttpUrl


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
