from abc import ABC, abstractmethod

from data_output.schemas import DailyDigest


class Publisher(ABC):
    """

    Abstract base class for publishers.
    """
    @abstractmethod
    async def publish(self, digest: DailyDigest) -> bool:
        """
        Publish a DailyDigest object.
        """
        pass
