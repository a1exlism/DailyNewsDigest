from typing import List, Dict, Any, Optional

from openai import AsyncOpenAI

from config.settings import settings
from config.llm_params import LLM_MODELS, LLM_SETTINGS
from config.prompts import PROMPTS
from data_processing.base import Processor
from utils.logger import get_logger

logger = get_logger(__name__)


class LLMSummarizer(Processor):
    """Summarizer using OpenAI-compatible APIs."""

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )

    async def summarize_content(
        self, content: str, model: str = LLM_MODELS["summarize_content"]
    ) -> Optional[str]:
        logger.debug(f"Summarizing content using model: {model}")
        """Summarize a single content string."""
        if not content:
            logger.info("No content provided for summarization.")
            return None
        
        prompt = PROMPTS["summarize_content"].format(content=content)
        return await self._get_completion(prompt, model)

    async def summarize_comments(
        self, comments: List[Dict[str, Any]], model: str = LLM_MODELS["summarize_comments"]
    ) -> Optional[str]:
        logger.debug(f"Summarizing comments using model: {model}")
        """Summarize a list of comments."""
        if not comments:
            logger.info("No comments provided for summarization.")
            return None

        comment_texts = [
            comment.get("text", "") for comment in comments if comment.get("text")
        ]
        full_text = " ".join(comment_texts)
        prompt = PROMPTS["summarize_comments"].format(content=full_text)
        return await self._get_completion(prompt, model)

    async def _get_completion(self, prompt: str, model: str) -> Optional[str]:
        logger.debug(f"Getting LLM completion for model: {model}, prompt length: {len(prompt)}")
        """Get completion from the LLM."""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": PROMPTS["system_message"]},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=LLM_SETTINGS["max_tokens"],
                temperature=LLM_SETTINGS["temperature"],
                top_p=LLM_SETTINGS["top_p"],
                timeout=settings.LLM_TIMEOUT,
            )
            # logger.debug(f"Full response: {response}")
            if hasattr(response, 'choices') and response.choices:
                return response.choices[0].message.content
            else:
                logger.error(f"LLM response did not contain expected 'choices' attribute or was empty. Full response: {response}")
                return None
        except Exception as e:
            logger.error(f"Error getting completion from LLM: {e}")
            return None

    async def process(self, raw_data: Dict[str, Any]) -> Any:
        # This method is part of the abstract base class, but the main logic
        # will be in a higher-level orchestrator that calls summarize_content
        # and summarize_comments separately.
        pass
