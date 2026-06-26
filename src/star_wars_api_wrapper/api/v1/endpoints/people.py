from typing import Any

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/people/{id}")
async def get_by_id(id: int) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://swapi.info/api/people/{id}/")
        if r.status_code != 200:
            raise HTTPException(
                status_code=r.status_code, detail=f"Swapi returned an error {r.text}"
            )
        data: dict[str, Any] = r.json()
        return data
