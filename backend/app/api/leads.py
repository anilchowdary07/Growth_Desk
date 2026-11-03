from __future__ import annotations

"""Lead Generation & CRM API."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_workspace
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.common import StatusResponse
from app.schemas.lead import (
    LeadActivityCreate,
    LeadActivityResponse,
    LeadCreate,
    LeadResponse,
    LeadUpdate,
)
from app.services.lead_service import lead_service

router = APIRouter(prefix="/leads", tags=["Leads & CRM"])


@router.get("", response_model=list[LeadResponse])
async def list_leads(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status: str | None = Query(None),
    source: str | None = Query(None),
):
    leads = await lead_service.get_leads(db, workspace.id, status, source)
    return [LeadResponse.model_validate(l) for l in leads]


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    data: LeadCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    lead = await lead_service.create_lead(db, workspace.id, data)
    return LeadResponse.model_validate(lead)


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    lead = await lead_service.get_lead(db, workspace.id, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadResponse.model_validate(lead)


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: UUID,
    data: LeadUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        lead = await lead_service.update_lead(db, workspace.id, lead_id, data)
        return LeadResponse.model_validate(lead)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{lead_id}/activity", response_model=LeadActivityResponse)
async def add_activity(
    lead_id: UUID,
    data: LeadActivityCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        act = await lead_service.add_activity(db, workspace.id, lead_id, data, current_user.full_name)
        return LeadActivityResponse.model_validate(act)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{lead_id}", response_model=StatusResponse)
async def delete_lead(
    lead_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await lead_service.delete_lead(db, workspace.id, lead_id)
        return StatusResponse(message="Lead deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
