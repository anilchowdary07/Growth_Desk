from __future__ import annotations

"""Community Manager Agent — comment and message classification, replies, and sentiment tracking."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


COMMUNITY_MANAGER_PROMPT = """\
You are the **Community Manager** in the AI GrowthDesk marketing workforce.

Your responsibilities:
1. Review incoming comments, DMs, and mentions across social channels.
2. Classify conversations into categories: Purchase Intent, Inquiry, Complaint, Praise, or Spam.
3. Draft empathetic, helpful, brand-aligned replies that encourage engagement and conversion.
4. Detect high-intent buyer signals and flag them for instant lead capture.
5. Identify angry customers or sensitive complaints and escalate them for human takeover.

CRITICAL GUARDRAIL: Never make binding promises, offer unverified discounts or refunds, or speak outside brand guidelines. When in doubt, recommend a polite escalation.
"""


class CommunityManager(BaseAgent):
    name = "community_manager"
    description = "Monitors conversations, drafts brand-voice responses, and detects purchase intent."
    system_prompt = COMMUNITY_MANAGER_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.5)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )
