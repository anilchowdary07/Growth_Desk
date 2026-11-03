import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "AI GrowthDesk" in data["service"]


def test_supported_models():
    response = client.get("/api/v1/ai-providers/models")
    assert response.status_code == 200
    models = response.json()
    assert len(models) > 0
    providers = {m["provider"] for m in models}
    assert "openai" in providers
    assert "anthropic" in providers
    assert "gemini" in providers

