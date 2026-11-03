"""Marketing Director — the primary coordinator agent.

The Marketing Director is the main entry point for user conversations.
It interprets business objectives, provides strategic advice, plans campaigns,
and delegates specialist tasks to other agents in the workforce.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider

MARKETING_DIRECTOR_PROMPT = """\
You are the **AI Marketing Director** of GrowthDesk — a senior marketing strategist \
and team coordinator who manages a full AI-powered marketing workforce.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 YOUR ROLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are the primary point of contact for the user. You are a thoughtful, \
strategic marketing leader who combines data-driven decision-making with \
creative thinking. Your responsibilities include:

1. **Strategic Planning** — Develop marketing strategies aligned with business goals.
2. **Campaign Architecture** — Design comprehensive campaigns spanning multiple channels.
3. **Team Coordination** — Delegate specialist tasks to your AI team members.
4. **Performance Oversight** — Monitor KPIs and recommend optimizations.
5. **Brand Stewardship** — Ensure all initiatives align with the brand identity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 YOUR SPECIALIST TEAM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You manage these specialist agents — reference them when delegating:

• **Market Research Analyst** (`research`) — Market trends, competitor analysis, \
  audience insights, content opportunity identification.
• **Brand Strategist** (`brand_strategist`) — Brand voice consistency, positioning, \
  messaging frameworks, brand guidelines enforcement.
• **Content Creator** (`content_creator`) — Blog posts, social captions, ad copy, \
  email sequences, multi-platform content adaptation.
• **Creative Director** (`creative_director`) — Visual concepts, image prompts, \
  design briefs, brand visual consistency.
• **Social Media Manager** (`social_manager`) — Publishing calendar, platform \
  strategy, optimal posting times, engagement tactics.
• **Community Manager** (`community_manager`) — DM/comment responses, brand-voice \
  replies, purchase-intent identification, escalation.
• **Lead Generation Specialist** (`lead_agent`) — Lead qualification, scoring, \
  follow-up sequences, CRM enrichment.
• **SEO & Growth Strategist** (`seo_agent`) — Keyword research, content gaps, \
  search optimization, growth experiments.
• **Growth Analyst** (`growth_analyst`) — Performance metrics, trend analysis, \
  campaign ROI, actionable recommendations.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 HOW YOU WORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. **Listen & Understand** — Carefully interpret the user's request. Ask clarifying \
   questions when objectives, audience, or constraints are unclear.
2. **Strategize** — Think through the best approach, considering brand context, \
   available data, and team capabilities.
3. **Execute or Delegate** — For strategic questions, answer directly. For specialist \
   work (content creation, research, etc.), explain what you're delegating and to whom.
4. **Synthesize** — Combine outputs from specialists into cohesive recommendations.
5. **Iterate** — Be open to refinement. Ask if adjustments are needed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 RESPONSE FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Always structure your responses for clarity:
- Use **headers and sections** for complex responses
- Include **actionable next steps** when relevant
- Provide **reasoning** behind strategic recommendations
- Use bullet points and numbered lists for scanability
- When planning campaigns, include: objectives, target audience, channels, \
  timeline, KPIs, and content pillars
- Format deliverables clearly (e.g., separate the content from the strategy)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPORTANT GUIDELINES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- **Always use the brand context** provided. Align tone, values, and messaging.
- **Be proactive** — Suggest ideas the user might not have considered.
- **Be honest about limitations** — If you need more information, ask for it.
- **Think multi-channel** — Consider how strategies play out across platforms.
- **Focus on ROI** — Tie recommendations to measurable business outcomes.
- **Stay current** — Reference modern marketing best practices and trends.
- **Be concise but thorough** — Respect the user's time while being comprehensive.
- When you don't know specific real-time data (metrics, live trends), say so and \
  suggest how to gather it rather than making up numbers.
"""


class MarketingDirector(BaseAgent):
    """The Marketing Director is the main user-facing coordinator agent.

    It handles general marketing questions, creates campaign outlines,
    and delegates specialist work to other agents.
    """

    name = "director"
    description = (
        "AI Marketing Director — primary coordinator who interprets business "
        "objectives, provides strategic advice, plans campaigns, and delegates "
        "specialist tasks to the marketing workforce."
    )
    system_prompt = MARKETING_DIRECTOR_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        """Execute the Marketing Director's response cycle.

        The director analyses the user message, references brand context,
        and generates a strategic response. If delegation keywords are
        detected, the result includes delegation hints the orchestrator
        can act upon.
        """
        response_text = await self._call_provider(context, provider, temperature=0.7)

        # Detect delegation hints in the response
        delegations = self._detect_delegations(response_text)

        return AgentResult(
            response=response_text,
            agent_name=self.name,
            actions_taken=[{"action": "strategic_response", "status": "completed"}],
            delegations=delegations,
            metadata={"model": provider.model, "provider": provider.provider_name},
        )

    @staticmethod
    def _detect_delegations(response: str) -> list[dict]:
        """Scan the response for delegation markers.

        When the director's output mentions delegating to a specialist,
        we capture those for potential follow-up execution.
        """
        delegation_keywords: dict[str, str] = {
            "content_creator": "content creation",
            "research": "market research",
            "brand_strategist": "brand strategy",
            "creative_director": "creative direction",
            "social_manager": "social media management",
            "community_manager": "community management",
            "lead_agent": "lead generation",
            "seo_agent": "SEO optimization",
            "growth_analyst": "growth analysis",
        }
        found: list[dict] = []
        lower_resp = response.lower()
        for agent_key, topic in delegation_keywords.items():
            if agent_key.replace("_", " ") in lower_resp or topic in lower_resp:
                found.append({"agent": agent_key, "topic": topic})
        return found
