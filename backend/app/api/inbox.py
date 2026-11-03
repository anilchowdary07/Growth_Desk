from __future__ import annotations

"""Unified Inbox & Social Conversations API."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_workspace
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.inbox import (
    ConversationResponse,
    ConversationUpdate,
    MessageResponse,
    ReplyRequest,
    SuggestReplyResponse,
)
from app.schemas.lead import LeadResponse
from app.services.inbox_service import inbox_service

router = APIRouter(prefix="/inbox", tags=["Unified Inbox"])


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
    status: str | None = Query(None),
    platform: str | None = Query(None),
    priority: str | None = Query(None),
):
    convs = await inbox_service.get_conversations(db, workspace.id, status, platform, priority)
    return [ConversationResponse.model_validate(c) for c in convs]


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    conv = await inbox_service.get_conversation(db, workspace.id, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse.model_validate(conv)


@router.post("/conversations/{conversation_id}/reply", response_model=MessageResponse)
async def reply(
    conversation_id: UUID,
    data: ReplyRequest,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        msg = await inbox_service.reply(db, workspace.id, conversation_id, current_user.id, data)
        return MessageResponse.model_validate(msg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/conversations/{conversation_id}/suggest-reply", response_model=SuggestReplyResponse)
async def suggest_reply(
    conversation_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await inbox_service.suggest_reply(db, workspace.id, conversation_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: UUID,
    data: ConversationUpdate,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        conv = await inbox_service.update_conversation(db, workspace.id, conversation_id, data)
        return ConversationResponse.model_validate(conv)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/conversations/{conversation_id}/create-lead", response_model=LeadResponse)
async def create_lead_from_conversation(
    conversation_id: UUID,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        lead = await inbox_service.create_lead_from_conversation(db, workspace.id, conversation_id)
        return LeadResponse.model_validate(lead)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

