from __future__ import annotations

"""Brand Brain service — profiles, knowledge base documents, and context search."""

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.brand import BrandDocument, BrandProfile
from app.schemas.brand import (
    BrandDocumentCreate,
    BrandProfileCreate,
    BrandProfileUpdate,
    BrandQueryResponse,
)


class BrandService:
    @staticmethod
    async def get_profile(db: AsyncSession, workspace_id: uuid.UUID) -> BrandProfile | None:
        result = await db.execute(
            select(BrandProfile).where(BrandProfile.workspace_id == workspace_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_or_update_profile(
        db: AsyncSession, workspace_id: uuid.UUID, data: BrandProfileCreate | BrandProfileUpdate
    ) -> BrandProfile:
        profile = await BrandService.get_profile(db, workspace_id)

        if not profile:
            profile = BrandProfile(
                id=uuid.uuid4(),
                workspace_id=workspace_id,
                company_name=data.company_name or "My Business",
            )
            db.add(profile)

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None or isinstance(data, BrandProfileUpdate):
                setattr(profile, field, value)

        await db.commit()
        await db.refresh(profile)
        return profile

    @staticmethod
    async def get_documents(db: AsyncSession, workspace_id: uuid.UUID) -> list[BrandDocument]:
        result = await db.execute(
            select(BrandDocument)
            .where(BrandDocument.workspace_id == workspace_id)
            .order_by(BrandDocument.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def add_document(
        db: AsyncSession, workspace_id: uuid.UUID, data: BrandDocumentCreate
    ) -> BrandDocument:
        doc = BrandDocument(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            title=data.title,
            content=data.content,
            doc_type=data.doc_type,
            metadata_json=data.metadata_json,
            is_processed=True,
        )
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        return doc

    @staticmethod
    async def delete_document(
        db: AsyncSession, workspace_id: uuid.UUID, doc_id: uuid.UUID
    ) -> None:
        doc = await db.get(BrandDocument, doc_id)
        if not doc or doc.workspace_id != workspace_id:
            raise ValueError("Document not found")
        await db.delete(doc)
        await db.commit()

    @staticmethod
    async def query_knowledge_base(
        db: AsyncSession, workspace_id: uuid.UUID, query: str, limit: int = 5
    ) -> BrandQueryResponse:
        docs = await BrandService.get_documents(db, workspace_id)
        profile = await BrandService.get_profile(db, workspace_id)

        relevant = []
        q_lower = query.lower()
        for d in docs:
            score = 0
            text = (d.title + " " + (d.content or "")).lower()
            for word in q_lower.split():
                if word in text:
                    score += 1
            relevant.append({"id": str(d.id), "title": d.title, "content": (d.content or "")[:500], "score": score})

        relevant.sort(key=lambda x: x["score"], reverse=True)
        top_docs = relevant[:limit]

        context_lines = []
        if profile:
            context_lines.append(f"Company: {profile.company_name}. Voice: {profile.brand_voice}.")
        for td in top_docs:
            context_lines.append(f"[{td['title']}]: {td['content']}")

        return BrandQueryResponse(
            query=query,
            context="\n".join(context_lines),
            relevant_documents=top_docs,
        )


brand_service = BrandService()
