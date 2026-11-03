from __future__ import annotations

"""Agents API — chat with Marketing Director and coordinate specialists."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import orchestrator
from app.core.database import get_db
from app.core.dependencies import get_current_workspace
from app.models.workspace import Workspace
from app.schemas.agent import AgentChatRequest, AgentChatResponse

router = APIRouter(prefix="/agents", tags=["AI Marketing Workforce"])


@router.post("/chat", response_model=AgentChatResponse)
async def chat_with_agent(
    data: AgentChatRequest,
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        result = await orchestrator.chat(
            db=db,
            workspace_id=workspace.id,
            user_message=data.message,
            conversation_history=data.conversation_history,
            target_agent=data.target_agent,
            campaign_context=data.campaign_context,
        )
        return AgentChatResponse(
            response=result.response,
            agent_name=result.agent_name,
            conversation_id=data.conversation_id,
            actions_taken=result.actions_taken,
            delegations=result.delegations,
            metadata=result.metadata,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent workforce error: {str(e)}")

