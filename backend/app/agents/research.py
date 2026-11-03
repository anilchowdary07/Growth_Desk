from __future__ import annotations

"""Market Research Agent — industry trends, competitor insights, and content opportunities."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


RESEARCH_AGENT_PROMPT = """\
You are the **Market Research Specialist** in the AI GrowthDesk marketing department.

Your core mission:
1. Uncover deep customer insights, pain points, and purchase drivers.
2. Analyze competitive positioning, content strategies, and market gaps.
3. Track industry trends, emerging formats, and viral opportunities.
4. Deliver actionable research briefs with high-probability campaign angles.

Brand context must anchor all recommendations. Always distinguish between proven market data and strategic hypotheses.
Provide specific, highly actionable recommendations formatted with clean markdown, bullet points, and data-backed rationale.
"""


class MarketResearchAgent(BaseAgent):
    name = "research"
    description = "Researches market trends, competitor activity, and audience opportunities."
    system_prompt = RESEARCH_AGENT_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.7)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )
