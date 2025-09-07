import notion_client
from typing import Dict, Any

from config.settings import settings
from data_output.base import Publisher
from data_output.schemas import DailyDigest
from utils.logger import get_logger

logger = get_logger(__name__)


class NotionPublisher(Publisher):
    """Publisher for Notion."""

    def __init__(self, database_id: str):
        self.client = notion_client.AsyncClient(auth=settings.NOTION_TOKEN)
        self.database_id = database_id

    async def publish(self, digest: DailyDigest) -> bool:
        logger.debug(f"Attempting to publish digest {digest.unique_id} to Notion.")
        """Publish a DailyDigest object to Notion."""
        properties = self._format_properties(digest)
        try:
            await self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
            )
            logger.info(f"Successfully published digest {digest.unique_id} to Notion.")
            return True
        except Exception as e:
            logger.error(f"Failed to publish digest {digest.unique_id} to Notion: {e}")
            return False

    def _split_text_into_rich_text_chunks(self, text: str, max_length: int = 2000) -> list[Dict[str, Any]]:
        """Splits a long string into a list of Notion rich text objects, each under max_length."""
        chunks = []
        if not text:
            return [{"type": "text", "text": {"content": ""}}]

        for i in range(0, len(text), max_length):
            chunk = text[i:i + max_length]
            chunks.append({"text": {"content": chunk}})
        # Notion API expects rich_text array elements to have a 'type' field
        # Adding 'type': 'text' to ensure compatibility
        return [{"type": "text", "text": {"content": chunk["text"]["content"]}} for chunk in chunks]


    def _format_properties(self, digest: DailyDigest) -> Dict[str, Any]:
        logger.debug(f"Formatting properties for digest {digest.unique_id}.")
        """Format the digest into Notion page properties."""
        # This is a simplified example. You will need to customize this based on your
        # Notion database schema.
        return {
            "Title": {"title": [{"text": {"content": digest.core_content.title}}]},            
            "URL": {"url": digest.core_content.url},
            "Summary": {"rich_text": self._split_text_into_rich_text_chunks(digest.analysis_summary.summary)},
            "Keywords": {"rich_text": [{"text": {"content": ", ".join(digest.analysis_summary.keywords)}}]},
            "Published Date": {"date": {"start": digest.core_content.publication_date.isoformat()}},
        }
