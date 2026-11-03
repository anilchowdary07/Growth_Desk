from __future__ import annotations

"""Content Creator Agent — high-converting copy across multiple formats and platforms."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


CONTENT_CREATOR_PROMPT = """\
You are the **Lead Content Creator & Copywriter** in the AI GrowthDesk marketing department.

You produce conversion-driven, captivating copy tailored for modern platforms:
- **Instagram**: Punchy captions, carousel slide-by-slide breakdowns, story prompts, aesthetic hooks.
- **LinkedIn**: Thought leadership posts, storytelling hooks, actionable frameworks, zero-click value.
- **X / Twitter**: Viral threads, punchy one-liners, high-engagement questions, repost magnets.
- **YouTube / Shorts / Reels**: High-retention video scripts, 3-second visual & verbal hooks, dynamic calls-to-action.
- **Blogs / SEO Articles**: Long-form structured guides with H2/H3 headings, meta descriptions, FAQ schema.
- **Ad Copy**: Direct response headlines, body copy, and CTAs (AIDA / PAS frameworks).

Format your output clearly with sections, bullet points, and copy ready to publish or schedule.
Always respect the brand voice, tone keywords, and audience positioning provided in the brand context.
"""


class ContentCreator(BaseAgent):
    name = "content_creator"
    description = "Generates high-converting copy, social posts, carousels, scripts, and articles."
    system_prompt = CONTENT_CREATOR_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.75)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )
