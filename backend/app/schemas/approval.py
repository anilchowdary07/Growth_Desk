from __future__ import annotations

"""Approval schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ApprovalCreate(BaseModel):
    item_type: str  # content, campaign, reply, ad, scheduled_post
    item_id: uuid.UUID
    title: str = Field(min_length=2)
    description: str | None = None
    meta_data: dict | None = None
    expires_at: datetime | None = None


class ApprovalAction(BaseModel):
    note: str | None = None


class ApprovalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    item_type: str
    item_id: uuid.UUID
    title: str
    description: str | None
    status: str
    requested_by: str
    reviewed_by: uuid.UUID | None
    reviewed_at: datetime | None
    review_note: str | None
    meta_data: dict | None
    expires_at: datetime | None
    created_at: datetime

