from __future__ import annotations

"""Campaigns API — autonomous planning and execution."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_workspace
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.campaign import (
    CampaignCreate,
    CampaignResponse,
    CampaignTaskCreate,
    CampaignTaskResponse,
    CampaignTaskUpdate,
    CampaignUpdate,
)
from app.services.campaign_service import campaign_service

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get("", response_model=list[CampaignResponse])
async def list_campaigns(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status: str | None = Query(None),
):
    campaigns = await campaign_service.get_campaigns(db, workspace.id, status)
    return [CampaignResponse.model_validate(c) for c in campaigns]


@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    data: CampaignCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    campaign = await campaign_service.create_campaign(db, workspace.id, current_user.id, data)
    return CampaignResponse.model_validate(campaign)


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    campaign = await campaign_service.get_campaign(db, workspace.id, campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return CampaignResponse.model_validate(campaign)


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: UUID,
    data: CampaignUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        campaign = await campaign_service.update_campaign(db, workspace.id, campaign_id, data)
        return CampaignResponse.model_validate(campaign)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{campaign_id}/plan", response_model=CampaignResponse)
async def generate_campaign_plan(
    campaign_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        campaign = await campaign_service.generate_campaign_plan(db, workspace.id, campaign_id)
        return CampaignResponse.model_validate(campaign)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{campaign_id}/tasks", response_model=CampaignTaskResponse)
async def add_task(
    campaign_id: UUID,
    data: CampaignTaskCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    task = await campaign_service.add_task(db, campaign_id, data)
    return CampaignTaskResponse.model_validate(task)


@router.put("/tasks/{task_id}", response_model=CampaignTaskResponse)
async def update_task(
    task_id: UUID,
    data: CampaignTaskUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        task = await campaign_service.update_task(db, task_id, data)
        return CampaignTaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
