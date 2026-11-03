from __future__ import annotations

"""Unified Inbox & Social Conversations service."""

import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agents.orchestrator import orchestrator
from app.models.inbox import Conversation, Message
from app.models.lead import Lead, LeadActivity
from app.schemas.inbox import ConversationUpdate, ReplyRequest, SuggestReplyResponse


class InboxService:
    @staticmethod
    async def get_conversations(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        status: str | None = None,
        platform: str | None = None,
        priority: str | None = None,
    ) -> list[Conversation]:
        query = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.workspace_id == workspace_id)
            .order_by(Conversation.last_message_at.desc().nullslast())
        )
        if status:
            query = query.where(Conversation.status == status)
        if platform:
            query = query.where(Conversation.platform == platform)
        if priority:
            query = query.where(Conversation.priority == priority)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_conversation(
        db: AsyncSession, workspace_id: uuid.UUID, conversation_id: uuid.UUID
    ) -> Conversation | None:
        result = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id, Conversation.workspace_id == workspace_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def reply(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        data: ReplyRequest,
    ) -> Message:
        conv = await InboxService.get_conversation(db, workspace_id, conversation_id)
        if not conv:
            raise ValueError("Conversation not found")

        msg = Message(
            id=uuid.uuid4(),
            conversation_id=conversation_id,
            direction="outbound",
            sender_type="user",
            sender_id=str(user_id),
            body=data.body,
            status=data.status,
            is_ai_generated=False,
        )
        db.add(msg)
        conv.last_message_at = datetime.utcnow()
        conv.status = "replied"
        await db.commit()
        await db.refresh(msg)
        return msg

    @staticmethod
    async def suggest_reply(
        db: AsyncSession, workspace_id: uuid.UUID, conversation_id: uuid.UUID
    ) -> SuggestReplyResponse:
        conv = await InboxService.get_conversation(db, workspace_id, conversation_id)
        if not conv:
            raise ValueError("Conversation not found")

        recent_msgs = conv.messages[-5:] if conv.messages else []
        history_text = "\n".join(
            [f"{m.sender_type.upper()}: {m.body}" for m in recent_msgs]
        )

        prompt = (
            f"You are the Community Manager. Analyze this customer interaction and suggest an optimal, brand-aligned reply.\n"
            f"Platform: {conv.platform}\n"
            f"Contact: {conv.contact_name or 'Customer'}\n"
            f"Recent Conversation:\n{history_text or 'No prior messages'}\n\n"
            f"Respond with:\n"
            f"1. Suggested Reply Text (warm, direct, professional)\n"
            f"2. Sentiment (Positive/Neutral/Negative)\n"
            f"3. Intent (Purchase Intent, Support Inquiry, Casual Comment, Complaint)"
        )

        agent_res = await orchestrator.chat(
            db=db,
            workspace_id=workspace_id,
            user_message=prompt,
            target_agent="community_manager",
        )

        return SuggestReplyResponse(
            suggested_reply=agent_res.response,
            confidence=0.92,
            sentiment=conv.sentiment or "neutral",
            intent_detected=conv.classification or "inquiry",
            reasoning="Analyzed with Community Manager against Brand Brain guidelines.",
        )

    @staticmethod
    async def update_conversation(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        conversation_id: uuid.UUID,
        data: ConversationUpdate,
    ) -> Conversation:
        conv = await InboxService.get_conversation(db, workspace_id, conversation_id)
        if not conv:
            raise ValueError("Conversation not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(conv, field, value)

        await db.commit()
        await db.refresh(conv)
        return conv

    @staticmethod
    async def create_lead_from_conversation(
        db: AsyncSession, workspace_id: uuid.UUID, conversation_id: uuid.UUID
    ) -> Lead:
        conv = await InboxService.get_conversation(db, workspace_id, conversation_id)
        if not conv:
            raise ValueError("Conversation not found")

        lead = Lead(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            name=conv.contact_name or conv.contact_username or "Social Prospect",
            source=conv.platform,
            source_conversation_id=conv.id,
            status="new",
            score=70 if conv.classification == "purchase_intent" else 50,
            notes=f"Lead automatically captured from {conv.platform} {conv.conversation_type}.",
        )
        db.add(lead)
        conv.lead_id = lead.id

        activity = LeadActivity(
            id=uuid.uuid4(),
            lead_id=lead.id,
            activity_type="created",
            description=f"Captured from {conv.platform} interaction",
            performed_by="ai",
        )
        db.add(activity)

        await db.commit()
        await db.refresh(lead)
        return lead


inbox_service = InboxService()
