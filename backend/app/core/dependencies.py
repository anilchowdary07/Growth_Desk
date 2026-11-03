from __future__ import annotations

"""FastAPI dependencies for authentication, workspace resolution, and role checks."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_access_token
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ---------------------------------------------------------------------------
# Current authenticated user
# ---------------------------------------------------------------------------


async def get_current_user(
    token: Annotated[str, Depends(_oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Decode the JWT and return the corresponding active ``User``.

    Raises 401 if the token is invalid or the user is inactive / missing.
    """
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# ---------------------------------------------------------------------------
# Current workspace (from X-Workspace-ID header)
# ---------------------------------------------------------------------------


async def get_current_workspace(
    x_workspace_id: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Workspace:
    """Resolve the workspace from the ``X-Workspace-ID`` header.

    Also verifies that the current user is a member of the workspace.
    Raises 404 if the workspace does not exist or the user is not a member.
    """
    try:
        workspace_id = UUID(x_workspace_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid workspace ID format",
        )

    result = await db.execute(select(Workspace).where(Workspace.id == workspace_id))
    workspace = result.scalar_one_or_none()

    if workspace is None or not workspace.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    # Verify membership
    membership = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id,
        )
    )
    if membership.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this workspace",
        )

    return workspace


# ---------------------------------------------------------------------------
# Workspace member (user + workspace combined)
# ---------------------------------------------------------------------------


async def get_workspace_member(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    workspace: Annotated[Workspace, Depends(get_current_workspace)],
) -> WorkspaceMember:
    """Return the ``WorkspaceMember`` record for the current user & workspace."""
    result = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace.id,
            WorkspaceMember.user_id == current_user.id,
        )
    )
    member = result.scalar_one_or_none()
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workspace membership not found",
        )
    return member


# ---------------------------------------------------------------------------
# Role-based access control
# ---------------------------------------------------------------------------

_ROLE_HIERARCHY: dict[str, int] = {
    "viewer": 0,
    "editor": 1,
    "admin": 2,
    "owner": 3,
}


def require_role(minimum_role: str):
    """Dependency factory that enforces a minimum workspace role.

    Usage::

        @router.post("/dangerous")
        async def dangerous_action(
            member: WorkspaceMember = Depends(require_role("admin")),
        ):
            ...
    """
    min_level = _ROLE_HIERARCHY.get(minimum_role, 0)

    async def _check(
        member: Annotated[WorkspaceMember, Depends(get_workspace_member)],
    ) -> WorkspaceMember:
        member_level = _ROLE_HIERARCHY.get(member.role, -1)
        if member_level < min_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{minimum_role}' or higher required",
            )
        return member

    return _check
