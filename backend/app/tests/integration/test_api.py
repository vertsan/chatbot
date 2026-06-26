import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
class TestHealthEndpoint:
    async def test_health_check(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


@pytest.mark.asyncio
class TestAuthEndpoints:
    async def test_register_validation(self, client):
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "invalid", "password": "short"},
        )
        assert response.status_code == 422  # Validation error

    async def test_login_validation(self, client):
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "invalid"},
        )
        assert response.status_code == 422
