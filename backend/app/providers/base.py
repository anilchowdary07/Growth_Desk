"""Base class for AI provider integrations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class AIMessage:
    """Represents a single message in a conversation."""

    role: str  # "system", "user", "assistant"
    content: str


@dataclass
class AIResponse:
    """Structured response from an AI provider."""

    content: str
    model: str
    provider: str
    usage: dict | None = None  # {"prompt_tokens": N, "completion_tokens": N, "total_tokens": N}
    finish_reason: str | None = None


class BaseAIProvider(ABC):
    """Base class for AI provider integrations.

    All provider implementations must inherit from this class and implement
    the abstract methods: chat, test_connection, and available_models.
    """

    provider_name: str

    def __init__(self, api_key: str, model: str | None = None, base_url: str | None = None):
        self.api_key = api_key
        self.model = model or self.default_model
        self.base_url = base_url

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Return the default model identifier for this provider."""
        ...

    @abstractmethod
    async def chat(self, messages: list[AIMessage], **kwargs) -> AIResponse:
        """Send a chat completion request.

        Args:
            messages: List of conversation messages.
            **kwargs: Additional provider-specific parameters (temperature, max_tokens, etc.).

        Returns:
            AIResponse with the generated text and metadata.
        """
        ...

    @abstractmethod
    async def test_connection(self) -> bool:
        """Test that the API key is valid and the provider is reachable.

        Returns:
            True if connection succeeds, raises otherwise.
        """
        ...

    @classmethod
    @abstractmethod
    def available_models(cls) -> list[dict]:
        """Return a list of models offered by this provider.

        Each dict should have at minimum: {"id": str, "name": str, "context_window": int}.
        """
        ...
