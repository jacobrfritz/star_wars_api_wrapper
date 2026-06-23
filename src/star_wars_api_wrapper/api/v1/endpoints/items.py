from typing import Any

from fastapi import APIRouter, Depends, Query
from star_wars_api_wrapper.core.exceptions import NotFoundException
from star_wars_api_wrapper.repositories.base import BaseItemsRepository
from star_wars_api_wrapper.repositories.items import InMemoryItemsRepository
from star_wars_api_wrapper.schemas.items import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()


def get_items_repository() -> BaseItemsRepository:
    """Dependency provider returning an active items storage repository."""
    return InMemoryItemsRepository()


@router.get("", response_model=list[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of items to return"),
    repo: BaseItemsRepository = Depends(get_items_repository),
) -> list[Any]:
    """Retrieve items with pagination, decoupled from data access details."""
    return await repo.list(skip=skip, limit=limit)


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(
    item_in: ItemCreate,
    repo: BaseItemsRepository = Depends(get_items_repository),
) -> Any:
    """Create a new item."""
    return await repo.create(item_in)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    repo: BaseItemsRepository = Depends(get_items_repository),
) -> Any:
    """Retrieve a single item by ID, throwing HTTP 404 if missing."""
    item = await repo.get(item_id)
    if not item:
        raise NotFoundException(detail=f"Item with ID {item_id} not found.")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    repo: BaseItemsRepository = Depends(get_items_repository),
) -> Any:
    """Update an existing item's fields."""
    item = await repo.update(item_id, item_in)
    if not item:
        raise NotFoundException(detail=f"Item with ID {item_id} not found.")
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    repo: BaseItemsRepository = Depends(get_items_repository),
) -> None:
    """Delete an item by ID."""
    deleted = await repo.delete(item_id)
    if not deleted:
        raise NotFoundException(detail=f"Item with ID {item_id} not found.")
