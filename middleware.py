# middleware.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from logging_config import logger


# Middleware setup
def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Custom exception handler for HTTP exceptions
def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: RequestValidationError, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {exc}", emoji="❌")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )


# Event handlers
def setup_event_handlers(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up the application...", emoji="✅")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down the application...", emoji="⚠️")
