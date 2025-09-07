from typing import Any, Dict, Optional

import aiohttp
from utils.logger import get_logger

logger = get_logger(__name__)


async def http_get(session: aiohttp.ClientSession, url: str, params: Optional[Dict[str, Any]] = None, response_type: str = "json") -> Optional[Any]:
    """Perform an asynchronous GET request using a provided session."""
    try:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            if response_type == "json":
                return await response.json()
            elif response_type == "text":
                return await response.text()
            else:
                logger.error(f"Unsupported response_type: {response_type}")
                return None
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching {url}: {e}")
        return None
