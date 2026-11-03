from __future__ import annotations

"""AI Provider schemas — BYOK management."""

import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class AIProviderCreate(BaseModel):
    provider_type: Literal["openai", "anthropic", "gemini"]
    api_key: str = Field(min_length=5)
    display_name: str | None = None
    default_model: str | None = None
    is_default: bool = False


class AIProviderUpdate(BaseModel):
    api_key: str | None = None
    display_name: str | None = None
    default_model: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None


class AIProviderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    provider_type: str
    display_name: str
    is_active: bool
    is_default: bool
    default_model: str | None
    last_verified_at: datetime | None
    created_at: datetime
    # Note: NEVER expose api_key in responses!


class AIProviderTestResult(BaseModel):
    success: bool
    provider: str
    model: str | None = None
    message: str


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    context_window: int | None = None
    cost_tier: str = "$"
    supports_vision: bool = False
    supports_functions: bool = False
