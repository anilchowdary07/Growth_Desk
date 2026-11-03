"""AI provider factory — create and retrieve configured providers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.core.encryption import decrypt_value
from app.models.ai_provider import AIProvider
from app.providers.base import BaseAIProvider

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

# Late imports to avoid circular references at module level.
_PROVIDER_MAP: dict[str, type[BaseAIProvider]] | None = None


def _get_provider_map() -> dict[str, type[BaseAIProvider]]:
    """Lazily build the provider class map."""
    global _PROVIDER_MAP
    if _PROVIDER_MAP is None:
        from app.providers.anthropic_provider import AnthropicProvider
        from app.providers.gemini_provider import GeminiProvider
        from app.providers.openai_provider import OpenAIProvider

        _PROVIDER_MAP = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "gemini": GeminiProvider,
        }
    return _PROVIDER_MAP


async def get_ai_provider(
    db: "AsyncSession",
    workspace_id: str,
    provider_type: str | None = None,
) -> BaseAIProvider:
    """Get a configured AI provider for a workspace.

    If *provider_type* is ``None``, the workspace's default provider is used.

    Args:
        db: Database session.
        workspace_id: The owning workspace ID.
        provider_type: Optional specific provider type (e.g. ``"openai"``).

    Returns:
        An instantiated provider ready for use.

    Raises:
        ValueError: If no provider is configured or the type is unknown.
    """
    query = select(AIProvider).where(
        AIProvider.workspace_id == workspace_id,
        AIProvider.is_active.is_(True),
    )

    if provider_type:
        query = query.where(AIProvider.provider_type == provider_type)
    else:
        # Prefer the workspace default, fall back to any active provider.
        query = query.order_by(AIProvider.is_default.desc())

    result = await db.execute(query)
    provider_row = result.scalars().first()

    if not provider_row:
        raise ValueError(
            "No AI provider configured for this workspace. "
            "Please add a provider under Settings → AI Providers."
        )

    api_key = decrypt_value(provider_row.encrypted_api_key)
    return create_provider(
        provider_type=provider_row.provider_type,
        api_key=api_key,
        model=provider_row.default_model,
    )


def create_provider(
    provider_type: str,
    api_key: str,
    model: str | None = None,
) -> BaseAIProvider:
    """Create a provider instance directly (without DB lookup).

    Args:
        provider_type: One of ``"openai"``, ``"anthropic"``, ``"gemini"``.
        api_key: The raw (decrypted) API key.
        model: Optional model override.

    Returns:
        An instantiated provider.

    Raises:
        ValueError: If *provider_type* is not recognised.
    """
    provider_map = _get_provider_map()
    cls = provider_map.get(provider_type)
    if not cls:
        raise ValueError(f"Unknown provider type: {provider_type!r}. Available: {list(provider_map)}")
    return cls(api_key=api_key, model=model)
