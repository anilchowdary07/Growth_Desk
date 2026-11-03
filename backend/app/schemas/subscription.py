from __future__ import annotations

"""Subscription & Licensing schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    display_name: str
    description: str | None
    price_monthly: float
    price_yearly: float
    limits: dict
    features: list
    is_active: bool
    sort_order: int


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    org_id: uuid.UUID
    plan_id: uuid.UUID
    status: str
    payment_provider: str | None
    current_period_start: datetime | None
    current_period_end: datetime | None
    trial_ends_at: datetime | None
    plan: PlanResponse


class UpgradeRequest(BaseModel):
    plan_name: str  # starter, professional, agency
    billing_period: str = "monthly"  # monthly, yearly
