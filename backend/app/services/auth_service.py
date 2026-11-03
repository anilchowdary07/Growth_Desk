from __future__ import annotations

"""Authentication and User management service."""

import re
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.subscription import Plan, Subscription
from app.models.user import User
from app.models.workspace import Organization, OrgMember, Workspace, WorkspaceMember
from app.schemas.auth import UserRegister, UserUpdate


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text) or "workspace"


class AuthService:
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email.lower().strip()))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def register_user(db: AsyncSession, data: UserRegister) -> tuple[User, Workspace]:
        existing = await AuthService.get_user_by_email(db, data.email)
        if existing:
            raise ValueError("A user with this email already exists")

        # Create user
        user = User(
            id=uuid.uuid4(),
            email=data.email.lower().strip(),
            full_name=data.full_name.strip(),
            hashed_password=hash_password(data.password),
            is_active=True,
        )
        db.add(user)
        await db.flush()

        # Create default organization
        org_name = data.organization_name or f"{user.full_name}'s Org"
        org_slug = f"{_slugify(org_name)}-{str(uuid.uuid4())[:8]}"
        org = Organization(
            id=uuid.uuid4(),
            name=org_name,
            slug=org_slug,
            owner_id=user.id,
            subscription_plan="starter",
            subscription_status="active",
        )
        db.add(org)
        await db.flush()

        # Org membership
        org_member = OrgMember(
            id=uuid.uuid4(),
            org_id=org.id,
            user_id=user.id,
            role="owner",
        )
        db.add(org_member)

        # Create default workspace
        ws_name = "Main Marketing Workspace"
        ws_slug = "main"
        workspace = Workspace(
            id=uuid.uuid4(),
            org_id=org.id,
            name=ws_name,
            slug=ws_slug,
            description="Default workspace for autonomous marketing operations",
            is_active=True,
        )
        db.add(workspace)
        await db.flush()

        # Workspace membership
        ws_member = WorkspaceMember(
            id=uuid.uuid4(),
            workspace_id=workspace.id,
            user_id=user.id,
            role="owner",
        )
        db.add(ws_member)

        # Assign starter plan
        plan_res = await db.execute(select(Plan).where(Plan.name == "starter"))
        starter_plan = plan_res.scalar_one_or_none()
        if starter_plan:
            sub = Subscription(
                id=uuid.uuid4(),
                org_id=org.id,
                plan_id=starter_plan.id,
                status="active",
            )
            db.add(sub)

        await db.commit()
        await db.refresh(user)
        await db.refresh(workspace)
        return user, workspace

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
        user = await AuthService.get_user_by_email(db, email)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def update_profile(db: AsyncSession, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = await AuthService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.avatar_url is not None:
            user.avatar_url = data.avatar_url
        await db.commit()
        await db.refresh(user)
        return user


auth_service = AuthService()

