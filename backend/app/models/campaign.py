from __future__ import annotations

"""Campaign and campaign task models."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Campaign(Base):
    """A marketing campaign orchestrated by AI agents."""

    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="draft", nullable=False
    )  # draft, planning, active, paused, completed, archived
    strategy: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    target_audience: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    budget: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    kpi_targets: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    results: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    tasks: Mapped[list["CampaignTask"]] = relationship(
        "CampaignTask", back_populates="campaign", lazy="selectin"
    )
    workspace: Mapped["Workspace"] = relationship("Workspace", lazy="selectin")  # noqa: F821
    creator: Mapped["User | None"] = relationship("User", lazy="selectin")  # noqa: F821


class CampaignTask(Base):
    """An individual task within a campaign, potentially handled by an AI agent."""

    __tablename__ = "campaign_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    task_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # content, creative, publish, research, approval
    status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )  # pending, in_progress, completed, failed, cancelled
    assigned_agent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    dependencies: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    campaign: Mapped["Campaign"] = relationship(
        "Campaign", back_populates="tasks", lazy="selectin"
    )
