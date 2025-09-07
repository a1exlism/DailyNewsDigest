import asyncio
from typing import Any, Dict, List, Optional

import aiohttp

from data_acquisition.base import DataSource
from utils.http_client import http_get
from utils.logger import get_logger

logger = get_logger(__name__)


class HackerNewsDataSource(DataSource):
    """Data source for Hacker News."""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def fetch_top_stories(self, count: int) -> List[Dict[str, Any]]:
        """Fetch top stories from Hacker News."""
        logger.debug(f"Fetching top {count} stories.")
        top_stories_url = f"{self.BASE_URL}/topstories.json"
        story_ids = await http_get(self.session, top_stories_url)
        if not story_ids:
            logger.info("No top story IDs found.")
            return []

        tasks = [
            self.fetch_story_details(story_id) for story_id in story_ids[:count]
        ]
        stories = await asyncio.gather(*tasks)
        return [story for story in stories if story]

    async def fetch_story_details(self, story_id: int) -> Optional[Dict[str, Any]]:
        """Fetch details for a specific story."""
        logger.debug(f"Fetching details for story ID: {story_id}.")
        story_url = f"{self.BASE_URL}/item/{story_id}.json"
        details = await http_get(self.session, story_url)
        if not details:
            logger.info(f"No details found for story ID: {story_id}.")
        return details

    async def fetch_comments(self, comment_ids: List[int], count: int) -> List[Dict[str, Any]]:
        """Fetch a number of comments for a story."""
        # 这里多获取50%
        fetch_limit = int(count * 1.2)
        if fetch_limit > len(comment_ids):
            fetch_limit = len(comment_ids)
        logger.debug(f"Fetching {count} comments for comment IDs: {comment_ids}.")
        if not comment_ids:
            logger.info("No comment IDs provided.")
            return []

        tasks = [
            self._fetch_comment(comment_id) for comment_id in comment_ids[:fetch_limit]
        ]
        comments = await asyncio.gather(*tasks)
        comments_filtered = [comment for comment in comments if comment and not comment.get("deleted")]
        return comments_filtered[:count]

    async def _fetch_comment(self, comment_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single comment."""
        logger.debug(f"Fetching details for comment ID: {comment_id}.")
        comment_url = f"{self.BASE_URL}/item/{comment_id}.json"
        comment = await http_get(self.session, comment_url)
        if not comment:
            logger.info(f"No details found for comment ID: {comment_id}.")
        return comment

    async def fetch_original_content(self, url: str) -> Optional[str]:
        """Not implemented for HackerNewsDataSource, will be handled by WebScraper."""
        logger.warning(
            "fetch_original_content is not implemented in HackerNewsDataSource. "
            "Use WebScraper for this purpose."
        )
        return None
