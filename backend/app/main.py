from __future__ import annotations

"""FastAPI Application entry point for AI GrowthDesk."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import all_routers
from app.core.config import get_settings
from app.core.database import dispose_engine, init_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("growthdesk")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize database engine and background services."""
    logger.info("Starting up AI GrowthDesk API...")
    init_engine()
    yield
    logger.info("Shutting down AI GrowthDesk API...")
    await dispose_engine()


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Autonomous AI Marketing Workforce Platform — BYOK Multi-Tenant SaaS",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for container probes and load balancers."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "0.1.0",
    }


# Include all modular API routers under the /api/v1 prefix
for router in all_routers:
    app.include_router(router, prefix=settings.API_V1_PREFIX)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Our team has been notified."},
    )

