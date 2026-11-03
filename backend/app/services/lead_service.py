from __future__ import annotations

"""Lead Generation and CRM service."""

import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.lead import Lead, LeadActivity
from app.schemas.lead import LeadActivityCreate, LeadCreate, LeadUpdate


class LeadService:
    @staticmethod
    async def get_leads(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        status: str | None = None,
        source: str | None = None,
    ) -> list[Lead]:
        query = (
            select(Lead)
            .options(selectinload(Lead.activities))
            .where(Lead.workspace_id == workspace_id)
            .order_by(Lead.score.desc().nullslast(), Lead.created_at.desc())
        )
        if status:
            query = query.where(Lead.status == status)
        if source:
            query = query.where(Lead.source == source)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_lead(
        db: AsyncSession, workspace_id: uuid.UUID, lead_id: uuid.UUID
    ) -> Lead | None:
        result = await db.execute(
            select(Lead)
            .options(selectinload(Lead.activities))
            .where(Lead.id == lead_id, Lead.workspace_id == workspace_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_lead(
        db: AsyncSession, workspace_id: uuid.UUID, data: LeadCreate
    ) -> Lead:
        lead = Lead(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            company=data.company,
            source=data.source,
            source_conversation_id=data.source_conversation_id,
            status=data.status,
            score=data.score or 50,
            tags=data.tags or [],
            notes=data.notes,
            custom_fields=data.custom_fields or {},
        )
        db.add(lead)
        await db.flush()

        activity = LeadActivity(
            id=uuid.uuid4(),
            lead_id=lead.id,
            activity_type="created",
            description="Lead captured into system",
            performed_by="user",
        )
        db.add(activity)

        await db.commit()
        await db.refresh(lead)
        return lead

    @staticmethod
    async def update_lead(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        lead_id: uuid.UUID,
        data: LeadUpdate,
    ) -> Lead:
        lead = await LeadService.get_lead(db, workspace_id, lead_id)
        if not lead:
            raise ValueError("Lead not found")

        old_status = lead.status

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(lead, field, value)

        if data.status and data.status != old_status:
            if data.status == "converted":
                lead.converted_at = datetime.utcnow()
            activity = LeadActivity(
                id=uuid.uuid4(),
                lead_id=lead.id,
                activity_type="status_changed",
                description=f"Status moved from {old_status} to {data.status}",
                performed_by="user",
            )
            db.add(activity)

        await db.commit()
        await db.refresh(lead)
        return lead

    @staticmethod
    async def add_activity(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        lead_id: uuid.UUID,
        data: LeadActivityCreate,
        performed_by: str = "user",
    ) -> LeadActivity:
        lead = await LeadService.get_lead(db, workspace_id, lead_id)
        if not lead:
            raise ValueError("Lead not found")

        activity = LeadActivity(
            id=uuid.uuid4(),
            lead_id=lead.id,
            activity_type=data.activity_type,
            description=data.description,
            metadata_json=data.metadata_json,
            performed_by=performed_by,
        )
        db.add(activity)
        await db.commit()
        await db.refresh(activity)
        return activity

    @staticmethod
    async def delete_lead(
        db: AsyncSession, workspace_id: uuid.UUID, lead_id: uuid.UUID
    ) -> None:
        lead = await LeadService.get_lead(db, workspace_id, lead_id)
        if not lead:
            raise ValueError("Lead not found")
        await db.delete(lead)
        await db.commit()


lead_service = LeadService()

