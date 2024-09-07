import sys
from functools import wraps

from loguru import logger

# Remove default logger to avoid duplicate logs
logger.remove()

# Define emojis for different log levels
level_emojis = {
    "DEBUG": "🐛",
    "INFO": "ℹ️",
    "SUCCESS": "✅",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "🔥"
}

# Add custom logger with formatting and emojis for all levels
logger.add(
    sys.stdout,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level> {extra[emoji]}"
    ),
    level="DEBUG",
    colorize=True,
    backtrace=True,
    diagnose=True,
    filter=lambda record: record["extra"].update(emoji=level_emojis.get(record["level"].name, ""))
)

# Add file logger with rotation and retention
logger.add(
    "logs/app.log",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - "
        "{message} {extra[emoji]}"
    ),
    level="DEBUG",  # Log everything from DEBUG level upwards
    rotation="10 MB",  # Rotate after 10 MB
    retention="10 days",  # Keep logs for 10 days
    compression="zip",  # Compress logs
    backtrace=True,
    diagnose=True,
    filter=lambda record: record["extra"].update(emoji=level_emojis.get(record["level"].name, ""))
)


def log_decorator(level="INFO"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, f"Entering {func.__name__}()")
            try:
                result = func(*args, **kwargs)
                logger.log(level, f"Exiting {func.__name__}()")
                return result
            except Exception as e:
                logger.exception(f"Exception in {func.__name__}(): {e}")
                raise

        return wrapper

    return decorator
