from __future__ import annotations

"""Creative Director Agent — visual concepts, prompts for image generation, and design briefs."""

from typing import TYPE_CHECKING

from app.agents.base import AgentContext, AgentResult, BaseAgent

if TYPE_CHECKING:
    from app.providers.base import BaseAIProvider


CREATIVE_DIRECTOR_PROMPT = """\
You are the **Creative Director** in the AI GrowthDesk marketing workforce.

Your responsibilities:
1. Translate marketing ideas into visual concepts, posters, carousels, and ad banners.
2. Produce production-ready prompts for AI image generators (Midjourney, DALL-E 3, Flux, Imagen).
3. Specify color palettes, typography styling, framing, lighting, aspect ratios, and focal points.
4. Provide creative briefs for video editors and graphic designers.

Always ground visual ideas in the brand's visual identity, primary colors, and aesthetic standards.
"""


class CreativeDirector(BaseAgent):
    name = "creative_director"
    description = "Designs visual concepts, image generation prompts, and creative production briefs."
    system_prompt = CREATIVE_DIRECTOR_PROMPT

    async def execute(self, context: AgentContext, provider: "BaseAIProvider") -> AgentResult:
        messages = self.build_messages(context)
        response = await provider.chat(messages, temperature=0.7)
        return AgentResult(
            response=response.content,
            agent_name=self.name,
            metadata={"model": response.model, "provider": response.provider},
        )
