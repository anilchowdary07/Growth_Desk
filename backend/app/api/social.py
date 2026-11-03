from __future__ import annotations

"""Social Media & Calendar publishing API."""

from datetime import datetime
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_workspace
from app.models.workspace import Workspace
from app.schemas.common import StatusResponse
from app.schemas.social import (
    SchedulePostRequest,
    ScheduledPostResponse,
    ScheduledPostUpdate,
    SocialAccountConnect,
    SocialAccountResponse,
)
from app.services.social_service import social_service

router = APIRouter(prefix="/social", tags=["Social Media & Calendar"])


@router.get("/accounts", response_model=list[SocialAccountResponse])
async def list_accounts(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    accounts = await social_service.get_accounts(db, workspace.id)
    return [SocialAccountResponse.model_validate(a) for a in accounts]


@router.post("/accounts", response_model=SocialAccountResponse, status_code=status.HTTP_201_CREATED)
async def connect_account(
    data: SocialAccountConnect,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    account = await social_service.connect_account(db, workspace.id, data)
    return SocialAccountResponse.model_validate(account)


@router.delete("/accounts/{account_id}", response_model=StatusResponse)
async def disconnect_account(
    account_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await social_service.disconnect_account(db, workspace.id, account_id)
        return StatusResponse(message="Account disconnected successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/calendar", response_model=list[ScheduledPostResponse])
async def get_calendar(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
):
    posts = await social_service.get_scheduled_posts(db, workspace.id, start_date, end_date)
    return [ScheduledPostResponse.model_validate(p) for p in posts]


@router.post("/schedule", response_model=ScheduledPostResponse, status_code=status.HTTP_201_CREATED)
async def schedule_post(
    data: SchedulePostRequest,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        post = await social_service.schedule_post(db, workspace.id, data)
        return ScheduledPostResponse.model_validate(post)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/schedule/{post_id}", response_model=ScheduledPostResponse)
async def update_scheduled_post(
    post_id: UUID,
    data: ScheduledPostUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        post = await social_service.update_scheduled_post(db, workspace.id, post_id, data)
        return ScheduledPostResponse.model_validate(post)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/schedule/{post_id}", response_model=StatusResponse)
async def cancel_scheduled_post(
    post_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await social_service.cancel_scheduled_post(db, workspace.id, post_id)
        return StatusResponse(message="Post scheduled status cancelled")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
