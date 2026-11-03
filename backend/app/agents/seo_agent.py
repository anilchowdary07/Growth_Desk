from __future__ import annotations

"""SEO & Growth Agent — keyword research, content gap analysis, and organic visibility."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


SEO_AGENT_PROMPT = """\
You are the **SEO & Organic Growth Specialist** in the AI GrowthDesk marketing workforce.

Your responsibilities:
1. Identify high-intent keyword clusters, search volumes, and difficulty tiers.
2. Conduct competitor content gap audits to identify easy ranking opportunities.
3. Formulate article outlines optimized for search intent, entity coverage, and Generative Engine Optimization (GEO / Perplexity / Gemini search visibility).
4. Recommend internal linking architectures and on-page optimization improvements.
"""


class SEOGrowthAgent(BaseAgent):
    name = "seo_agent"
    description = "Conducts SEO research, identifies content gaps, and optimizes for search & GEO engines."
    system_prompt = SEO_AGENT_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.6)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )

