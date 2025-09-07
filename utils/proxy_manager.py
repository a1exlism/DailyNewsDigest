import os
from typing import Optional

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

def get_proxy_settings() -> Optional[str]:
    """Reads proxy settings from environment variables or settings."""
    proxy = settings.PROXY_URL or os.environ.get("ALL_PROXY") or \
            os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY") or \
            os.environ.get("SOCKS_PROXY")
    
    if proxy:
        logger.info(f"Using proxy: {proxy}")
    else:
        logger.info("No proxy configured.")
    
    return proxy

def get_proxy_dict() -> Optional[dict]:
    """Returns a dictionary of proxy settings for httpx."""
    proxy_url = get_proxy_settings()
    if proxy_url:
        return {"all://": proxy_url}
    return None
