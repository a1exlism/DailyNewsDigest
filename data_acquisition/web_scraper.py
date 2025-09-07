import aiohttp
import trafilatura
from typing import Optional

from utils.http_client import http_get
from utils.logger import get_logger

logger = get_logger(__name__)


class WebScraper:
    """A web scraper to extract main content from URLs."""

    @staticmethod
    async def fetch_and_extract_content(session: aiohttp.ClientSession, url: str) -> Optional[str]:
        logger.debug(f"Fetching and extracting content from URL: {url}")
        """Fetches content from a URL and extracts the main text."""
        try:
            # Use http_get to fetch raw HTML content as text
            html_content = await http_get(session, url, response_type="text")
            if not html_content:
                logger.info(f"No HTML content fetched from {url}.")
                return None

            # Use trafilatura to extract the main content
            main_content = trafilatura.extract(
                html_content,
                include_comments=False,
                include_tables=False,
                no_fallback=True,
            )
            return main_content
        except Exception as e:
            logger.error(f"Failed to fetch or extract content from {url}: {e}")
            return None
