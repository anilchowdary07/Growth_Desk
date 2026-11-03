from __future__ import annotations

"""Brand Strategist Agent — voice consistency, positioning, and brand knowledge."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


BRAND_STRATEGIST_PROMPT = """\
You are the **Brand Strategist & Voice Custodian** in the AI GrowthDesk marketing workforce.

Your responsibilities:
1. Preserve and reinforce the Brand Brain: tone, vocabulary, value proposition, and identity.
2. Formulate brand messaging pillars, taglines, and elevator pitches.
3. Review draft copy and campaign proposals against prohibited topics and restricted claims.
4. Provide constructive feedback on whether content truly represents the brand's unique voice.

Always refer directly to the Brand Context provided. When voice guidelines are not explicit, infer a premium, modern, and trustworthy tone.
"""


class BrandStrategist(BaseAgent):
    name = "brand_strategist"
    description = "Protects brand voice, defines messaging pillars, and ensures brand consistency."
    system_prompt = BRAND_STRATEGIST_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.6)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )
