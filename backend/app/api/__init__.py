from __future__ import annotations

"""API Routers registry for AI GrowthDesk."""

from app.api.agents import router as agents_router
from app.api.ai_providers import router as ai_providers_router
from app.api.analytics import router as analytics_router
from app.api.approvals import router as approvals_router
from app.api.auth import router as auth_router
from app.api.brand import router as brand_router
from app.api.campaigns import router as campaigns_router
from app.api.content import router as content_router
from app.api.inbox import router as inbox_router
from app.api.leads import router as leads_router
from app.api.social import router as social_router
from app.api.subscriptions import router as subscriptions_router
from app.api.workspaces import router as workspaces_router

all_routers = [
    auth_router,
    workspaces_router,
    ai_providers_router,
    brand_router,
    campaigns_router,
    content_router,
    social_router,
    inbox_router,
    leads_router,
    analytics_router,
    approvals_router,
    subscriptions_router,
    agents_router,
]
