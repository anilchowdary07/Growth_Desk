from __future__ import annotations

"""Lead and lead activity models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Lead(Base):
    """A potential customer captured from social or manual input."""

    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # instagram, facebook, website, manual
    source_conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50), default="new", nullable=False
    )  # new, contacted, qualified, converted, lost
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 0-100
    tags: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    custom_fields: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    converted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    activities: Mapped[list["LeadActivity"]] = relationship(
        "LeadActivity", back_populates="lead", lazy="selectin"
    )
    workspace: Mapped["Workspace"] = relationship("Workspace", lazy="selectin")  # noqa: F821


class LeadActivity(Base):
    """An activity log entry for a lead."""

    __tablename__ = "lead_activities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False
    )
    activity_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # created, contacted, note_added, status_changed, conversation, email_sent
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    performed_by: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # user UUID or "ai"

    # Relationships
    lead: Mapped["Lead"] = relationship(
        "Lead", back_populates="activities", lazy="selectin"
    )
