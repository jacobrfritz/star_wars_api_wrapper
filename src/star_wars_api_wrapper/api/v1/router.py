from fastapi import APIRouter
from star_wars_api_wrapper.api.v1.endpoints import health, items, people

api_router = APIRouter()
api_router.include_router(health.router, tags=["System"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
api_router.include_router(people.router)
