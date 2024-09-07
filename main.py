from fastapi import FastAPI

from api import router as api_router
from logging_config import logger
from middleware import setup_middleware, setup_exception_handlers, setup_event_handlers

app = FastAPI(
    title="Audio Separation API",
    description="API for separating audio into stems using Spleeter.",
    version="0.1.0"
)

try:
    setup_middleware(app)
    logger.info("Middleware setup completed successfully.", emoji="✅")
except Exception as e:
    logger.error(f"Error setting up middleware: {e}", emoji="❌")

try:
    setup_exception_handlers(app)
    logger.info("Exception handlers setup completed successfully.", emoji="✅")
except Exception as e:
    logger.error(f"Error setting up exception handlers: {e}", emoji="❌")

try:
    setup_event_handlers(app)
    logger.info("Event handlers setup completed successfully.", emoji="✅")
except Exception as e:
    logger.error(f"Error setting up event handlers: {e}", emoji="❌")

try:
    app.include_router(api_router)
    logger.info("Routes from api.py included successfully.", emoji="✅")
except Exception as e:
    logger.error(f"Error including routes from api.py: {e}", emoji="❌")