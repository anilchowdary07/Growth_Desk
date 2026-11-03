"""Base agent class and shared data structures."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from app.providers.base import AIMessage

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


@dataclass
class AgentContext:
    """Contextual information passed to every agent invocation."""

    workspace_id: str
    brand_context: str  # Compiled brand profile, voice, documents summary
    user_message: str
    conversation_history: list[dict] = field(default_factory=list)
    campaign_context: dict | None = None
    additional_context: dict | None = None


@dataclass
class AgentResult:
    """Structured result returned by an agent after execution."""

    response: str
    agent_name: str
    actions_taken: list[dict] = field(default_factory=list)
    delegations: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all specialist AI agents.

    Subclasses must define ``name``, ``description``, ``system_prompt``
    class attributes and implement :meth:`execute`.
    """

    name: str
    description: str
    system_prompt: str

    @abstractmethod
    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        """Execute the agent's task using the given context and AI provider.

        Args:
            context: The conversation and workspace context.
            provider: The configured AI provider to use.

        Returns:
            AgentResult with the generated response, actions, and metadata.
        """
        ...

    def build_messages(self, context: AgentContext) -> list[AIMessage]:
        """Build the ordered message list for the AI provider.

        Order:
        1. System prompt
        2. Brand context (as system message)
        3. Conversation history
        4. Current user message
        """
        messages: list[AIMessage] = [AIMessage(role="system", content=self.system_prompt)]

        if context.brand_context:
            messages.append(
                AIMessage(role="system", content=f"Brand Context:\n{context.brand_context}")
            )

        if context.campaign_context:
            import json

            messages.append(
                AIMessage(
                    role="system",
                    content=f"Current Campaign Context:\n{json.dumps(context.campaign_context, indent=2)}",
                )
            )

        if context.additional_context:
            import json

            messages.append(
                AIMessage(
                    role="system",
                    content=f"Additional Context:\n{json.dumps(context.additional_context, indent=2)}",
                )
            )

        for msg in context.conversation_history:
            messages.append(AIMessage(role=msg["role"], content=msg["content"]))

        messages.append(AIMessage(role="user", content=context.user_message))
        return messages

    async def _call_provider(self, context: AgentContext, provider: "BaseAIProvider", **kwargs) -> str:
        """Helper to call the provider with built messages and return content."""
        messages = self.build_messages(context)
        response = await provider.chat(messages, **kwargs)
        return response.content
