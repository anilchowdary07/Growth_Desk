from __future__ import annotations

"""AI Provider management API (BYOK)."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_workspace
from app.models.workspace import Workspace
from app.schemas.ai_provider import (
    AIProviderCreate,
    AIProviderResponse,
    AIProviderTestResult,
    AIProviderUpdate,
    ModelInfo,
)
from app.schemas.common import StatusResponse
from app.services.ai_provider_service import ai_provider_service

router = APIRouter(prefix="/ai-providers", tags=["AI Providers (BYOK)"])


@router.get("", response_model=list[AIProviderResponse])
async def list_providers(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    providers = await ai_provider_service.get_providers(db, workspace.id)
    return [AIProviderResponse.model_validate(p) for p in providers]


@router.post("", response_model=AIProviderResponse, status_code=status.HTTP_201_CREATED)
async def add_provider(
    data: AIProviderCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    provider = await ai_provider_service.add_provider(db, workspace.id, data)
    return AIProviderResponse.model_validate(provider)


@router.put("/{provider_id}", response_model=AIProviderResponse)
async def update_provider(
    provider_id: UUID,
    data: AIProviderUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        provider = await ai_provider_service.update_provider(db, workspace.id, provider_id, data)
        return AIProviderResponse.model_validate(provider)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{provider_id}", response_model=StatusResponse)
async def delete_provider(
    provider_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await ai_provider_service.delete_provider(db, workspace.id, provider_id)
        return StatusResponse(message="Provider deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{provider_id}/test", response_model=AIProviderTestResult)
async def test_provider(
    provider_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await ai_provider_service.test_provider(db, workspace.id, provider_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/models", response_model=list[ModelInfo])
async def list_models():
    return ai_provider_service.get_supported_models()
