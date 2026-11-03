from __future__ import annotations

"""Workspaces and Tenant management API."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User
from app.models.workspace import WorkspaceMember
from app.schemas.workspace import (
    InviteMember,
    WorkspaceCreate,
    WorkspaceMemberResponse,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from app.services.workspace_service import workspace_service

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.get("", response_model=list[WorkspaceResponse])
async def list_workspaces(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    workspaces = await workspace_service.get_user_workspaces(db, current_user.id)
    return [WorkspaceResponse.model_validate(w) for w in workspaces]


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    data: WorkspaceCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        workspace = await workspace_service.create_workspace(db, current_user, data)
        return WorkspaceResponse.model_validate(workspace)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    workspace = await workspace_service.get_workspace(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return WorkspaceResponse.model_validate(workspace)


@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: UUID,
    data: WorkspaceUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        workspace = await workspace_service.update_workspace(db, workspace_id, data)
        return WorkspaceResponse.model_validate(workspace)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMemberResponse])
async def list_members(
    workspace_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    members = await workspace_service.get_workspace_members(db, workspace_id)
    items = []
    for m in members:
        items.append(
            WorkspaceMemberResponse(
                id=m.id,
                workspace_id=m.workspace_id,
                user_id=m.user_id,
                role=m.role,
                created_at=m.created_at,
                user_email=m.user.email if m.user else None,
                user_name=m.user.full_name if m.user else None,
            )
        )
    return items


@router.post("/{workspace_id}/members", response_model=WorkspaceMemberResponse)
async def invite_member(
    workspace_id: UUID,
    data: InviteMember,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        member = await workspace_service.invite_member(db, workspace_id, data)
        return WorkspaceMemberResponse(
            id=member.id,
            workspace_id=member.workspace_id,
            user_id=member.user_id,
            role=member.role,
            created_at=member.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{workspace_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    workspace_id: UUID,
    member_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await workspace_service.remove_member(db, workspace_id, member_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
