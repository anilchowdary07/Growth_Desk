from __future__ import annotations

"""Async SQLAlchemy database engine, session factory, and declarative base."""

import uuid
from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import get_settings

# ---------------------------------------------------------------------------
# Engine & session – initialised lazily via ``init_engine()``
# ---------------------------------------------------------------------------

_engine = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    """Declarative base with common columns shared by every table."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def init_engine() -> None:
    """Create the async engine and session factory.

    Call once during application startup (e.g. in the lifespan handler).
    """
    global _engine, _async_session_factory  # noqa: PLW0603

    settings = get_settings()
    _engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
    )
    _async_session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def dispose_engine() -> None:
    """Dispose the async engine – call on shutdown."""
    global _engine  # noqa: PLW0603
    if _engine is not None:
        await _engine.dispose()
        _engine = None


def get_engine():
    """Return the current async engine (or ``None`` if not initialised)."""
    return _engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an ``AsyncSession`` and auto-closes it."""
    if _async_session_factory is None:
        raise RuntimeError("Database engine not initialised. Call init_engine() first.")
    async with _async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
