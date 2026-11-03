"""Anthropic (Claude) provider implementation."""

from __future__ import annotations

import logging

import httpx

from app.providers.base import AIMessage, AIResponse, BaseAIProvider

logger = logging.getLogger(__name__)

_ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"
_ANTHROPIC_VERSION = "2023-06-01"


class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude provider."""

    provider_name = "anthropic"

    @property
    def default_model(self) -> str:
        return "claude-sonnet-4-20250514"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "claude-sonnet-4-20250514", "name": "Claude Sonnet 4", "context_window": 200_000},
            {"id": "claude-3.5-haiku", "name": "Claude 3.5 Haiku", "context_window": 200_000},
        ]

    async def chat(self, messages: list[AIMessage], **kwargs) -> AIResponse:
        """Send a chat request to the Anthropic Messages API.

        Anthropic requires the system prompt to be passed as a top-level
        ``system`` parameter rather than as a message with role "system".
        """
        system_parts: list[str] = []
        conversation: list[dict] = []

        for msg in messages:
            if msg.role == "system":
                system_parts.append(msg.content)
            else:
                conversation.append({"role": msg.role, "content": msg.content})

        # Anthropic requires the conversation to start with a "user" message.
        # If we only received system messages, create a minimal user turn.
        if not conversation:
            conversation.append({"role": "user", "content": "Hello"})

        payload: dict = {
            "model": self.model,
            "messages": conversation,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }
        if system_parts:
            payload["system"] = "\n\n".join(system_parts)
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "top_p" in kwargs:
            payload["top_p"] = kwargs["top_p"]

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": _ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(_ANTHROPIC_MESSAGES_URL, json=payload, headers=headers)
            self._handle_error(response)
            data = response.json()

        # Anthropic returns content as a list of blocks.
        content_blocks = data.get("content", [])
        text_parts = [b["text"] for b in content_blocks if b.get("type") == "text"]
        content = "\n".join(text_parts) if text_parts else ""

        usage_data = data.get("usage")

        return AIResponse(
            content=content,
            model=data.get("model", self.model),
            provider=self.provider_name,
            usage={
                "prompt_tokens": usage_data.get("input_tokens", 0),
                "completion_tokens": usage_data.get("output_tokens", 0),
                "total_tokens": usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0),
            }
            if usage_data
            else None,
            finish_reason=data.get("stop_reason"),
        )

    async def test_connection(self) -> bool:
        """Send a minimal request to verify the API key."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": _ANTHROPIC_VERSION,
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Hi"}],
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(_ANTHROPIC_MESSAGES_URL, json=payload, headers=headers)
            self._handle_error(response)
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _handle_error(response: httpx.Response) -> None:
        """Raise descriptive errors for Anthropic failure modes."""
        if response.status_code == 401:
            raise ValueError("Invalid Anthropic API key.")
        if response.status_code == 429:
            raise ValueError("Anthropic rate limit exceeded. Please try again later.")
        if response.status_code == 404:
            raise ValueError("Requested model not available on your Anthropic plan.")
        response.raise_for_status()
