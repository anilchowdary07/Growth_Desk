from __future__ import annotations

"""AI Provider management service (BYOK)."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.encryption import encrypt_value
from app.models.ai_provider import AIProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.factory import create_provider
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider
from app.schemas.ai_provider import AIProviderCreate, AIProviderTestResult, AIProviderUpdate, ModelInfo


class AIProviderService:
    @staticmethod
    async def get_providers(db: AsyncSession, workspace_id: uuid.UUID) -> list[AIProvider]:
        result = await db.execute(
            select(AIProvider)
            .where(AIProvider.workspace_id == workspace_id)
            .order_by(AIProvider.is_default.desc(), AIProvider.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_provider(
        db: AsyncSession, workspace_id: uuid.UUID, provider_id: uuid.UUID
    ) -> AIProvider | None:
        result = await db.execute(
            select(AIProvider).where(
                AIProvider.id == provider_id, AIProvider.workspace_id == workspace_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def add_provider(
        db: AsyncSession, workspace_id: uuid.UUID, data: AIProviderCreate
    ) -> AIProvider:
        # Check if one already exists for this provider_type in workspace
        existing = await db.execute(
            select(AIProvider).where(
                AIProvider.workspace_id == workspace_id,
                AIProvider.provider_type == data.provider_type,
            )
        )
        row = existing.scalar_one_or_none()

        encrypted_key = encrypt_value(data.api_key.strip())
        display_name = data.display_name or data.provider_type.capitalize()

        if data.is_default:
            # Demote others
            await db.execute(
                update(AIProvider)
                .where(AIProvider.workspace_id == workspace_id)
                .values(is_default=False)
            )

        if row:
            row.encrypted_api_key = encrypted_key
            row.display_name = display_name
            row.default_model = data.default_model
            row.is_active = True
            if data.is_default:
                row.is_default = True
            await db.commit()
            await db.refresh(row)
            return row

        # Check if first provider in workspace -> make default
        count_res = await db.execute(
            select(AIProvider).where(AIProvider.workspace_id == workspace_id)
        )
        first_one = len(count_res.scalars().all()) == 0

        provider = AIProvider(
            id=uuid.uuid4(),
            workspace_id=workspace_id,
            provider_type=data.provider_type,
            encrypted_api_key=encrypted_key,
            display_name=display_name,
            default_model=data.default_model,
            is_active=True,
            is_default=data.is_default or first_one,
        )
        db.add(provider)
        await db.commit()
        await db.refresh(provider)
        return provider

    @staticmethod
    async def update_provider(
        db: AsyncSession,
        workspace_id: uuid.UUID,
        provider_id: uuid.UUID,
        data: AIProviderUpdate,
    ) -> AIProvider:
        provider = await AIProviderService.get_provider(db, workspace_id, provider_id)
        if not provider:
            raise ValueError("Provider configuration not found")

        if data.api_key is not None:
            provider.encrypted_api_key = encrypt_value(data.api_key.strip())
        if data.display_name is not None:
            provider.display_name = data.display_name
        if data.default_model is not None:
            provider.default_model = data.default_model
        if data.is_active is not None:
            provider.is_active = data.is_active
        if data.is_default is True:
            await db.execute(
                update(AIProvider)
                .where(AIProvider.workspace_id == workspace_id)
                .values(is_default=False)
            )
            provider.is_default = True

        await db.commit()
        await db.refresh(provider)
        return provider

    @staticmethod
    async def delete_provider(
        db: AsyncSession, workspace_id: uuid.UUID, provider_id: uuid.UUID
    ) -> None:
        provider = await AIProviderService.get_provider(db, workspace_id, provider_id)
        if not provider:
            raise ValueError("Provider configuration not found")
        await db.delete(provider)
        await db.commit()

    @staticmethod
    async def test_provider(
        db: AsyncSession, workspace_id: uuid.UUID, provider_id: uuid.UUID
    ) -> AIProviderTestResult:
        provider = await AIProviderService.get_provider(db, workspace_id, provider_id)
        if not provider:
            raise ValueError("Provider configuration not found")

        from app.core.encryption import decrypt_value

        decrypted_key = decrypt_value(provider.encrypted_api_key)
        instance = create_provider(
            provider_type=provider.provider_type,
            api_key=decrypted_key,
            model=provider.default_model,
        )

        try:
            connected = await instance.test_connection()
            if connected:
                provider.last_verified_at = datetime.now(timezone.utc)
                await db.commit()
                return AIProviderTestResult(
                    success=True,
                    provider=provider.provider_type,
                    model=instance.model,
                    message="API connection verified successfully! Ready to operate.",
                )
            else:
                return AIProviderTestResult(
                    success=False,
                    provider=provider.provider_type,
                    model=instance.model,
                    message="Connection test failed. Please verify your API key and permissions.",
                )
        except Exception as e:
            return AIProviderTestResult(
                success=False,
                provider=provider.provider_type,
                model=instance.model,
                message=f"Connection test error: {str(e)}",
            )

    @staticmethod
    def get_supported_models() -> list[ModelInfo]:
        models = []
        for m in OpenAIProvider.available_models():
            models.append(
                ModelInfo(
                    id=m["id"],
                    name=m["name"],
                    provider="openai",
                    context_window=m.get("context_window"),
                    cost_tier="$$$" if "o1" in m["id"] or "4o" == m["id"] else "$",
                    supports_vision=m.get("supports_vision", True),
                )
            )
        for m in AnthropicProvider.available_models():
            models.append(
                ModelInfo(
                    id=m["id"],
                    name=m["name"],
                    provider="anthropic",
                    context_window=m.get("context_window"),
                    cost_tier="$$$" if "opus" in m["id"] else "$$",
                    supports_vision=m.get("supports_vision", True),
                )
            )
        for m in GeminiProvider.available_models():
            models.append(
                ModelInfo(
                    id=m["id"],
                    name=m["name"],
                    provider="gemini",
                    context_window=m.get("context_window"),
                    cost_tier="$$" if "pro" in m["id"] else "$",
                    supports_vision=m.get("supports_vision", True),
                )
            )
        return models


ai_provider_service = AIProviderService()
