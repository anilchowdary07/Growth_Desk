from __future__ import annotations

"""Services registry for AI GrowthDesk."""

from app.services.ai_provider_service import ai_provider_service
from app.services.analytics_service import analytics_service
from app.services.approval_service import approval_service
from app.services.auth_service import auth_service
from app.services.brand_service import brand_service
from app.services.campaign_service import campaign_service
from app.services.content_service import content_service
from app.services.inbox_service import inbox_service
from app.services.lead_service import lead_service
from app.services.social_service import social_service
from app.services.subscription_service import subscription_service
from app.services.workspace_service import workspace_service

__all__ = [
    "ai_provider_service",
    "analytics_service",
    "approval_service",
    "auth_service",
    "brand_service",
    "campaign_service",
    "content_service",
    "inbox_service",
    "lead_service",
    "social_service",
    "subscription_service",
    "workspace_service",
]

