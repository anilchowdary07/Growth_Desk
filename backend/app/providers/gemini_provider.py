"""Google Gemini provider implementation."""

from __future__ import annotations

import logging

import httpx

from app.providers.base import AIMessage, AIResponse, BaseAIProvider

logger = logging.getLogger(__name__)

_GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


class GeminiProvider(BaseAIProvider):
    """Google Gemini (Generative Language API) provider."""

    provider_name = "gemini"

    @property
    def default_model(self) -> str:
        return "gemini-2.0-flash"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash", "context_window": 1_048_576},
            {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro", "context_window": 1_048_576},
            {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash", "context_window": 1_048_576},
        ]

    async def chat(self, messages: list[AIMessage], **kwargs) -> AIResponse:
        """Send a generateContent request to the Gemini API.

        Gemini uses a different message schema:
        - System instructions go into ``system_instruction``.
        - Conversation turns use ``role: "user" | "model"`` with ``parts: [{text}]``.
        """
        system_parts: list[str] = []
        contents: list[dict] = []

        for msg in messages:
            if msg.role == "system":
                system_parts.append(msg.content)
            else:
                role = "model" if msg.role == "assistant" else "user"
                contents.append({"role": role, "parts": [{"text": msg.content}]})

        if not contents:
            contents.append({"role": "user", "parts": [{"text": "Hello"}]})

        payload: dict = {"contents": contents}
        if system_parts:
            payload["system_instruction"] = {"parts": [{"text": "\n\n".join(system_parts)}]}

        generation_config: dict = {}
        if "temperature" in kwargs:
            generation_config["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            generation_config["maxOutputTokens"] = kwargs["max_tokens"]
        if "top_p" in kwargs:
            generation_config["topP"] = kwargs["top_p"]
        if generation_config:
            payload["generationConfig"] = generation_config

        url = f"{_GEMINI_BASE_URL}/models/{self.model}:generateContent"
        params = {"key": self.api_key}

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload, params=params)
            self._handle_error(response)
            data = response.json()

        # Parse response
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("Gemini returned no candidates.")

        candidate = candidates[0]
        parts = candidate.get("content", {}).get("parts", [])
        text_parts = [p["text"] for p in parts if "text" in p]
        content = "\n".join(text_parts) if text_parts else ""

        usage_meta = data.get("usageMetadata", {})

        return AIResponse(
            content=content,
            model=self.model,
            provider=self.provider_name,
            usage={
                "prompt_tokens": usage_meta.get("promptTokenCount", 0),
                "completion_tokens": usage_meta.get("candidatesTokenCount", 0),
                "total_tokens": usage_meta.get("totalTokenCount", 0),
            }
            if usage_meta
            else None,
            finish_reason=candidate.get("finishReason"),
        )

    async def test_connection(self) -> bool:
        """List models to verify the API key is valid."""
        url = f"{_GEMINI_BASE_URL}/models"
        params = {"key": self.api_key}
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params)
            self._handle_error(response)
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _handle_error(response: httpx.Response) -> None:
        """Raise descriptive errors for Gemini failure modes."""
        if response.status_code == 400:
            body = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
            msg = body.get("error", {}).get("message", "Bad request to Gemini API.")
            raise ValueError(msg)
        if response.status_code in (401, 403):
            raise ValueError("Invalid or unauthorized Gemini API key.")
        if response.status_code == 429:
            raise ValueError("Gemini rate limit exceeded. Please try again later.")
        if response.status_code == 404:
            raise ValueError("Requested Gemini model not found.")
        response.raise_for_status()
