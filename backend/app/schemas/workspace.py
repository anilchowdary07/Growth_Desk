from __future__ import annotations

"""Workspace and Organization schemas."""

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OrgCreate(BaseModel):
    name: str = Field(min_length=2)


class OrgResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    owner_id: uuid.UUID
    subscription_plan: str
    subscription_status: str
    subscription_expires_at: datetime | None
    max_workspaces: int
    created_at: datetime


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str | None = None


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    org_id: uuid.UUID
    name: str
    slug: str
    description: str | None
    is_active: bool
    created_at: datetime


class WorkspaceMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workspace_id: uuid.UUID
    user_id: uuid.UUID
    role: str
    created_at: datetime
    user_email: str | None = None
    user_name: str | None = None


class InviteMember(BaseModel):
    email: EmailStr
    role: str = "editor"  # owner, admin, editor, viewer
