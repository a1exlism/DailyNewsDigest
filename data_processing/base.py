from abc import ABC, abstractmethod
from typing import List, Dict, Any

from data_output.schemas import DailyDigest


class Processor(ABC):
    """
    Abstract base class for data processors.
    """
    @abstractmethod
    async def process(self, raw_data: Dict[str, Any]) -> DailyDigest:
        """
        Process raw data and return a DailyDigest object.
        """
        pass

    @abstractmethod
    async def summarize_content(self, content: str) -> str:
        """
        Summarize content using an LLM.
        """
        pass

    @abstractmethod
    async def summarize_comments(self, comments: List[Dict[str, Any]]) -> str:
        """
        Summarize comments using an LLM.
        """
        pass