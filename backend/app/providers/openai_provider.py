"""OpenAI and OpenAI-compatible providers (OpenRouter, DeepSeek, Groq, Custom)."""

from __future__ import annotations

import logging
from typing import Any
import httpx

from app.providers.base import AIMessage, AIResponse, BaseAIProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI and OpenAI-compatible ChatCompletion provider."""

    provider_name = "openai"

    def __init__(
        self,
        api_key: str,
        model: str | None = None,
        base_url: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ):
        super().__init__(api_key, model, base_url)
        self.endpoint_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        self.extra_headers = extra_headers or {}

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
        payload: dict = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
        for key in ("temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"):
            if key in kwargs:
                payload[key] = kwargs[key]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            **self.extra_headers,
        }

        chat_url = f"{self.endpoint_url}/chat/completions"

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(chat_url, json=payload, headers=headers)
            self._handle_error(response)
            data = response.json()

        choice = data["choices"][0]
        usage = data.get("usage")

        return AIResponse(
            content=choice["message"]["content"],
            model=data.get("model", self.model),
            provider=self.provider_name,
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            }
            if usage
            else None,
            finish_reason=choice.get("finish_reason"),
        )

    async def test_connection(self) -> bool:
        """Validate the API key by querying models endpoint or sending test token."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            **self.extra_headers,
        }
        test_url = f"{self.endpoint_url}/models"
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.get(test_url, headers=headers)
                if response.status_code in (200, 201):
                    return True
                # If models endpoint isn't supported, try a minimal completion
                if response.status_code == 404:
                    comp_res = await client.post(
                        f"{self.endpoint_url}/chat/completions",
                        json={"model": self.model, "messages": [{"role": "user", "content": "hi"}], "max_tokens": 1},
                        headers={"Content-Type": "application/json", **headers},
                    )
                    return comp_res.status_code in (200, 201)
                self._handle_error(response)
                return True
            except Exception as e:
                logger.warning(f"Connection test error for {self.provider_name}: {e}")
                raise

    @staticmethod
    def _handle_error(response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ValueError("Invalid API key or unauthorized access.")
        if response.status_code == 429:
            raise ValueError("API rate limit or quota exceeded. Please check your provider account credits.")
        if response.status_code == 404:
            raise ValueError("Requested model or endpoint not found on this provider.")
        response.raise_for_status()


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter provider — supports 200+ models via unified API."""

    provider_name = "openrouter"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key,
            model=model or "meta-llama/llama-3.3-70b-instruct",
            base_url=base_url or "https://openrouter.ai/api/v1",
            extra_headers={
                "HTTP-Referer": "https://growthdesk.io",
                "X-Title": "AI GrowthDesk",
            },
        )

    @property
    def default_model(self) -> str:
        return "meta-llama/llama-3.3-70b-instruct"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "meta-llama/llama-3.3-70b-instruct", "name": "Llama 3.3 70B (OpenRouter)", "context_window": 128_000},
            {"id": "deepseek/deepseek-chat", "name": "DeepSeek V3 (OpenRouter)", "context_window": 64_000},
            {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet (OpenRouter)", "context_window": 200_000},
            {"id": "openai/gpt-4o", "name": "GPT-4o (OpenRouter)", "context_window": 128_000},
            {"id": "google/gemini-2.0-flash-001", "name": "Gemini 2.0 Flash (OpenRouter)", "context_window": 1_000_000},
        ]


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek official API provider."""

    provider_name = "deepseek"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key,
            model=model or "deepseek-chat",
            base_url=base_url or "https://api.deepseek.com/v1",
        )

    @property
    def default_model(self) -> str:
        return "deepseek-chat"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "deepseek-chat", "name": "DeepSeek V3 Chat", "context_window": 64_000},
            {"id": "deepseek-reasoner", "name": "DeepSeek R1 Reasoner", "context_window": 64_000},
        ]


class GroqProvider(OpenAIProvider):
    """Groq ultra-fast LPU inference provider."""

    provider_name = "groq"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key,
            model=model or "llama-3.3-70b-versatile",
            base_url=base_url or "https://api.groq.com/openai/v1",
        )

    @property
    def default_model(self) -> str:
        return "llama-3.3-70b-versatile"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "llama-3.3-70b-versatile", "name": "Llama 3.3 70B (Groq)", "context_window": 128_000},
            {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B (Groq)", "context_window": 32_768},
            {"id": "deepseek-r1-distill-llama-70b", "name": "DeepSeek R1 70B (Groq)", "context_window": 128_000},
        ]


class MistralProvider(OpenAIProvider):
    """Mistral AI official API provider."""

    provider_name = "mistral"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key,
            model=model or "mistral-large-latest",
            base_url=base_url or "https://api.mistral.ai/v1",
        )

    @property
    def default_model(self) -> str:
        return "mistral-large-latest"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "mistral-large-latest", "name": "Mistral Large", "context_window": 128_000},
            {"id": "mistral-small-latest", "name": "Mistral Small", "context_window": 128_000},
            {"id": "codestral-latest", "name": "Codestral", "context_window": 256_000},
            {"id": "open-mistral-nemo", "name": "Mistral Nemo", "context_window": 128_000},
        ]


class PerplexityProvider(OpenAIProvider):
    """Perplexity AI online search & reasoning provider."""

    provider_name = "perplexity"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key,
            model=model or "sonar-pro",
            base_url=base_url or "https://api.perplexity.ai",
        )

    @property
    def default_model(self) -> str:
        return "sonar-pro"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "sonar-pro", "name": "Sonar Pro (Search-Grounded)", "context_window": 200_000},
            {"id": "sonar", "name": "Sonar (Fast Search)", "context_window": 128_000},
            {"id": "sonar-reasoning", "name": "Sonar Reasoning (Deep Research)", "context_window": 128_000},
        ]


class TogetherProvider(OpenAIProvider):
    """Together AI open-source model inference provider."""

    provider_name = "together"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key,
            model=model or "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            base_url=base_url or "https://api.together.xyz/v1",
        )

    @property
    def default_model(self) -> str:
        return "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "name": "Llama 3.1 70B Turbo", "context_window": 131_072},
            {"id": "deepseek-ai/DeepSeek-R1", "name": "DeepSeek R1 (Together)", "context_window": 64_000},
            {"id": "Qwen/Qwen2.5-72B-Instruct-Turbo", "name": "Qwen 2.5 72B Turbo", "context_window": 131_072},
        ]


class XAIProvider(OpenAIProvider):
    """xAI (Grok) official API provider."""

    provider_name = "xai"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key,
            model=model or "grok-2-latest",
            base_url=base_url or "https://api.x.ai/v1",
        )

    @property
    def default_model(self) -> str:
        return "grok-2-latest"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "grok-2-latest", "name": "Grok 2", "context_window": 128_000},
            {"id": "grok-beta", "name": "Grok Beta", "context_window": 128_000},
        ]


class CustomOpenAIProvider(OpenAIProvider):
    """Custom / Local OpenAI-compatible provider (e.g. Ollama, vLLM, LMStudio, Mistral, Together)."""

    provider_name = "custom"

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key or "local-key",
            model=model or "default",
            base_url=base_url or "http://localhost:11434/v1",
        )

    @property
    def default_model(self) -> str:
        return "default"

    @classmethod
    def available_models(cls) -> list[dict]:
        return [
            {"id": "default", "name": "Custom Model (Configured by Endpoint)", "context_window": 128_000},
        ]
