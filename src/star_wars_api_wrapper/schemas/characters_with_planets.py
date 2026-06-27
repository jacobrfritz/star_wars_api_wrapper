from pydantic import BaseModel
from star_wars_api_wrapper.schemas.people import Person
from star_wars_api_wrapper.schemas.planet import Planet


class CharacterWithPlanet(BaseModel):
    person: Person
    homeworld: Planet | None
