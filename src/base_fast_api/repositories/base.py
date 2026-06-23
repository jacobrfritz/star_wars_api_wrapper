from abc import ABC, abstractmethod
from typing import Any

from base_fast_api.schemas.items import ItemCreate, ItemUpdate


class BaseItemsRepository(ABC):
    """Abstract interface defining required behaviors for items storage providers."""

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 10) -> list[Any]:
        """Retrieve a list of items with pagination offsets."""
        pass

    @abstractmethod
    async def get(self, item_id: int) -> Any | None:
        """Retrieve a single item by ID, or return None if not found."""
        pass

    @abstractmethod
    async def create(self, item_in: ItemCreate) -> Any:
        """Persist a new item to storage.
        Raises BadRequestException on duplicate name.
        """
        pass

    @abstractmethod
    async def update(self, item_id: int, item_in: ItemUpdate) -> Any | None:
        """Update properties of an existing item.
        Returns updated record, or None if not found.
        """
        pass

    @abstractmethod
    async def delete(self, item_id: int) -> bool:
        """Remove an item from storage. Returns True if deleted, False if not found."""
        pass
