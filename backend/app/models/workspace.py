from __future__ import annotations

"""Workspace and organisation models."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Organization(Base):
    """Top-level billing entity that owns one or more workspaces."""

    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    subscription_plan: Mapped[str] = mapped_column(String(50), default="starter", nullable=False)
    subscription_status: Mapped[str] = mapped_column(
        String(50), default="trialing", nullable=False
    )
    subscription_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    max_workspaces: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    workspaces: Mapped[list["Workspace"]] = relationship(
        "Workspace", back_populates="organization", lazy="selectin"
    )
    members: Mapped[list["OrgMember"]] = relationship(
        "OrgMember", back_populates="organization", lazy="selectin"
    )
    owner: Mapped["User"] = relationship(  # noqa: F821
        "User", foreign_keys=[owner_id], lazy="selectin"
    )


class OrgMember(Base):
    """Membership linking a user to an organisation with a role."""

    __tablename__ = "org_members"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # owner, admin, member

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="members", lazy="selectin"
    )
    user: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="org_memberships", lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("org_id", "user_id", name="uq_org_member"),
    )


class Workspace(Base):
    """A project workspace within an organisation."""

    __tablename__ = "workspaces"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="workspaces", lazy="selectin"
    )
    members: Mapped[list["WorkspaceMember"]] = relationship(
        "WorkspaceMember", back_populates="workspace", lazy="selectin"
    )
    brand_profile: Mapped["BrandProfile | None"] = relationship(  # noqa: F821
        "BrandProfile", back_populates="workspace", uselist=False, lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("org_id", "slug", name="uq_workspace_org_slug"),
    )


class WorkspaceMember(Base):
    """Membership linking a user to a workspace with a role."""

    __tablename__ = "workspace_members"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # owner, admin, editor, viewer

    # Relationships
    workspace: Mapped["Workspace"] = relationship(
        "Workspace", back_populates="members", lazy="selectin"
    )
    user: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="memberships", lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("workspace_id", "user_id", name="uq_workspace_member"),
    )
