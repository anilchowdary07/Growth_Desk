from __future__ import annotations

"""Campaign schemas."""

import uuid
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class CampaignCreate(BaseModel):
    title: str = Field(min_length=2)
    objective: str = Field(min_length=5)
    description: str | None = None
    target_audience: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    budget: float | None = None
    kpi_targets: dict | None = None


class CampaignUpdate(BaseModel):
    title: str | None = None
    objective: str | None = None
    description: str | None = None
    status: str | None = None
    strategy: dict | None = None
    target_audience: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    budget: float | None = None
    kpi_targets: dict | None = None
    results: dict | None = None


class CampaignTaskCreate(BaseModel):
    title: str = Field(min_length=2)
    description: str | None = None
    task_type: str = "content"
    assigned_agent: str | None = None
    due_date: date | None = None


class CampaignTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    assigned_agent: str | None = None
    result: dict | None = None
    due_date: date | None = None


class CampaignTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    campaign_id: uuid.UUID
    title: str
    description: str | None
    task_type: str
    status: str
    assigned_agent: str | None
    result: dict | None
    due_date: date | None
    completed_at: datetime | None
    created_at: datetime


class CampaignResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    title: str
    description: str | None
    objective: str
    status: str
    strategy: dict | None
    target_audience: str | None
    start_date: date | None
    end_date: date | None
    budget: float | None
    kpi_targets: dict | None
    results: dict | None
    created_by: uuid.UUID
    tasks: list[CampaignTaskResponse] = []
    created_at: datetime
    updated_at: datetime

