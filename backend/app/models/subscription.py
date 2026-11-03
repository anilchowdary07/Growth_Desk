from __future__ import annotations

"""Subscription and Plan models for SaaS licensing and limits."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Plan(Base):
    """SaaS subscription plan with entitlement limits and features."""

    __tablename__ = "plans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_monthly: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    price_yearly: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    limits: Mapped[dict] = mapped_column(
        JSON,
        default=lambda: {
            "max_workspaces": 1,
            "max_campaigns": 5,
            "max_social_accounts": 3,
            "max_monthly_posts": 100,
            "can_access_advanced_agents": False,
        },
        nullable=False,
    )
    features: Mapped[list] = mapped_column(
        JSON,
        default=lambda: [
            "basic_agents",
            "content_generation",
            "brand_brain",
        ],
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="plan", lazy="selectin"
    )


class Subscription(Base):
    """Active subscription linking an organisation to a plan."""

    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(50), default="active", nullable=False
    )  # trialing, active, past_due, cancelled, expired
    payment_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)  # razorpay, stripe
    external_subscription_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    current_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    trial_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    plan: Mapped["Plan"] = relationship("Plan", back_populates="subscriptions", lazy="selectin")

