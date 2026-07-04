from typing import Any, cast

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from star_wars_api_wrapper import get_logger

logger = get_logger(__name__)

with_retry = retry(
    wait=wait_random_exponential(multiplier=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)


@with_retry
async def fetch_from_api(client: httpx.AsyncClient, url: str) -> dict[str, Any]:
    logger.info(f"Fetching from SWAPI: {url}")
    r = await client.get(url)
    r.raise_for_status()
    return cast(dict[str, Any], r.json())
