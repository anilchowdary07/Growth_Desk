from __future__ import annotations

"""Brand profile, brand document, and brand embedding models."""

import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

try:
    from pgvector.sqlalchemy import Vector
except ImportError:  # pragma: no cover – optional at import time
    Vector = None  # type: ignore[assignment,misc]


class BrandProfile(Base):
    """Brand identity and voice configuration for a workspace."""

    __tablename__ = "brand_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_audience: Mapped[str | None] = mapped_column(Text, nullable=True)
    brand_voice: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tone_keywords: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    brand_colors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    website: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    products_services: Mapped[str | None] = mapped_column(Text, nullable=True)
    competitors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    restricted_topics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    content_preferences: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    faqs: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    custom_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    workspace: Mapped["Workspace"] = relationship(  # noqa: F821
        "Workspace", back_populates="brand_profile", lazy="selectin"
    )


class BrandDocument(Base):
    """An uploaded or scraped brand knowledge document."""

    __tablename__ = "brand_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    doc_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # pdf, text, image, url
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    embeddings: Mapped[list["BrandEmbedding"]] = relationship(
        "BrandEmbedding", back_populates="document", lazy="selectin"
    )


class BrandEmbedding(Base):
    """Vector embedding chunk for brand knowledge retrieval."""

    __tablename__ = "brand_embeddings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False
    )
    document_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("brand_documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(1536), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    document: Mapped["BrandDocument | None"] = relationship(
        "BrandDocument", back_populates="embeddings", lazy="selectin"
    )
