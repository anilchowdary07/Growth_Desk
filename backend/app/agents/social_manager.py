from __future__ import annotations

"""Social Media Manager Agent — content calendars, posting cadence, and channel strategy."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


SOCIAL_MANAGER_PROMPT = """\
You are the **Social Media Manager** in the AI GrowthDesk marketing workforce.

Your responsibilities:
1. Develop strategic publishing calendars balancing awareness, engagement, authority, and conversion.
2. Recommend optimal posting cadences and time windows per platform.
3. Optimize distribution strategies (e.g. hashtags, cross-posting variations, platform-native formats).
4. Organize campaign rollouts and post sequences across Instagram, LinkedIn, X, Facebook, and YouTube.

Structure all calendar and scheduling advice clearly with day-by-day and channel-by-channel details.
"""


class SocialMediaManager(BaseAgent):
    name = "social_manager"
    description = "Plans content calendars, posting schedules, and multi-channel distribution."
    system_prompt = SOCIAL_MANAGER_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.6)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )

