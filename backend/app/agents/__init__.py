from __future__ import annotations

"""Agents registry for AI GrowthDesk."""

from app.agents.advertising_agent import AdvertisingAgent
from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.brand_strategist import BrandStrategist
from app.agents.community_manager import CommunityManager
from app.agents.content_creator import ContentCreator
from app.agents.creative_director import CreativeDirector
from app.agents.director import MarketingDirector
from app.agents.growth_analyst import GrowthAnalyst
from app.agents.lead_agent import LeadGenerationAgent
from app.agents.orchestrator import AgentOrchestrator, orchestrator
from app.agents.research import MarketResearchAgent
from app.agents.seo_agent import SEOGrowthAgent
from app.agents.social_manager import SocialMediaManager

__all__ = [
    "AdvertisingAgent",
    "AgentContext",
    "AgentOrchestrator",
    "AgentResult",
    "BaseAgent",
    "BrandStrategist",
    "CommunityManager",
    "ContentCreator",
    "CreativeDirector",
    "GrowthAnalyst",
    "LeadGenerationAgent",
    "MarketResearchAgent",
    "MarketingDirector",
    "SEOGrowthAgent",
    "SocialMediaManager",
    "orchestrator",
]
