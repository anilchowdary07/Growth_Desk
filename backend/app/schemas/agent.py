from __future__ import annotations

"""Agent chat schemas."""

from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    target_agent: str = "director"
    conversation_history: list[dict] | None = None
    campaign_context: dict | None = None


class AgentChatResponse(BaseModel):
    response: str
    agent_name: str
    conversation_id: str | None = None
    actions_taken: list[dict] = []
    delegations: list[dict] = []
    metadata: dict = {}

