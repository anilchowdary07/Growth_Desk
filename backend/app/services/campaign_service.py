from __future__ import annotations

"""Campaign management service — goals to multi-channel execution."""

import json
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agents.orchestrator import orchestrator
from app.models.campaign import Campaign, CampaignTask
from app.schemas.campaign import CampaignCreate, CampaignTaskCreate, CampaignTaskUpdate, CampaignUpdate


class CampaignService:
    @staticmethod
    async def get_campaigns(
        db: AsyncSession, workspace_id: uuid.UUID, status: str | None = None
    ) -> list[Campaign]:
        query = (
            select(Campaign)
            .options(selectinload(Campaign.tasks))
            .where(Campaign.workspace_id == workspace_id)
            .order_by(Campaign.created_at.desc())
        )
        if status:
            query = query.where(Campaign.status == status)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_campaign(
        db: AsyncSession, workspace_id: uuid.UUID, campaign_id: uuid.UUID
    ) -> Campaign | None:
        result = await db.execute(
            select(Campaign)
            .options(selectinload(Campaign.tasks))
            .where(Campaign.id == campaign_id, Campaign.workspace_id == workspace_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_campaign(
        db: AsyncSession, workspace_id: uuid.UUID, user_id: uuid.UUID, data: CampaignCreate
    ) -> Campaign:
        campaign = Campaign(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            title=data.title,
            objective=data.objective,
            description=data.description,
            status="planning",
            target_audience=data.target_audience,
            start_date=data.start_date,
            end_date=data.end_date,
            budget=data.budget,
            kpi_targets=data.kpi_targets or {"leads": 50, "impressions": 20000},
            created_by=user_id,
        )
        db.add(campaign)
        await db.commit()
        await db.refresh(campaign)
        return campaign

    @staticmethod
    async def generate_campaign_plan(
        db: AsyncSession, workspace_id: uuid.UUID, campaign_id: uuid.UUID
    ) -> Campaign:
        campaign = await CampaignService.get_campaign(db, workspace_id, campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")

        plan_prompt = (
            f"You are the AI Marketing Director. Formulate a complete campaign strategy for this objective:\n"
            f"Title: {campaign.title}\n"
            f"Objective: {campaign.objective}\n"
            f"Target Audience: {campaign.target_audience or 'General target market'}\n"
            f"Budget: ${campaign.budget or 1000}\n\n"
            f"Provide:\n"
            f"1. Executive Summary & Core Angle\n"
            f"2. Phase 1 (Week 1): Awareness & Content Blitz\n"
            f"3. Phase 2 (Weeks 2-3): Engagement & Lead Magnets\n"
            f"4. Phase 3 (Week 4): Retargeting & Direct Conversion\n"
            f"5. Key KPI Benchmarks"
        )

        agent_result = await orchestrator.chat(
            db=db,
            workspace_id=workspace_id,
            user_message=plan_prompt,
            target_agent="director",
        )

        campaign.strategy = {
            "summary": agent_result.response,
            "generated_by": agent_result.agent_name,
            "metadata": agent_result.metadata,
        }
        campaign.status = "active"

        # Create 4 core tasks
        default_tasks = [
            ("Develop Brand Positioning & Hook Framework", "brand_strategist", "research"),
            ("Generate 10 Multi-Platform Social Media Posts", "content_creator", "content"),
            ("Design Creative Visual Concepts & Prompts", "creative_director", "creative"),
            ("Publishing Schedule & Distribution Setup", "social_manager", "publish"),
        ]

        for title, agent, task_type in default_tasks:
            task = CampaignTask(
                id=uuid.uuid4(),
                campaign_id=campaign.id,
                title=title,
                task_type=task_type,
                status="pending",
                assigned_agent=agent,
            )
            db.add(task)

        await db.commit()
        await db.refresh(campaign)
        return campaign

    @staticmethod
    async def update_campaign(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        campaign_id: uuid.UUID,
        data: CampaignUpdate,
    ) -> Campaign:
        campaign = await CampaignService.get_campaign(db, workspace_id, campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(campaign, field, value)

        await db.commit()
        await db.refresh(campaign)
        return campaign

    @staticmethod
    async def add_task(
        db: AsyncSession, campaign_id: uuid.UUID, data: CampaignTaskCreate
    ) -> CampaignTask:
        task = CampaignTask(
            id=uuid.uuid4(),
            campaign_id=campaign_id,
            title=data.title,
            description=data.description,
            task_type=data.task_type,
            status="pending",
            assigned_agent=data.assigned_agent,
            due_date=data.due_date,
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def update_task(
        db: AsyncSession, task_id: uuid.UUID, data: CampaignTaskUpdate
    ) -> CampaignTask:
        task = await db.get(CampaignTask, task_id)
        if not task:
            raise ValueError("Task not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(task, field, value)
        if data.status == "completed" and not task.completed_at:
            task.completed_at = datetime.utcnow()

        await db.commit()
        await db.refresh(task)
        return task


campaign_service = CampaignService()

