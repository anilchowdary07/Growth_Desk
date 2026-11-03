from __future__ import annotations

"""Content & Creative Studio schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ContentCreate(BaseModel):
    title: str = Field(min_length=2)
    content_type: str = "social_post"  # social_post, blog, caption, script, ad_copy, carousel, poster, thumbnail
    platform: str | None = None  # instagram, facebook, youtube, linkedin, twitter, tiktok, pinterest
    body: str | None = None
    campaign_id: uuid.UUID | None = None
    metadata_json: dict | None = None
    media_urls: list[str] | None = None


class ContentUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    status: str | None = None
    metadata_json: dict | None = None
    media_urls: list[str] | None = None


class ContentGenerateRequest(BaseModel):
    prompt: str = Field(min_length=5)
    content_type: str = "social_post"
    platform: str | None = None
    campaign_id: uuid.UUID | None = None
    count: int = 1  # Number of variations to generate
    additional_guidelines: str | None = None


class ContentVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content_id: uuid.UUID
    version_number: int
    body: str
    metadata_json: dict | None
    created_by: str
    created_at: datetime


class ContentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    campaign_id: uuid.UUID | None
    title: str
    content_type: str
    platform: str | None
    body: str | None
    metadata_json: dict | None
    media_urls: list[str] | None
    status: str
    ai_model_used: str | None
    created_by: uuid.UUID | None
    approved_by: uuid.UUID | None
    approved_at: datetime | None
    created_at: datetime
    updated_at: datetime
    versions: list[ContentVersionResponse] = []
