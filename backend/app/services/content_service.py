from __future__ import annotations

"""Content & Creative Studio service."""

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agents.orchestrator import orchestrator
from app.models.content import ContentItem, ContentVersion
from app.schemas.content import ContentCreate, ContentGenerateRequest, ContentUpdate


class ContentService:
    @staticmethod
    async def get_content_items(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        content_type: str | None = None,
        platform: str | None = None,
        status: str | None = None,
        campaign_id: uuid.UUID | None = None,
    ) -> list[ContentItem]:
        query = (
            select(ContentItem)
            .options(selectinload(ContentItem.versions))
            .where(ContentItem.workspace_id == workspace_id)
            .order_by(ContentItem.created_at.desc())
        )
        if content_type:
            query = query.where(ContentItem.content_type == content_type)
        if platform:
            query = query.where(ContentItem.platform == platform)
        if status:
            query = query.where(ContentItem.status == status)
        if campaign_id:
            query = query.where(ContentItem.campaign_id == campaign_id)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_content(
        db: AsyncSession, workspace_id: uuid.UUID, content_id: uuid.UUID
    ) -> ContentItem | None:
        result = await db.execute(
            select(ContentItem)
            .options(selectinload(ContentItem.versions))
            .where(ContentItem.id == content_id, ContentItem.workspace_id == workspace_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_content(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        user_id: uuid.UUID | None,
        data: ContentCreate,
    ) -> ContentItem:
        item = ContentItem(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            campaign_id=data.campaign_id,
            title=data.title,
            content_type=data.content_type,
            platform=data.platform,
            body=data.body or "",
            metadata_json=data.metadata_json or {},
            media_urls=data.media_urls or [],
            status="draft",
            created_by=user_id,
        )
        db.add(item)
        await db.flush()

        if item.body:
            version = ContentVersion(
                id=uuid.uuid4(),
                content_id=item.id,
                version_number=1,
                body=item.body,
                metadata_json=item.metadata_json,
                created_by=str(user_id) if user_id else "user",
            )
            db.add(version)

        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def generate_content(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        user_id: uuid.UUID | None,
        request: ContentGenerateRequest,
    ) -> list[ContentItem]:
        prompt = (
            f"Generate high-performing, brand-aligned marketing copy.\n"
            f"Content Type: {request.content_type}\n"
            f"Target Platform: {request.platform or 'Multi-platform'}\n"
            f"Prompt / Theme: {request.prompt}\n"
        )
        if request.additional_guidelines:
            prompt += f"Additional Guidelines: {request.additional_guidelines}\n"

        prompt += "\nFormat as ready-to-publish copy with hooks, body, hashtags, and call-to-action."

        agent_result = await orchestrator.chat(
            db=db,
            workspace_id=workspace_id,
            user_message=prompt,
            target_agent="content_creator",
        )

        items = []
        item = ContentItem(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            campaign_id=request.campaign_id,
            title=f"{request.content_type.capitalize()}: {request.prompt[:40]}...",
            content_type=request.content_type,
            platform=request.platform,
            body=agent_result.response,
            metadata_json={
                "generated_by": agent_result.agent_name,
                "model": agent_result.metadata.get("model"),
            },
            status="review",
            ai_model_used=agent_result.metadata.get("model", "ai-specialist"),
            created_by=user_id,
        )
        db.add(item)
        await db.flush()

        version = ContentVersion(
            id=uuid.uuid4(),
            content_id=item.id,
            version_number=1,
            body=item.body,
            metadata_json=item.metadata_json,
            created_by="ai",
        )
        db.add(version)
        items.append(item)

        await db.commit()
        for it in items:
            await db.refresh(it)
        return items

    @staticmethod
    async def update_content(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        content_id: uuid.UUID,
        data: ContentUpdate,
    ) -> ContentItem:
        item = await ContentService.get_content(db, workspace_id, content_id)
        if not item:
            raise ValueError("Content not found")

        body_changed = data.body is not None and data.body != item.body

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(item, field, value)

        if body_changed:
            current_versions_res = await db.execute(
                select(ContentVersion).where(ContentVersion.content_id == content_id)
            )
            count = len(current_versions_res.scalars().all())
            version = ContentVersion(
                id=uuid.uuid4(),
                content_id=content_id,
                version_number=count + 1,
                body=item.body or "",
                metadata_json=item.metadata_json,
                created_by="user",
            )
            db.add(version)

        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def approve_content(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        content_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> ContentItem:
        item = await ContentService.get_content(db, workspace_id, content_id)
        if not item:
            raise ValueError("Content not found")
        item.status = "approved"
        item.approved_by = user_id
        item.approved_at = datetime.utcnow()
        await db.commit()
        await db.refresh(item)
        return item

    @staticmethod
    async def delete_content(
        db: AsyncSession, workspace_id: uuid.UUID, content_id: uuid.UUID
    ) -> None:
        item = await ContentService.get_content(db, workspace_id, content_id)
        if not item:
            raise ValueError("Content not found")
        await db.delete(item)
        await db.commit()


content_service = ContentService()

