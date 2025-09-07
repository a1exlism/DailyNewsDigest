from telegram import Bot
from telegram.ext import Updater

from config.settings import settings
from notification.base import Notifier
from utils.logger import get_logger

logger = get_logger(__name__)


class TelegramNotifier(Notifier):
    """Notifier for Telegram."""

    def __init__(self, chat_id: str):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.chat_id = chat_id

    async def send_notification(self, message: str, status: str) -> bool:
        logger.debug(f"Attempting to send {status} notification to Telegram with message: {message}")
        """Send a notification to Telegram."""
        try:
            full_message = f"[{status.upper()}] {message}"
            await self.bot.send_message(chat_id=self.chat_id, text=full_message)
            logger.info("Successfully sent notification to Telegram.")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification to Telegram: {e}")
            return False
