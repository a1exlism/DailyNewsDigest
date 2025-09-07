from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class DataSource(ABC):
    """
    Abstract base class for data sources.
    """
    @abstractmethod
    async def fetch_top_stories(self, count: int) -> List[Dict[str, Any]]:
        """
        Fetch top stories from the data source.
        """
        pass

    @abstractmethod
    async def fetch_story_details(self, story_id: str) -> Dict[str, Any]:
        """
        Fetch details for a specific story.
        """
        pass

    @abstractmethod
    async def fetch_comments(self, comment_ids: List[str], count: int) -> List[Dict[str, Any]]:
        """
        Fetch a number of comments for a story.
        """
        pass

    @abstractmethod
    async def fetch_original_content(self, url: str) -> Optional[str]:
        """
        Fetch original content from a URL.
        """
        pass