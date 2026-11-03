from __future__ import annotations

"""Agent Orchestrator — coordinates the AI Marketing Director and specialist agents."""

import logging
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import select

from app.agents.advertising_agent import AdvertisingAgent
from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.brand_strategist import BrandStrategist
from app.agents.community_manager import CommunityManager
from app.agents.content_creator import ContentCreator
from app.agents.creative_director import CreativeDirector
from app.agents.director import MarketingDirector
from app.agents.growth_analyst import GrowthAnalyst
from app.agents.lead_agent import LeadGenerationAgent
from app.agents.research import MarketResearchAgent
from app.agents.seo_agent import SEOGrowthAgent
from app.agents.social_manager import SocialMediaManager
from app.models.brand import BrandDocument, BrandProfile
from app.providers.factory import get_ai_provider

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Central orchestrator for AI marketing workforce agents."""

    def __init__(self):
        self.agents: dict[str, BaseAgent] = {
            "director": MarketingDirector(),
            "research": MarketResearchAgent(),
            "brand_strategist": BrandStrategist(),
            "content_creator": ContentCreator(),
            "creative_director": CreativeDirector(),
            "social_manager": SocialMediaManager(),
            "community_manager": CommunityManager(),
            "lead_agent": LeadGenerationAgent(),
            "advertising_agent": AdvertisingAgent(),
            "seo_agent": SEOGrowthAgent(),
            "growth_analyst": GrowthAnalyst(),
        }

    async def build_brand_context(self, db: "AsyncSession", workspace_id: UUID) -> str:
        """Fetch and compile brand information and knowledge documents into a context block."""
        profile_res = await db.execute(
            select(BrandProfile).where(BrandProfile.workspace_id == workspace_id)
        )
        profile = profile_res.scalar_one_or_none()

        docs_res = await db.execute(
            select(BrandDocument).where(BrandDocument.workspace_id == workspace_id).limit(5)
        )
        docs = docs_res.scalars().all()

        lines = ["=== BRAND BRAIN KNOWLEDGE BASE ==="]
        if profile:
            lines.append(f"Company: {profile.company_name}")
            if profile.industry:
                lines.append(f"Industry: {profile.industry}")
            if profile.description:
                lines.append(f"Description: {profile.description}")
            if profile.target_audience:
                lines.append(f"Target Audience: {profile.target_audience}")
            if profile.brand_voice:
                lines.append(f"Brand Voice: {profile.brand_voice}")
            if profile.tone_keywords:
                lines.append(f"Tone Keywords: {', '.join(profile.tone_keywords)}")
            if profile.products_services:
                lines.append(f"Products/Services: {profile.products_services}")
            if profile.competitors:
                lines.append(f"Key Competitors: {', '.join(profile.competitors)}")
            if profile.restricted_topics:
                lines.append(f"RESTRICTED TOPICS & CLAIMS: {', '.join(profile.restricted_topics)}")
            if profile.brand_colors:
                lines.append(f"Brand Colors: {profile.brand_colors}")
        else:
            lines.append("Brand profile: No profile configured yet. Maintain professional, modern SaaS best practices.")

        if docs:
            lines.append("\n=== REFERENCE DOCUMENTS ===")
            for doc in docs:
                content_preview = (doc.content or "")[:400]
                lines.append(f"Document [{doc.title}]: {content_preview}")

        return "\n".join(lines)

    async def chat(
        self,
        db: "AsyncSession",
        workspace_id: UUID,
        user_message: str,
        conversation_history: list[dict] | None = None,
        target_agent: str = "director",
        campaign_context: dict | None = None,
    ) -> AgentResult:
        """Route a user message to the specified agent (default: director)."""
        brand_context = await self.build_brand_context(db, workspace_id)
        provider = await get_ai_provider(db, str(workspace_id))

        context = AgentContext(
            workspace_id=str(workspace_id),
            brand_context=brand_context,
            user_message=user_message,
            conversation_history=conversation_history or [],
            campaign_context=campaign_context,
        )

        agent = self.agents.get(target_agent, self.agents["director"])
        try:
            return await agent.execute(context, provider)
        except Exception as e:
            logger.warning(f"Provider {provider.provider_name} call failed: {e}. Falling back to preview engine.")
            from app.providers.fallback_provider import FallbackSimulationProvider
            fallback = FallbackSimulationProvider(api_key="preview", model="growthdesk-strategy-v1")
            res = await agent.execute(context, fallback)
            res.response = (
                f"> ℹ️ **Notice ({provider.provider_name})**: {str(e)}\n\n"
                f"{res.response}"
            )
            return res


orchestrator = AgentOrchestrator()

