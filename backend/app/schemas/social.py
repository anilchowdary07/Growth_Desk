from __future__ import annotations

"""Social Media & Calendar schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class SocialAccountConnect(BaseModel):
    platform: str
    access_token: str
    refresh_token: str | None = None
    username: str | None = None
    display_name: str | None = None
    avatar_url: str | None = None


class SocialAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    platform: str
    platform_user_id: str | None
    username: str | None
    display_name: str | None
    avatar_url: str | None
    is_active: bool
    last_synced_at: datetime | None
    created_at: datetime


class SchedulePostRequest(BaseModel):
    content_id: uuid.UUID
    social_account_id: uuid.UUID
    scheduled_at: datetime


class ScheduledPostUpdate(BaseModel):
    scheduled_at: datetime | None = None
    status: str | None = None


class ScheduledPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    content_id: uuid.UUID
    social_account_id: uuid.UUID
    scheduled_at: datetime
    published_at: datetime | None
    status: str
    platform_post_id: str | None
    error_message: str | None
    retry_count: int
    created_at: datetime
    content_title: str | None = None
    platform: str | None = None
