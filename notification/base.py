from abc import ABC, abstractmethod


class Notifier(ABC):
    """
    Abstract base class for notifiers.
    """

    @abstractmethod
    async def send_notification(self, message: str, status: str) -> bool:
        """
        Send a notification.
        """
        pass