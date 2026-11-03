from __future__ import annotations

"""Brand Brain API — Profile & Knowledge Base."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_workspace
from app.models.workspace import Workspace
from app.schemas.brand import (
    BrandDocumentCreate,
    BrandDocumentResponse,
    BrandProfileCreate,
    BrandProfileResponse,
    BrandProfileUpdate,
    BrandQueryRequest,
    BrandQueryResponse,
)
from app.schemas.common import StatusResponse
from app.services.brand_service import brand_service

router = APIRouter(prefix="/brand", tags=["Brand Brain"])


@router.get("/profile", response_model=BrandProfileResponse | None)
async def get_brand_profile(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    profile = await brand_service.get_profile(db, workspace.id)
    if not profile:
        return None
    return BrandProfileResponse.model_validate(profile)


@router.post("/profile", response_model=BrandProfileResponse)
async def create_or_update_profile(
    data: BrandProfileCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    profile = await brand_service.create_or_update_profile(db, workspace.id, data)
    return BrandProfileResponse.model_validate(profile)


@router.put("/profile", response_model=BrandProfileResponse)
async def update_profile(
    data: BrandProfileUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    profile = await brand_service.create_or_update_profile(db, workspace.id, data)
    return BrandProfileResponse.model_validate(profile)


@router.get("/documents", response_model=list[BrandDocumentResponse])
async def list_documents(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    docs = await brand_service.get_documents(db, workspace.id)
    return [BrandDocumentResponse.model_validate(d) for d in docs]


@router.post("/documents", response_model=BrandDocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    data: BrandDocumentCreate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    doc = await brand_service.add_document(db, workspace.id, data)
    return BrandDocumentResponse.model_validate(doc)


@router.delete("/documents/{doc_id}", response_model=StatusResponse)
async def delete_document(
    doc_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        await brand_service.delete_document(db, workspace.id, doc_id)
        return StatusResponse(message="Document deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/query", response_model=BrandQueryResponse)
async def query_knowledge_base(
    data: BrandQueryRequest,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await brand_service.query_knowledge_base(db, workspace.id, data.query, data.limit)
