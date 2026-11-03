from __future__ import annotations

"""Workspace and Member management service."""

import re
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.workspace import Organization, Workspace, WorkspaceMember
from app.schemas.workspace import InviteMember, WorkspaceCreate, WorkspaceUpdate


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text) or "workspace"


class WorkspaceService:
    @staticmethod
    async def get_user_workspaces(db: AsyncSession, user_id: uuid.UUID) -> list[Workspace]:
        result = await db.execute(
            select(Workspace)
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(WorkspaceMember.user_id == user_id, Workspace.is_active.is_(True))
            .order_by(Workspace.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_workspace(db: AsyncSession, workspace_id: uuid.UUID) -> Workspace | None:
        result = await db.execute(
            select(Workspace)
            .options(selectinload(Workspace.members))
            .where(Workspace.id == workspace_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_workspace(
        db: AsyncSession, user: User, data: WorkspaceCreate
    ) -> Workspace:
        # Find user's organization
        member_res = await db.execute(
            select(WorkspaceMember)
            .join(Workspace)
            .where(WorkspaceMember.user_id == user.id)
            .limit(1)
        )
        existing_member = member_res.scalar_one_or_none()
        if not existing_member:
            raise ValueError("User does not have an active organization")

        ws = await db.get(Workspace, existing_member.workspace_id)
        org_id = ws.org_id

        slug = f"{_slugify(data.name)}-{str(uuid.uuid4())[:6]}"
        workspace = Workspace(
            id=uuid.uuid4(),
            org_id=org_id,
            name=data.name,
            slug=slug,
            description=data.description,
            is_active=True,
        )
        db.add(workspace)
        await db.flush()

        member = WorkspaceMember(
            id=uuid.uuid4(),
            workspace_id=workspace.id,
            user_id=user.id,
            role="owner",
        )
        db.add(member)
        await db.commit()
        await db.refresh(workspace)
        return workspace

    @staticmethod
    async def update_workspace(
        db: AsyncSession, workspace_id: uuid.UUID, data: WorkspaceUpdate
    ) -> Workspace:
        workspace = await db.get(Workspace, workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")
        if data.name is not None:
            workspace.name = data.name
        if data.description is not None:
            workspace.description = data.description
        if data.is_active is not None:
            workspace.is_active = data.is_active
        await db.commit()
        await db.refresh(workspace)
        return workspace

    @staticmethod
    async def get_workspace_members(
        db: AsyncSession, workspace_id: uuid.UUID
    ) -> list[WorkspaceMember]:
        result = await db.execute(
            select(WorkspaceMember)
            .options(selectinload(WorkspaceMember.user))
            .where(WorkspaceMember.workspace_id == workspace_id)
        )
        return list(result.scalars().all())

    @staticmethod
    async def invite_member(
        db: AsyncSession, workspace_id: uuid.UUID, data: InviteMember
    ) -> WorkspaceMember:
        user_res = await db.execute(select(User).where(User.email == data.email.lower()))
        target_user = user_res.scalar_one_or_none()
        if not target_user:
            raise ValueError(f"No registered user found with email {data.email}")

        # Check existing
        existing_res = await db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == target_user.id,
            )
        )
        if existing_res.scalar_one_or_none():
            raise ValueError("User is already a member of this workspace")

        member = WorkspaceMember(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            user_id=target_user.id,
            role=data.role,
        )
        db.add(member)
        await db.commit()
        await db.refresh(member)
        return member

    @staticmethod
    async def remove_member(
        db: AsyncSession, workspace_id: uuid.UUID, member_id: uuid.UUID
    ) -> None:
        member = await db.get(WorkspaceMember, member_id)
        if not member or member.workspace_id != workspace_id:
            raise ValueError("Membership record not found")
        if member.role == "owner":
            raise ValueError("Cannot remove workspace owner")
        await db.delete(member)
        await db.commit()


workspace_service = WorkspaceService()

