from __future__ import annotations

"""Pydantic schemas registry for AI GrowthDesk."""

from app.schemas.agent import AgentChatRequest, AgentChatResponse
from app.schemas.ai_provider import (
    AIProviderCreate,
    AIProviderResponse,
    AIProviderTestResult,
    AIProviderUpdate,
    ModelInfo,
)
from app.schemas.analytics import MetricCard, OverviewAnalytics, TimeSeriesPoint
from app.schemas.approval import ApprovalAction, ApprovalCreate, ApprovalResponse
from app.schemas.auth import (
    RefreshTokenRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    UserUpdate,
)
from app.schemas.brand import (
    BrandDocumentCreate,
    BrandDocumentResponse,
    BrandProfileCreate,
    BrandProfileResponse,
    BrandProfileUpdate,
    BrandQueryRequest,
    BrandQueryResponse,
)
from app.schemas.campaign import (
    CampaignCreate,
    CampaignResponse,
    CampaignTaskCreate,
    CampaignTaskResponse,
    CampaignTaskUpdate,
    CampaignUpdate,
)
from app.schemas.common import ErrorResponse, PaginatedResponse, StatusResponse
from app.schemas.content import (
    ContentCreate,
    ContentGenerateRequest,
    ContentResponse,
    ContentUpdate,
    ContentVersionResponse,
)
from app.schemas.inbox import (
    ConversationResponse,
    ConversationUpdate,
    MessageResponse,
    ReplyRequest,
    SuggestReplyResponse,
)
from app.schemas.lead import (
    LeadActivityCreate,
    LeadActivityResponse,
    LeadCreate,
    LeadResponse,
    LeadUpdate,
)
from app.schemas.social import (
    SchedulePostRequest,
    ScheduledPostResponse,
    ScheduledPostUpdate,
    SocialAccountConnect,
    SocialAccountResponse,
)
from app.schemas.subscription import PlanResponse, SubscriptionResponse, UpgradeRequest
from app.schemas.workspace import (
    InviteMember,
    OrgCreate,
    OrgResponse,
    WorkspaceCreate,
    WorkspaceMemberResponse,
    WorkspaceResponse,
    WorkspaceUpdate,
)

__all__ = [
    "AIProviderCreate",
    "AIProviderResponse",
    "AIProviderTestResult",
    "AIProviderUpdate",
    "AgentChatRequest",
    "AgentChatResponse",
    "ApprovalAction",
    "ApprovalCreate",
    "ApprovalResponse",
    "BrandDocumentCreate",
    "BrandDocumentResponse",
    "BrandProfileCreate",
    "BrandProfileResponse",
    "BrandProfileUpdate",
    "BrandQueryRequest",
    "BrandQueryResponse",
    "CampaignCreate",
    "CampaignResponse",
    "CampaignTaskCreate",
    "CampaignTaskResponse",
    "CampaignTaskUpdate",
    "CampaignUpdate",
    "ContentCreate",
    "ContentGenerateRequest",
    "ContentResponse",
    "ContentUpdate",
    "ContentVersionResponse",
    "ConversationResponse",
    "ConversationUpdate",
    "ErrorResponse",
    "InviteMember",
    "LeadActivityCreate",
    "LeadActivityResponse",
    "LeadCreate",
    "LeadResponse",
    "LeadUpdate",
    "MessageResponse",
    "MetricCard",
    "ModelInfo",
    "OrgCreate",
    "OrgResponse",
    "OverviewAnalytics",
    "PaginatedResponse",
    "PlanResponse",
    "RefreshTokenRequest",
    "ReplyRequest",
    "SchedulePostRequest",
    "ScheduledPostResponse",
    "ScheduledPostUpdate",
    "SocialAccountConnect",
    "SocialAccountResponse",
    "StatusResponse",
    "SubscriptionResponse",
    "SuggestReplyResponse",
    "TimeSeriesPoint",
    "TokenResponse",
    "UpgradeRequest",
    "UserLogin",
    "UserRegister",
    "UserResponse",
    "UserUpdate",
    "WorkspaceCreate",
    "WorkspaceMemberResponse",
    "WorkspaceResponse",
    "WorkspaceUpdate",
]

