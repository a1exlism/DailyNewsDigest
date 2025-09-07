import logging
from logging.handlers import RotatingFileHandler
from config.settings import settings


# Configure log format
LOG_FORMAT = '[%(levelname)5s] - %(filename)s:%(lineno)d - %(message)s'
LOG_FORMAT_EX = '[%(levelname)5s] %(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(message)s'


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with configured handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the lowest level to capture all messages

    # Avoid adding handlers multiple times
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.getLevelName(settings.LOG_LEVEL))  # Configurable log level
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

        # File handler (optional, e.g., daily rotation or size-based rotation)
        file_handler = RotatingFileHandler(
            'app.log',
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)  # Log DEBUG level and above to file
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

    return logger
