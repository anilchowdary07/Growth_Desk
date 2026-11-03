from __future__ import annotations

"""Content item and content version models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ContentItem(Base):
    """A piece of marketing content (post, blog, ad copy, etc.)."""

    __tablename__ = "content_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    campaign_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    content_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # social_post, blog, caption, script, ad_copy, carousel, poster, thumbnail
    platform: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # instagram, facebook, youtube, linkedin, twitter, tiktok, pinterest
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    media_urls: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="draft", nullable=False
    )  # draft, review, approved, published, rejected, archived
    ai_model_used: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    versions: Mapped[list["ContentVersion"]] = relationship(
        "ContentVersion", back_populates="content_item", lazy="selectin"
    )
    workspace: Mapped["Workspace"] = relationship("Workspace", lazy="selectin")  # noqa: F821
    campaign: Mapped["Campaign | None"] = relationship("Campaign", lazy="selectin")  # noqa: F821


class ContentVersion(Base):
    """Immutable snapshot of a content item's body at a point in time."""

    __tablename__ = "content_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    content_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_by: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # "ai" or user UUID

    # Relationships
    content_item: Mapped["ContentItem"] = relationship(
        "ContentItem", back_populates="versions", lazy="selectin"
    )
