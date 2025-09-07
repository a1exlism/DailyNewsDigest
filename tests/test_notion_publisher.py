import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from data_output.notion_publisher import NotionPublisher
from data_output.schemas import DailyDigest, CoreContent, AnalysisSummary, SourceOutlet, RetrievalInfo
from config.settings import settings

@pytest.fixture
def mock_notion_publisher():
    with patch('notion_client.AsyncClient') as MockAsyncClient:
        publisher = NotionPublisher(database_id="test_db_id")
        publisher.client = MockAsyncClient()
        yield publisher

@pytest.fixture
def notion_publisher_for_integration_test():
    # This fixture will use a real Notion client for integration tests
    publisher = NotionPublisher(database_id=settings.TEST_NOTION_DATABASE_ID)
    yield publisher

@pytest.mark.skipif(not settings.TEST_MODE, reason="测试模式未启用")
def test_split_text_into_rich_text_chunks_short_text(mock_notion_publisher):
    text = "This is a short text."
    chunks = mock_notion_publisher._split_text_into_rich_text_chunks(text)
    assert len(chunks) == 1
    assert chunks[0]["text"]["content"] == text
    assert chunks[0]["type"] == "text"

@pytest.mark.skipif(not settings.TEST_MODE, reason="测试模式未启用")
def test_split_text_into_rich_text_chunks_long_text(mock_notion_publisher):
    long_text = "a" * 2001  # 2001 characters
    chunks = mock_notion_publisher._split_text_into_rich_text_chunks(long_text)
    assert len(chunks) == 2
    assert chunks[0]["text"]["content"] == "a" * 2000
    assert chunks[1]["text"]["content"] == "a" * 1

@pytest.mark.skipif(not settings.TEST_MODE, reason="测试模式未启用")
def test_split_text_into_rich_text_chunks_exact_2000_chars(mock_notion_publisher):
    exact_text = "b" * 2000
    chunks = mock_notion_publisher._split_text_into_rich_text_chunks(exact_text)
    assert len(chunks) == 1
    assert chunks[0]["text"]["content"] == exact_text

@pytest.mark.skipif(not settings.TEST_MODE, reason="测试模式未启用")
def test_split_text_into_rich_text_chunks_empty_text(mock_notion_publisher):
    empty_text = ""
    chunks = mock_notion_publisher._split_text_into_rich_text_chunks(empty_text)
    assert len(chunks) == 1
    assert chunks[0]["text"]["content"] == empty_text


@pytest.mark.asyncio
@pytest.mark.skipif(not settings.TEST_MODE, reason="测试模式未启用")
async def test_publish_with_long_summary(notion_publisher_for_integration_test):
    long_summary = "c" * 4001  # 4001 characters
    digest = DailyDigest(
        unique_id="test_id",
        retrieval_info=RetrievalInfo(
            retrieved_date=datetime.now(),
            source_type="test_source"
        ),
        core_content=CoreContent(
            title="Test Title",
            url="http://test.com",
            publication_date=datetime.now(),
            source_outlet=SourceOutlet(name="Test Outlet", domain="testoutlet.com"),
            media_type="article",
            language="en",
            original_content="This is the original content."
        ),
        analysis_summary=AnalysisSummary(
            summary=long_summary,
            keywords=["test", "summary"],
        )
    )

    # In integration test mode, we cannot assert on mock calls.
    # We can only assert on the success of the publish operation.
    result = await notion_publisher_for_integration_test.publish(digest)
    assert result is True
