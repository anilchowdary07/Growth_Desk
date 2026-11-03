from __future__ import annotations

"""Brand Brain schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BrandProfileCreate(BaseModel):
    company_name: str = Field(min_length=2)
    industry: str | None = None
    description: str | None = None
    target_audience: str | None = None
    brand_voice: str | None = None
    tone_keywords: list[str] | None = None
    brand_colors: dict | None = None
    logo_url: str | None = None
    website: str | None = None
    products_services: str | None = None
    competitors: list[str] | None = None
    restricted_topics: list[str] | None = None
    content_preferences: dict | None = None
    faqs: list[dict] | None = None


class BrandProfileUpdate(BaseModel):
    company_name: str | None = None
    industry: str | None = None
    description: str | None = None
    target_audience: str | None = None
    brand_voice: str | None = None
    tone_keywords: list[str] | None = None
    brand_colors: dict | None = None
    logo_url: str | None = None
    website: str | None = None
    products_services: str | None = None
    competitors: list[str] | None = None
    restricted_topics: list[str] | None = None
    content_preferences: dict | None = None
    faqs: list[dict] | None = None


class BrandProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    company_name: str
    industry: str | None
    description: str | None
    target_audience: str | None
    brand_voice: str | None
    tone_keywords: list[str] | None
    brand_colors: dict | None
    logo_url: str | None
    website: str | None
    products_services: str | None
    competitors: list[str] | None
    restricted_topics: list[str] | None
    content_preferences: dict | None
    faqs: list[dict] | None
    created_at: datetime
    updated_at: datetime


class BrandDocumentCreate(BaseModel):
    title: str = Field(min_length=2)
    content: str = Field(min_length=10)
    doc_type: str = "text"
    metadata_json: dict | None = None


class BrandDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    title: str
    file_url: str | None
    content: str | None
    doc_type: str
    is_processed: bool
    created_at: datetime


class BrandQueryRequest(BaseModel):
    query: str = Field(min_length=2)
    limit: int = 5


class BrandQueryResponse(BaseModel):
    query: str
    context: str
    relevant_documents: list[dict]
