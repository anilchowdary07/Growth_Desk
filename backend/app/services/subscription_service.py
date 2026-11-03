from __future__ import annotations

"""SaaS Subscription and Entitlement enforcement service."""

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.subscription import Plan, Subscription
from app.models.workspace import Organization


class SubscriptionService:
    @staticmethod
    async def get_plans(db: AsyncSession) -> list[Plan]:
        result = await db.execute(select(Plan).order_by(Plan.sort_order.asc()))
        plans = list(result.scalars().all())
        if not plans:
            plans = await SubscriptionService.seed_default_plans(db)
        return plans

    @staticmethod
    async def seed_default_plans(db: AsyncSession) -> list[Plan]:
        default_plans = [
            Plan(
                id=uuid.uuid4(),
                name="starter",
                display_name="Starter Workforce",
                description="Ideal for single brands, creators, and early-stage ventures.",
                price_monthly=49.0,
                price_yearly=470.0,
                limits={
                    "max_workspaces": 1,
                    "max_campaigns": 3,
                    "max_social_accounts": 3,
                    "max_monthly_posts": 60,
                    "can_access_advanced_agents": False,
                },
                features=[
                    "AI Marketing Director",
                    "Brand Brain Central Knowledge",
                    "Content Studio (Social, Blog, Scripts)",
                    "Unified Social Inbox",
                    "Multi-Channel Publishing Calendar",
                    "BYOK Model Support",
                ],
                is_active=True,
                sort_order=1,
            ),
            Plan(
                id=uuid.uuid4(),
                name="professional",
                display_name="Growth Department",
                description="For fast-scaling companies requiring full autonomous agent coordination.",
                price_monthly=149.0,
                price_yearly=1430.0,
                limits={
                    "max_workspaces": 3,
                    "max_campaigns": 20,
                    "max_social_accounts": 10,
                    "max_monthly_posts": 300,
                    "can_access_advanced_agents": True,
                },
                features=[
                    "All Starter Features",
                    "Full Suite of 10 Specialist Agents",
                    "Advanced Campaign Planning & Autonomous Execution",
                    "Lead Qualification & CRM Scoring",
                    "Competitive Market Research Agent",
                    "Performance Analytics & ROAS Diagnosis",
                    "Priority Generation Queue",
                ],
                is_active=True,
                sort_order=2,
            ),
            Plan(
                id=uuid.uuid4(),
                name="agency",
                display_name="Agency Command Center",
                description="Multi-client management with dedicated Brand Brains and approval workflows.",
                price_monthly=399.0,
                price_yearly=3830.0,
                limits={
                    "max_workspaces": 25,
                    "max_campaigns": 100,
                    "max_social_accounts": 50,
                    "max_monthly_posts": 2000,
                    "can_access_advanced_agents": True,
                },
                features=[
                    "All Professional Features",
                    "25 Client Workspaces with Strict Data Isolation",
                    "Client Approval Portal & White-Labeling Ready",
                    "Custom Agent Prompts & Workflow Triggers",
                    "Automated Weekly Client Performance Reports",
                    "Dedicated Account Architecture",
                ],
                is_active=True,
                sort_order=3,
            ),
        ]
        for p in default_plans:
            db.add(p)
        await db.commit()
        for p in default_plans:
            await db.refresh(p)
        return default_plans

    @staticmethod
    async def get_current_subscription(
        db: AsyncSession, org_id: uuid.UUID
    ) -> Subscription | None:
        result = await db.execute(
            select(Subscription)
            .options(selectinload(Subscription.plan))
            .where(Subscription.org_id == org_id)
        )
        sub = result.scalar_one_or_none()
        if not sub:
            # Create starter sub
            plans = await SubscriptionService.get_plans(db)
            starter = next((p for p in plans if p.name == "starter"), plans[0])
            sub = Subscription(
                id=uuid.uuid4(),
                org_id=org_id,
                plan_id=starter.id,
                status="active",
            )
            db.add(sub)
            await db.commit()
            await db.refresh(sub)
            sub.plan = starter
        return sub

    @staticmethod
    async def upgrade_plan(
        db: AsyncSession, org_id: uuid.UUID, plan_name: str
    ) -> Subscription:
        plans = await SubscriptionService.get_plans(db)
        target_plan = next((p for p in plans if p.name == plan_name), None)
        if not target_plan:
            raise ValueError(f"Plan {plan_name} does not exist")

        sub = await SubscriptionService.get_current_subscription(db, org_id)
        if not sub:
            sub = Subscription(
                id=uuid.uuid4(),
                org_id=org_id,
                plan_id=target_plan.id,
                status="active",
                payment_provider="razorpay",
            )
            db.add(sub)
        else:
            sub.plan_id = target_plan.id
            sub.status = "active"
            sub.payment_provider = "razorpay"

        # Update organization max_workspaces
        org = await db.get(Organization, org_id)
        if org:
            org.subscription_plan = target_plan.name
            org.max_workspaces = target_plan.limits.get("max_workspaces", 1)

        await db.commit()
        await db.refresh(sub)
        sub.plan = target_plan
        return sub


subscription_service = SubscriptionService()

