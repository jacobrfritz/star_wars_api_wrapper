from typing import Any

from star_wars_api_wrapper.core.exceptions import BadRequestException
from star_wars_api_wrapper.repositories.base import BaseItemsRepository
from star_wars_api_wrapper.schemas.items import ItemCreate, ItemUpdate


class InMemoryItemsRepository(BaseItemsRepository):
    """
    In-memory concrete storage provider implementing CRUD operations.
    Keeps state in class-level structures to survive request instance lifetimes.
    """

    _db: dict[int, dict[str, Any]] = {
        1: {
            "id": 1,
            "name": "Screwdriver",
            "description": "Standard flathead screwdriver",
            "price": 5.99,
            "tax": 0.50,
        },
        2: {
            "id": 2,
            "name": "Hammer",
            "description": "Heavy-duty claw hammer",
            "price": 14.50,
            "tax": 1.20,
        },
    }
    _id_counter: int = 2

    async def list(self, skip: int = 0, limit: int = 10) -> list[dict[str, Any]]:
        items = list(self._db.values())
        return items[skip : skip + limit]

    async def get(self, item_id: int) -> dict[str, Any] | None:
        return self._db.get(item_id)

    async def create(self, item_in: ItemCreate) -> dict[str, Any]:
        # Duplicate detection check
        for item in self._db.values():
            if item["name"].lower() == item_in.name.lower():
                raise BadRequestException(
                    detail=f"Item with name '{item_in.name}' already exists.",
                    code="DUPLICATE_ITEM",
                )

        InMemoryItemsRepository._id_counter += 1
        new_item = {
            "id": InMemoryItemsRepository._id_counter,
            **item_in.model_dump(),
        }
        self._db[InMemoryItemsRepository._id_counter] = new_item
        return new_item

    async def update(self, item_id: int, item_in: ItemUpdate) -> dict[str, Any] | None:
        if item_id not in self._db:
            return None

        item = self._db[item_id]
        update_data = item_in.model_dump(exclude_unset=True)

        for key, val in update_data.items():
            item[key] = val

        self._db[item_id] = item
        return item

    async def delete(self, item_id: int) -> bool:
        if item_id not in self._db:
            return False
        del self._db[item_id]
        return True
