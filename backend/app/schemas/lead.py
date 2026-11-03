from __future__ import annotations

"""Lead Generation & CRM schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LeadCreate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    source: str = "manual"  # instagram, facebook, website, manual, inbox
    source_conversation_id: uuid.UUID | None = None
    status: str = "new"  # new, contacted, qualified, converted, lost
    score: int | None = 50
    tags: list[str] | None = None
    notes: str | None = None
    custom_fields: dict | None = None


class LeadUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    status: str | None = None
    score: int | None = None
    tags: list[str] | None = None
    notes: str | None = None
    custom_fields: dict | None = None
    assigned_to: uuid.UUID | None = None


class LeadActivityCreate(BaseModel):
    activity_type: str = "note_added"
    description: str = Field(min_length=2)
    metadata_json: dict | None = None


class LeadActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    lead_id: uuid.UUID
    activity_type: str
    description: str
    metadata_json: dict | None
    performed_by: str
    created_at: datetime


class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    name: str | None
    email: str | None
    phone: str | None
    company: str | None
    source: str | None
    status: str
    score: int | None
    tags: list[str] | None
    notes: str | None
    custom_fields: dict | None
    assigned_to: uuid.UUID | None
    converted_at: datetime | None
    created_at: datetime
    updated_at: datetime
    activities: list[LeadActivityResponse] = []

