"""Fallback simulation provider for development and sandbox testing without an active API key."""

from __future__ import annotations

import logging
from app.providers.base import AIMessage, AIResponse, BaseAIProvider

logger = logging.getLogger(__name__)


class FallbackSimulationProvider(BaseAIProvider):
    """Provides high-quality structured marketing responses when no external API key is connected."""

    provider_name = "preview_engine"

    @property
    def default_model(self) -> str:
        return "growthdesk-strategy-v1"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "growthdesk-strategy-v1", "name": "GrowthDesk Strategy Preview Engine", "context_window": 128_000}
        ]

    async def chat(self, messages: list[AIMessage], **kwargs) -> AIResponse:
        user_msg = next((m.content for m in reversed(messages) if m.role == "user"), "Strategy inquiry")

        # Synthesize a realistic marketing strategy / copy response
        response_text = (
            f"### 🎯 Strategic Analysis & Campaign Architecture\n\n"
            f"**Objective Focus**: \"{user_msg[:120]}...\"\n\n"
            f"#### 1. Core Positioning & Angle\n"
            f"- **Value Proposition**: High-retention, proof-driven narrative eliminating buyer skepticism.\n"
            f"- **Primary Channels**: LinkedIn (organic authority carousels) + Instagram (reels & visual objection-breakers).\n"
            f"- **Lead Engine**: 2-step value exchange (educational asset -> discovery qualification).\n\n"
            f"#### 2. Weekly Execution Roadmap\n"
            f"- **Week 1 (Attention Blitz)**: 5 high-impact thought leadership hooks addressing industry pain points.\n"
            f"- **Week 2 (Solution Proof)**: 3 customer case studies & slide-by-slide transformation carousels.\n"
            f"- **Week 3 (Direct Conversion)**: 4 direct-response offer posts with qualifying keyword triggers.\n"
            f"- **Week 4 (Retargeting & Close)**: Follow-up nurture sequences to convert warm conversation leads.\n\n"
            f"#### 3. Recommended KPI Targets\n"
            f"- Target Impressions: 25,000+ targeted views\n"
            f"- Inbound Buying Conversations: 40–50\n"
            f"- Qualified Pipeline Leads: 25+ booked inquiries\n\n"
            f"---\n"
            f"*💡 **Notice**: Operating in GrowthDesk Strategy Preview Mode. To run live generation with GPT-4o, Claude 3.5 Sonnet, Gemini 2.0, DeepSeek, or OpenRouter, connect your API key under **Settings → AI Providers (BYOK)**.*"
        )

        return AIResponse(
            content=response_text,
            model=self.model,
            provider=self.provider_name,
            usage={"prompt_tokens": 150, "completion_tokens": 300, "total_tokens": 450},
        )

    async def test_connection(self) -> bool:
        return True

