from __future__ import annotations

"""Unified Inbox & Conversations schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    conversation_id: uuid.UUID
    direction: str  # inbound, outbound
    sender_type: str  # contact, user, ai
    sender_id: str | None
    body: str
    media_urls: list[str] | None
    is_ai_generated: bool
    status: str
    created_at: datetime


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    social_account_id: uuid.UUID
    platform: str
    contact_name: str | None
    contact_username: str | None
    contact_avatar_url: str | None
    conversation_type: str
    status: str
    sentiment: str | None
    priority: str
    classification: str | None
    lead_id: uuid.UUID | None
    assigned_to: uuid.UUID | None
    auto_reply_enabled: bool
    last_message_at: datetime | None
    created_at: datetime
    messages: list[MessageResponse] = []


class ReplyRequest(BaseModel):
    body: str = Field(min_length=1)
    status: str = "sent"


class SuggestReplyResponse(BaseModel):
    suggested_reply: str
    confidence: float
    sentiment: str
    intent_detected: str
    reasoning: str


class ConversationUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    classification: str | None = None
    auto_reply_enabled: bool | None = None
