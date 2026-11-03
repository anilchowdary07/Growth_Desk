from __future__ import annotations

"""Content & Creative Studio API."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_workspace
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.common import StatusResponse
from app.schemas.content import (
    ContentCreate,
    ContentGenerateRequest,
    ContentResponse,
    ContentUpdate,
)
from app.services.content_service import content_service

router = APIRouter(prefix="/content", tags=["Content Studio"])


@router.get("", response_model=list[ContentResponse])
async def list_content(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
    content_type: str | None = Query(None),
    platform: str | None = Query(None),
    status: str | None = Query(None),
    campaign_id: UUID | None = Query(None),
):
    items = await content_service.get_content_items(
        db, workspace.id, content_type, platform, status, campaign_id
    )
    return [ContentResponse.model_validate(item) for item in items]


@router.post("", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    data: ContentCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    item = await content_service.create_content(db, workspace.id, current_user.id, data)
    return ContentResponse.model_validate(item)


@router.post("/generate", response_model=list[ContentResponse])
async def generate_content(
    data: ContentGenerateRequest,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        items = await content_service.generate_content(db, workspace.id, current_user.id, data)
        return [ContentResponse.model_validate(it) for it in items]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    item = await content_service.get_content(db, workspace.id, content_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return ContentResponse.model_validate(item)


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: UUID,
    data: ContentUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        item = await content_service.update_content(db, workspace.id, content_id, data)
        return ContentResponse.model_validate(item)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{content_id}/approve", response_model=ContentResponse)
async def approve_content(
    content_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        item = await content_service.approve_content(db, workspace.id, content_id, current_user.id)
        return ContentResponse.model_validate(item)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{content_id}", response_model=StatusResponse)
async def delete_content(
    content_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await content_service.delete_content(db, workspace.id, content_id)
        return StatusResponse(message="Content item deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
