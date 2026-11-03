from __future__ import annotations

"""Social Media connections and scheduling engine service."""

import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.encryption import encrypt_value
from app.models.content import ContentItem
from app.models.social import PublishLog, ScheduledPost, SocialAccount
from app.schemas.social import SchedulePostRequest, ScheduledPostUpdate, SocialAccountConnect


class SocialService:
    @staticmethod
    async def get_accounts(db: AsyncSession, workspace_id: uuid.UUID) -> list[SocialAccount]:
        result = await db.execute(
            select(SocialAccount)
            .where(SocialAccount.workspace_id == workspace_id)
            .order_by(SocialAccount.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def connect_account(
        db: AsyncSession, workspace_id: uuid.UUID, data: SocialAccountConnect
    ) -> SocialAccount:
        acc = SocialAccount(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            platform=data.platform,
            username=data.username,
            display_name=data.display_name or data.username or data.platform.capitalize(),
            avatar_url=data.avatar_url,
            encrypted_access_token=encrypt_value(data.access_token),
            encrypted_refresh_token=encrypt_value(data.refresh_token) if data.refresh_token else None,
            is_active=True,
            last_synced_at=datetime.utcnow(),
        )
        db.add(acc)
        await db.commit()
        await db.refresh(acc)
        return acc

    @staticmethod
    async def disconnect_account(
        db: AsyncSession, workspace_id: uuid.UUID, account_id: uuid.UUID
    ) -> None:
        acc = await db.get(SocialAccount, account_id)
        if not acc or acc.workspace_id != workspace_id:
            raise ValueError("Account not found")
        await db.delete(acc)
        await db.commit()

    @staticmethod
    async def get_scheduled_posts(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[ScheduledPost]:
        query = (
            select(ScheduledPost)
            .where(ScheduledPost.workspace_id == workspace_id)
            .order_by(ScheduledPost.scheduled_at.asc())
        )
        if start_date:
            query = query.where(ScheduledPost.scheduled_at >= start_date)
        if end_date:
            query = query.where(ScheduledPost.scheduled_at <= end_date)

        result = await db.execute(query)
        posts = list(result.scalars().all())
        return posts

    @staticmethod
    async def schedule_post(
        db: AsyncSession, workspace_id: uuid.UUID, data: SchedulePostRequest
    ) -> ScheduledPost:
        content = await db.get(ContentItem, data.content_id)
        if not content or content.workspace_id != workspace_id:
            raise ValueError("Content item not found")

        post = ScheduledPost(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            content_id=data.content_id,
            social_account_id=data.social_account_id,
            scheduled_at=data.scheduled_at,
            status="scheduled",
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def update_scheduled_post(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        post_id: uuid.UUID,
        data: ScheduledPostUpdate,
    ) -> ScheduledPost:
        post = await db.get(ScheduledPost, post_id)
        if not post or post.workspace_id != workspace_id:
            raise ValueError("Scheduled post not found")
        if data.scheduled_at is not None:
            post.scheduled_at = data.scheduled_at
        if data.status is not None:
            post.status = data.status
        await db.commit()
        await db.refresh(post)
        return post

    @staticmethod
    async def cancel_scheduled_post(
        db: AsyncSession, workspace_id: uuid.UUID, post_id: uuid.UUID
    ) -> None:
        post = await db.get(ScheduledPost, post_id)
        if not post or post.workspace_id != workspace_id:
            raise ValueError("Scheduled post not found")
        post.status = "cancelled"
        await db.commit()


social_service = SocialService()
