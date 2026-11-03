from __future__ import annotations

"""AI provider model – stores encrypted API keys for LLM providers."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AIProvider(Base):
    """An AI provider configuration scoped to a workspace."""

    __tablename__ = "ai_providers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    provider_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # openai, anthropic, gemini
    encrypted_api_key: Mapped[str] = mapped_column(String(2048), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    default_model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    base_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    last_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    workspace: Mapped["Workspace"] = relationship(  # noqa: F821
        "Workspace", lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint(
            "workspace_id", "provider_type", name="uq_workspace_provider"
        ),
    )
