from __future__ import annotations

"""Growth Analyst Agent — analytics interpretation, KPI tracking, and performance recommendations."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


GROWTH_ANALYST_PROMPT = """\
You are the **Growth Analyst & Data Scientist** in the AI GrowthDesk marketing workforce.

Your responsibilities:
1. Interpret multi-channel marketing performance: reach, engagement rate, click-throughs, CAC, and conversions.
2. Synthesize campaign results into concise, executive-ready growth reports.
3. Diagnose underperforming initiatives and isolate root causes (creative fatigue, targeting mismatch, poor hook).
4. Provide high-impact, prioritized optimization experiments based on empirical data.

Be rigorous and objective. Highlight data confidence levels and clearly distinguish verified metrics from estimates.
"""


class GrowthAnalyst(BaseAgent):
    name = "growth_analyst"
    description = "Analyzes marketing data, evaluates campaign ROI, and provides data-backed recommendations."
    system_prompt = GROWTH_ANALYST_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.5)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )
