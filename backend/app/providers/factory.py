"""AI provider factory — create, detect, and retrieve configured providers."""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.core.encryption import decrypt_value
from app.models.ai_provider import AIProvider
from app.providers.base import BaseAIProvider

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

_PROVIDER_MAP: dict[str, type[BaseAIProvider]] | None = None


def _get_provider_map() -> dict[str, type[BaseAIProvider]]:
    """Lazily build the provider class map."""
    global _PROVIDER_MAP
    if _PROVIDER_MAP is None:
        from app.providers.anthropic_provider import AnthropicProvider
        from app.providers.fallback_provider import FallbackSimulationProvider
        from app.providers.gemini_provider import GeminiProvider
        from app.providers.openai_provider import (
            CustomOpenAIProvider,
            DeepSeekProvider,
            GroqProvider,
            MistralProvider,
            OpenAIProvider,
            OpenRouterProvider,
            PerplexityProvider,
            TogetherProvider,
            XAIProvider,
        )

        _PROVIDER_MAP = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "gemini": GeminiProvider,
            "openrouter": OpenRouterProvider,
            "deepseek": DeepSeekProvider,
            "groq": GroqProvider,
            "mistral": MistralProvider,
            "perplexity": PerplexityProvider,
            "together": TogetherProvider,
            "xai": XAIProvider,
            "custom": CustomOpenAIProvider,
            "preview_engine": FallbackSimulationProvider,
        }
    return _PROVIDER_MAP


def detect_provider_from_key(api_key: str) -> str:
    """Intelligently detect the provider type based on key prefixes.
    
    Supports:
    - Google Gemini: AIza...
    - Anthropic Claude: sk-ant-...
    - OpenRouter: sk-or-...
    - Groq: gsk_...
    - Perplexity: pplx-...
    - xAI / Grok: xai-...
    - DeepSeek: dsk-... or sk-...
    - Mistral: mistral-... or ms-...
    - OpenAI / OpenAI-Compatible: sk-...
    - Default / Any other key: custom
    """
    key = api_key.strip()
    if key.startswith("AIza"):
        return "gemini"
    if key.startswith("sk-ant-"):
        return "anthropic"
    if key.startswith("sk-or-"):
        return "openrouter"
    if key.startswith("gsk_"):
        return "groq"
    if key.startswith("pplx-"):
        return "perplexity"
    if key.startswith("xai-"):
        return "xai"
    if key.startswith("dsk-"):
        return "deepseek"
    if key.startswith("mistral-") or key.startswith("ms-"):
        return "mistral"
    if key.startswith("sk-"):
        return "openai"
    return "custom"


async def get_ai_provider(
    db: "AsyncSession",
    workspace_id: str,
    provider_type: str | None = None,
) -> BaseAIProvider:
    """Get a configured AI provider for a workspace.

    1. Checks for workspace-configured provider in database.
    2. Falls back to environment variables (OPENAI_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY, etc.).
    3. Falls back to FallbackSimulationProvider so the workspace never crashes.
    """
    query = select(AIProvider).where(
        AIProvider.workspace_id == workspace_id,
        AIProvider.is_active.is_(True),
    )

    if provider_type and provider_type != "auto":
        query = query.where(AIProvider.provider_type == provider_type)
    else:
        query = query.order_by(AIProvider.is_default.desc())

    result = await db.execute(query)
    provider_row = result.scalars().first()

    if provider_row:
        try:
            api_key = decrypt_value(provider_row.encrypted_api_key)
            return create_provider(
                provider_type=provider_row.provider_type,
                api_key=api_key,
                model=provider_row.default_model,
                base_url=provider_row.base_url,
            )
        except Exception as e:
            logger.error(f"Error decrypting or loading provider {provider_row.id}: {e}")

    # Fallback to Environment Variables
    env_keys = [
        ("gemini", os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")),
        ("openai", os.getenv("OPENAI_API_KEY")),
        ("anthropic", os.getenv("ANTHROPIC_API_KEY")),
        ("openrouter", os.getenv("OPENROUTER_API_KEY")),
        ("deepseek", os.getenv("DEEPSEEK_API_KEY")),
        ("groq", os.getenv("GROQ_API_KEY")),
        ("mistral", os.getenv("MISTRAL_API_KEY")),
        ("perplexity", os.getenv("PERPLEXITY_API_KEY")),
        ("together", os.getenv("TOGETHER_API_KEY")),
        ("xai", os.getenv("XAI_API_KEY")),
    ]
    for p_type, key in env_keys:
        if key and len(key.strip()) > 5:
            return create_provider(provider_type=p_type, api_key=key.strip())

    # Fallback simulation provider for safe, crash-free preview
    from app.providers.fallback_provider import FallbackSimulationProvider
    return FallbackSimulationProvider(api_key="preview", model="growthdesk-strategy-v1")


def create_provider(
    provider_type: str,
    api_key: str,
    model: str | None = None,
    base_url: str | None = None,
) -> BaseAIProvider:
    """Create a provider instance directly for any API key."""
    if not provider_type or provider_type == "auto":
        provider_type = detect_provider_from_key(api_key)

    provider_map = _get_provider_map()
    cls = provider_map.get(provider_type.lower())

    if not cls:
        # If unknown provider name, treat as OpenAI-compatible with optional base_url
        from app.providers.openai_provider import CustomOpenAIProvider
        return CustomOpenAIProvider(api_key=api_key, model=model, base_url=base_url)

    from app.providers.openai_provider import OpenAIProvider
    if issubclass(cls, OpenAIProvider) and base_url:
        return cls(api_key=api_key, model=model, base_url=base_url)

    return cls(api_key=api_key, model=model)
