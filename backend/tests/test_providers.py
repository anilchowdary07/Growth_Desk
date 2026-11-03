import pytest
from app.providers.factory import create_provider, detect_provider_from_key
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
from app.providers.gemini_provider import GeminiProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.fallback_provider import FallbackSimulationProvider


def test_detect_provider_from_key():
    assert detect_provider_from_key("AIzaSyB_1234567890abcdef") == "gemini"
    assert detect_provider_from_key("AIzaTestKeyWithoutSy") == "gemini"
    assert detect_provider_from_key("sk-ant-api03-abcdef123456") == "anthropic"
    assert detect_provider_from_key("sk-or-v1-abcdef1234567890") == "openrouter"
    assert detect_provider_from_key("gsk_abcdef1234567890") == "groq"
    assert detect_provider_from_key("pplx-abcdef1234567890") == "perplexity"
    assert detect_provider_from_key("xai-abcdef1234567890") == "xai"
    assert detect_provider_from_key("dsk-abcdef1234567890") == "deepseek"
    assert detect_provider_from_key("mistral-abcdef123456") == "mistral"
    assert detect_provider_from_key("sk-proj-openai-key-1234") == "openai"
    assert detect_provider_from_key("any-random-arbitrary-custom-key") == "custom"


def test_create_any_provider():
    # OpenAI
    p_openai = create_provider("openai", "sk-test", model="gpt-4o")
    assert isinstance(p_openai, OpenAIProvider)
    assert p_openai.model == "gpt-4o"

    # Gemini
    p_gemini = create_provider("gemini", "AIzaSyTest", model="gemini-2.0-flash")
    assert isinstance(p_gemini, GeminiProvider)
    assert p_gemini.model == "gemini-2.0-flash"

    # Anthropic
    p_claude = create_provider("anthropic", "sk-ant-test", model="claude-3-5-sonnet")
    assert isinstance(p_claude, AnthropicProvider)
    assert p_claude.model == "claude-3-5-sonnet"

    # OpenRouter
    p_openrouter = create_provider("openrouter", "sk-or-test")
    assert isinstance(p_openrouter, OpenRouterProvider)
    assert p_openrouter.endpoint_url == "https://openrouter.ai/api/v1"

    # DeepSeek
    p_deepseek = create_provider("deepseek", "sk-deepseek")
    assert isinstance(p_deepseek, DeepSeekProvider)

    # Groq
    p_groq = create_provider("groq", "gsk_test")
    assert isinstance(p_groq, GroqProvider)

    # Mistral
    p_mistral = create_provider("mistral", "mistral-test")
    assert isinstance(p_mistral, MistralProvider)

    # Perplexity
    p_pplx = create_provider("perplexity", "pplx-test")
    assert isinstance(p_pplx, PerplexityProvider)

    # Together
    p_together = create_provider("together", "together-test")
    assert isinstance(p_together, TogetherProvider)

    # xAI
    p_xai = create_provider("xai", "xai-test")
    assert isinstance(p_xai, XAIProvider)

    # Custom OpenAI-compatible (e.g. local Ollama or vLLM)
    p_custom = create_provider(
        "custom",
        "local-token",
        model="llama3.2:latest",
        base_url="http://localhost:11434/v1",
    )
    assert isinstance(p_custom, CustomOpenAIProvider)
    assert p_custom.endpoint_url == "http://localhost:11434/v1"
    assert p_custom.model == "llama3.2:latest"

    # Auto-detection from key
    p_auto = create_provider("auto", "AIzaSyTestAuto")
    assert isinstance(p_auto, GeminiProvider)


@pytest.mark.asyncio
async def test_fallback_simulation_provider():
    fallback = FallbackSimulationProvider(api_key="preview", model="growthdesk-strategy-v1")
    assert fallback.provider_name == "preview_engine"
    assert await fallback.test_connection() is True

    from app.providers.base import AIMessage
    res = await fallback.chat([AIMessage(role="user", content="Launch a campaign")])
    assert "Strategic Analysis" in res.content
    assert res.provider == "preview_engine"
