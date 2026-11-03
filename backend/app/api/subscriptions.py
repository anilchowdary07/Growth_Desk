from __future__ import annotations

"""SaaS Subscriptions and Plans API."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_workspace
from app.models.workspace import Workspace
from app.schemas.subscription import PlanResponse, SubscriptionResponse, UpgradeRequest
from app.services.subscription_service import subscription_service

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions & Licensing"])


@router.get("/plans", response_model=list[PlanResponse])
async def list_plans(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    plans = await subscription_service.get_plans(db)
    return [PlanResponse.model_validate(p) for p in plans]


@router.get("/current", response_model=SubscriptionResponse)
async def get_current_subscription(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    sub = await subscription_service.get_current_subscription(db, workspace.org_id)
    return SubscriptionResponse.model_validate(sub)


@router.post("/upgrade", response_model=SubscriptionResponse)
async def upgrade_plan(
    data: UpgradeRequest,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        sub = await subscription_service.upgrade_plan(db, workspace.org_id, data.plan_name)
        return SubscriptionResponse.model_validate(sub)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

