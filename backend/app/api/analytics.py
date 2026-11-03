from __future__ import annotations

"""Analytics API."""

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_workspace
from app.models.workspace import Workspace
from app.schemas.analytics import OverviewAnalytics
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=OverviewAnalytics)
async def get_overview(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await analytics_service.get_overview(db, workspace.id)

