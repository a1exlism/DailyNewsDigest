import pytest
from data_processing.llm_summarizer import LLMSummarizer
from config.settings import settings


@pytest.mark.asyncio
@pytest.mark.skipif(not settings.TEST_MODE, reason="测试模式未启用")
@pytest.mark.parametrize("model_name, content_type", [
    ("gemini-2.5-pro", "article"),
    ("gemini-2.5-flash", "comments"),
    ("gemini-2.5-flash-lite", "comments"),
])
async def test_llm_model_availability(model_name, content_type):
    """Test LLM model availability and basic completion using actual LLM."""

    summarizer = LLMSummarizer()
    test_content = "This is a test article content for summarization."
    test_comments = [{"text": "This is the first test comment."},
                     {"text": "This is the second test comment."}]

    if content_type == "article":
        summary = await summarizer.summarize_content(test_content, model=model_name)
        assert isinstance(summary, str) and len(summary) > 0, f"Expected non-empty summary for model {model_name}"
    elif content_type == "comments":
        summary = await summarizer.summarize_comments(test_comments, model=model_name)
        assert isinstance(summary, str) and len(summary) > 0, f"Expected non-empty summary for model {model_name}"
