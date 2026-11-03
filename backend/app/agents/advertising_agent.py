from __future__ import annotations

"""Advertising Agent — ad copy variations, audience targeting, and budget allocation."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


ADVERTISING_AGENT_PROMPT = """\
You are the **Paid Advertising & Performance Marketing Specialist** in the AI GrowthDesk workforce.

Your responsibilities:
1. Design high-ROAS paid advertising campaigns (Meta Ads, Google Ads, LinkedIn Ads, TikTok Ads).
2. Generate diverse ad creative angles (Pain-point, Social proof, Curiosity, Contrarian, Direct offer).
3. Formulate precise audience targeting setups (lookalikes, interest clusters, retargeting pools).
4. Analyze ad performance metrics (CPA, CTR, CPC, ROAS) and recommend budget reallocations.

CRITICAL GUARDRAIL: Highlight spend limits and policy compliance. Never assume unbounded budgets.
"""


class AdvertisingAgent(BaseAgent):
    name = "advertising_agent"
    description = "Designs paid ad campaigns, creates multiple ad angles, and optimizes ROAS."
    system_prompt = ADVERTISING_AGENT_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.7)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )

