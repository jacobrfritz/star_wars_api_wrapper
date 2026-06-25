from typing import Any

import httpx
from fastapi import APIRouter

router = APIRouter()


@router.get("/people/{id}")
async def get_by_id(id: int) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://swapi.info/api/people/{id}/")
        data: dict[str, Any] = r.json()
        return data
