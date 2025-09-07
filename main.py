from utils.proxy_manager import get_proxy_settings

import asyncio
import hashlib
from datetime import datetime, timezone

import aiohttp

from config.settings import settings
from data_acquisition.hackernews import HackerNewsDataSource
from data_acquisition.web_scraper import WebScraper
from data_output.notion_publisher import NotionPublisher
from data_output.schemas import (
    AnalysisSummary,
    CoreContent,
    DailyDigest,
    RetrievalInfo,
    SourceOutlet,
)
from data_processing.llm_summarizer import LLMSummarizer
from notification.telegram_notifier import TelegramNotifier
from utils.logger import get_logger

logger = get_logger(__name__)


class Orchestrator:
    """Orchestrates the entire news digest generation process."""

    def __init__(self, session: aiohttp.ClientSession):
        self.data_source = HackerNewsDataSource(session=session)
        self.llm_summarizer = LLMSummarizer()
        self.publisher = NotionPublisher(database_id=settings.NOTION_DATABASE_ID)
        self.notifier = TelegramNotifier(chat_id=settings.TELEGRAM_CHAT_ID)
        self.session = session

    async def run(self):
        """Run the orchestration process."""
        logger.info("Starting Daily News Digest generation...")
        try:
            stories = await self.data_source.fetch_top_stories(settings.TOP_N_NEWS)
            for story_data in stories:
                if not story_data.get("url"):
                    continue

                digest = await self.process_story(story_data)
                if digest:
                    await self.publisher.publish(digest)

            await self.notifier.send_notification(
                "Daily News Digest generation completed successfully.", "SUCCESS"
            )
        except Exception as e:
            logger.error(f"An error occurred during orchestration: {e}", exc_info=True)
            await self.notifier.send_notification(f"An error occurred: {e}", "ERROR")

    async def process_story(self, story_data: dict) -> DailyDigest | None:
        """Process a single story."""
        url = story_data.get("url")
        logger.info(f"Processing story: {story_data.get('title')}")

        content_task = WebScraper.fetch_and_extract_content(self.session, url)
        comments_task = self.data_source.fetch_comments(
            story_data.get("kids", []), settings.TOP_M_COMMENTS
        )
        original_content, comments = await asyncio.gather(content_task, comments_task)

        if not original_content:
            logger.warning(f"Could not fetch or extract content from {url}")
            return None

        summary_task = self.llm_summarizer.summarize_content(original_content)
        comment_summary_task = self.llm_summarizer.summarize_comments(comments)
        summary, comment_summary = await asyncio.gather(
            summary_task, comment_summary_task
        )

        if not summary:
            logger.warning(f"Could not summarize content for {url}")
            return None

        final_summary = (
            f"{summary}\n\n--- Comment Summary ---\n"
            f"{comment_summary or 'No comments to summarize.'}"
        )

        return self._create_digest(story_data, final_summary, original_content, url)

    def _create_digest(
        self, story_data, summary, original_content, url
    ) -> DailyDigest:
        """Create a DailyDigest object from the processed data."""
        now = datetime.now(timezone.utc)
        return DailyDigest(
            unique_id=hashlib.md5(url.encode()).hexdigest(),
            retrieval_info=RetrievalInfo(
                retrieved_date=now, source_type="Hacker News API"
            ),
            core_content=CoreContent(
                title=story_data.get("title", ""),
                url=url,
                publication_date=datetime.fromtimestamp(
                    story_data.get("time", 0), tz=timezone.utc
                ),
                author=[story_data.get("by", "")],
                source_outlet=SourceOutlet(
                    name="Hacker News", domain="news.ycombinator.com"
                ),
                media_type="Text Article",
                language="en",
                original_content=original_content,
            ),
            analysis_summary=AnalysisSummary(
                summary=summary,
                keywords=[],  # Keyword extraction could be a future feature
            ),
        )


async def main():
    """Main entry point for the application."""
    proxy_url = get_proxy_settings()
    async with aiohttp.ClientSession(proxy=proxy_url) as session:
        orchestrator = Orchestrator(session=session)        
        await orchestrator.run()


if __name__ == "__main__":
    if settings.TEST_MODE:
        logger.error("Main application entry point is disabled in TEST_MODE. To run the application, set TEST_MODE=False in your environment.")
        exit
    else:
        asyncio.run(main())
