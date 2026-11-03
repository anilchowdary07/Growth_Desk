from __future__ import annotations

"""Human Approval Center API."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_workspace
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.approval import ApprovalAction, ApprovalResponse
from app.services.approval_service import approval_service

router = APIRouter(prefix="/approvals", tags=["Human Approval Center"])


@router.get("", response_model=list[ApprovalResponse])
async def list_approvals(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status: str = Query("pending"),
):
    approvals = await approval_service.get_approvals(db, workspace.id, status)
    return [ApprovalResponse.model_validate(a) for a in approvals]


@router.post("/{approval_id}/approve", response_model=ApprovalResponse)
async def approve_item(
    approval_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    action: ApprovalAction | None = None,
):
    try:
        appr = await approval_service.approve_item(
            db, workspace.id, approval_id, current_user.id, action
        )
        return ApprovalResponse.model_validate(appr)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{approval_id}/reject", response_model=ApprovalResponse)
async def reject_item(
    approval_id: UUID,
    action: ApprovalAction,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        appr = await approval_service.reject_item(
            db, workspace.id, approval_id, current_user.id, action
        )
        return ApprovalResponse.model_validate(appr)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
