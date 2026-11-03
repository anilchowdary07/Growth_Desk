from __future__ import annotations

"""Approval service for human-in-the-loop workflows."""

import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.approval import Approval
from app.models.content import ContentItem
from app.schemas.approval import ApprovalAction, ApprovalCreate


class ApprovalService:
    @staticmethod
    async def get_approvals(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        status: str = "pending",
    ) -> list[Approval]:
        query = (
            select(Approval)
            .where(Approval.workspace_id == workspace_id)
            .order_by(Approval.created_at.desc())
        )
        if status != "all":
            query = query.where(Approval.status == status)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create_approval(
        db: AsyncSession, workspace_id: uuid.UUID, data: ApprovalCreate
    ) -> Approval:
        approval = Approval(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            item_type=data.item_type,
            item_id=data.item_id,
            title=data.title,
            description=data.description,
            status="pending",
            requested_by="ai",
            meta_data=data.meta_data,
            expires_at=data.expires_at,
        )
        db.add(approval)
        await db.commit()
        await db.refresh(approval)
        return approval

    @staticmethod
    async def approve_item(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        approval_id: uuid.UUID,
        user_id: uuid.UUID,
        action: ApprovalAction | None = None,
    ) -> Approval:
        approval = await db.get(Approval, approval_id)
        if not approval or approval.workspace_id != workspace_id:
            raise ValueError("Approval item not found")

        approval.status = "approved"
        approval.reviewed_by = user_id
        approval.reviewed_at = datetime.utcnow()
        if action and action.note:
            approval.review_note = action.note

        # If it's a content item, update content status
        if approval.item_type == "content":
            content = await db.get(ContentItem, approval.item_id)
            if content:
                content.status = "approved"
                content.approved_by = user_id
                content.approved_at = datetime.utcnow()

        await db.commit()
        await db.refresh(approval)
        return approval

    @staticmethod
    async def reject_item(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        approval_id: uuid.UUID,
        user_id: uuid.UUID,
        action: ApprovalAction,
    ) -> Approval:
        approval = await db.get(Approval, approval_id)
        if not approval or approval.workspace_id != workspace_id:
            raise ValueError("Approval item not found")

        approval.status = "rejected"
        approval.reviewed_by = user_id
        approval.reviewed_at = datetime.utcnow()
        approval.review_note = action.note

        if approval.item_type == "content":
            content = await db.get(ContentItem, approval.item_id)
            if content:
                content.status = "rejected"

        await db.commit()
        await db.refresh(approval)
        return approval


approval_service = ApprovalService()

