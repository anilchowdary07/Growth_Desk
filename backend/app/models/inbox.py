from __future__ import annotations

"""Unified inbox models – conversations and messages."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Conversation(Base):
    """A social media conversation thread (DM, comment, mention, etc.)."""

    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    social_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False
    )
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    platform_conversation_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_avatar_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    conversation_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # comment, dm, mention, review
    status: Mapped[str] = mapped_column(
        String(50), default="open", nullable=False
    )  # open, replied, resolved, spam, escalated
    sentiment: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # positive, neutral, negative
    priority: Mapped[str] = mapped_column(
        String(50), default="normal", nullable=False
    )  # low, normal, high, urgent
    classification: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # inquiry, complaint, purchase_intent, support, spam
    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="SET NULL"), nullable=True
    )
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    auto_reply_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", lazy="selectin"
    )
    social_account: Mapped["SocialAccount"] = relationship(  # noqa: F821
        "SocialAccount", lazy="selectin"
    )


class Message(Base):
    """An individual message within a conversation."""

    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False
    )
    direction: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # inbound, outbound
    sender_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # contact, user, ai
    sender_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    media_urls: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    platform_message_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ai_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="sent", nullable=False
    )  # draft, pending_approval, sent, delivered, failed

    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages", lazy="selectin"
    )
