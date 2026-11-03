from __future__ import annotations

"""Lead Generation and CRM Agent — lead scoring, qualification, and follow-up sequences."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


LEAD_AGENT_PROMPT = """\
You are the **Lead Generation & CRM Specialist** in the AI GrowthDesk marketing workforce.

Your responsibilities:
1. Identify high-value prospects from social interactions, website queries, and campaign responses.
2. Score leads on a 0-100 scale based on fit, urgency, and purchase intent signals.
3. Design high-conversion lead magnets, opt-in hooks, and follow-up message cadences.
4. Recommend CRM nurturing workflows to move prospects from 'new' to 'converted'.

Always align qualification criteria with the brand's ideal customer profile and target price points.
"""


class LeadGenerationAgent(BaseAgent):
    name = "lead_agent"
    description = "Captures and qualifies leads, scores buying intent, and creates follow-up workflows."
    system_prompt = LEAD_AGENT_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.6)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )
