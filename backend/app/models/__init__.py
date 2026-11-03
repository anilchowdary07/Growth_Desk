from __future__ import annotations

"""Database models registry for AI GrowthDesk."""

from app.models.ai_provider import AIProvider
from app.models.approval import Approval
from app.models.audit import AuditLog
from app.models.brand import BrandDocument, BrandEmbedding, BrandProfile
from app.models.campaign import Campaign, CampaignTask
from app.models.content import ContentItem, ContentVersion
from app.models.inbox import Conversation, Message
from app.models.lead import Lead, LeadActivity
from app.models.social import PublishLog, ScheduledPost, SocialAccount
from app.models.subscription import Plan, Subscription
from app.models.user import User
from app.models.workspace import Organization, OrgMember, Workspace, WorkspaceMember

__all__ = [
    "AIProvider",
    "Approval",
    "AuditLog",
    "BrandDocument",
    "BrandEmbedding",
    "BrandProfile",
    "Campaign",
    "CampaignTask",
    "ContentItem",
    "ContentVersion",
    "Conversation",
    "Lead",
    "LeadActivity",
    "Message",
    "OrgMember",
    "Organization",
    "Plan",
    "PublishLog",
    "ScheduledPost",
    "SocialAccount",
    "Subscription",
    "User",
    "Workspace",
    "WorkspaceMember",
]
