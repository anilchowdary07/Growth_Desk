import pytest
from app.agents.base import AgentContext
from app.agents.orchestrator import AgentOrchestrator
from app.providers.base import AIMessage, AIResponse, BaseAIProvider


class MockProvider(BaseAIProvider):
    provider_name = "mock"

    @property
    def default_model(self) -> str:
        return "mock-model"

    async def chat(self, messages: list[AIMessage], **kwargs) -> AIResponse:
        return AIResponse(
            content="Mock strategic recommendation for your campaign.",
            model="mock-model",
            provider="mock",
            usage={"total_tokens": 100},
        )

    async def test_connection(self) -> bool:
        return True

    @classmethod
    def available_models(cls) -> list[dict]:
        return [{"id": "mock-model", "name": "Mock Model"}]


@pytest.mark.asyncio
async def test_orchestrator_agents_list():
    orchestrator = AgentOrchestrator()
    expected_agents = [
        "director",
        "research",
        "brand_strategist",
        "content_creator",
        "creative_director",
        "social_manager",
        "community_manager",
        "lead_agent",
        "advertising_agent",
        "seo_agent",
        "growth_analyst",
    ]
    for agent_name in expected_agents:
        assert agent_name in orchestrator.agents
        agent = orchestrator.agents[agent_name]
        assert len(agent.system_prompt) > 50


@pytest.mark.asyncio
async def test_agent_execution_with_mock():
    orchestrator = AgentOrchestrator()
    provider = MockProvider(api_key="mock-key")
    director = orchestrator.agents["director"]

    context = AgentContext(
        workspace_id="test-ws",
        brand_context="Brand: TechCorp. Voice: Direct, visionary.",
        user_message="Launch new SaaS product",
    )

    result = await director.execute(context, provider)
    assert result.agent_name == "director"
    assert "Mock strategic recommendation" in result.response

