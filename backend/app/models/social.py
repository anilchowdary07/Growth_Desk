from __future__ import annotations

"""Social account, scheduled post, and publish log models."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SocialAccount(Base):
    """A connected social media account for a workspace."""

    __tablename__ = "social_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    platform: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # instagram, facebook, youtube, linkedin, twitter, tiktok, pinterest
    platform_user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    encrypted_access_token: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    encrypted_refresh_token: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    scopes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", lazy="selectin")  # noqa: F821
    scheduled_posts: Mapped[list["ScheduledPost"]] = relationship(
        "ScheduledPost", back_populates="social_account", lazy="selectin"
    )


class ScheduledPost(Base):
    """A content item scheduled for publishing on a social account."""

    __tablename__ = "scheduled_posts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    content_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False
    )
    social_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50), default="scheduled", nullable=False
    )  # scheduled, publishing, published, failed, cancelled
    platform_post_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    social_account: Mapped["SocialAccount"] = relationship(
        "SocialAccount", back_populates="scheduled_posts", lazy="selectin"
    )
    content_item: Mapped["ContentItem"] = relationship(  # noqa: F821
        "ContentItem", lazy="selectin"
    )
    publish_logs: Mapped[list["PublishLog"]] = relationship(
        "PublishLog", back_populates="scheduled_post", lazy="selectin"
    )


class PublishLog(Base):
    """Audit trail entry for a scheduled post's publish lifecycle."""

    __tablename__ = "publish_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    scheduled_post_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scheduled_posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    action: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # attempted, published, failed, retried
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    scheduled_post: Mapped["ScheduledPost"] = relationship(
        "ScheduledPost", back_populates="publish_logs", lazy="selectin"
    )
