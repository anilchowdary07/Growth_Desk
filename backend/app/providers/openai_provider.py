"""OpenAI provider implementation."""

from __future__ import annotations

import logging

import httpx

from app.providers.base import AIMessage, AIResponse, BaseAIProvider

logger = logging.getLogger(__name__)

_OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIProvider(BaseAIProvider):
    """OpenAI ChatCompletion provider (GPT-4o family)."""

    provider_name = "openai"

    @property
    def default_model(self) -> str:
        return "gpt-4o"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "gpt-4o", "name": "GPT-4o", "context_window": 128_000},
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "context_window": 128_000},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "context_window": 128_000},
            {"id": "o1", "name": "o1", "context_window": 200_000},
            {"id": "o1-mini", "name": "o1 Mini", "context_window": 128_000},
        ]

    async def chat(self, messages: list[AIMessage], **kwargs) -> AIResponse:
        """Send a chat completion request to OpenAI.

        Args:
            messages: Conversation messages.
            **kwargs: Extra params forwarded to the API (temperature, max_tokens, etc.).

        Returns:
            AIResponse with generated content.

        Raises:
            httpx.HTTPStatusError: On non-2xx responses.
            ValueError: On unexpected response structure.
        """
        payload: dict = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
        # Forward optional parameters
        for key in ("temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"):
            if key in kwargs:
                payload[key] = kwargs[key]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(_OPENAI_CHAT_URL, json=payload, headers=headers)
            self._handle_error(response)
            data = response.json()

        choice = data["choices"][0]
        usage = data.get("usage")

        return AIResponse(
            content=choice["message"]["content"],
            model=data.get("model", self.model),
            provider=self.provider_name,
            usage={
                "prompt_tokens": usage["prompt_tokens"],
                "completion_tokens": usage["completion_tokens"],
                "total_tokens": usage["total_tokens"],
            }
            if usage
            else None,
            finish_reason=choice.get("finish_reason"),
        )

    async def test_connection(self) -> bool:
        """Validate the API key by listing models."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get("https://api.openai.com/v1/models", headers=headers)
            self._handle_error(response)
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _handle_error(response: httpx.Response) -> None:
        """Raise descriptive errors for common OpenAI failure modes."""
        if response.status_code == 401:
            raise ValueError("Invalid OpenAI API key.")
        if response.status_code == 429:
            raise ValueError("OpenAI rate limit exceeded. Please try again later.")
        if response.status_code == 404:
            raise ValueError("Requested model not available on your OpenAI plan.")
        response.raise_for_status()
