import pytest
from httpx import AsyncClient
from backend.app import app

@pytest.mark.asyncio
async def test_searchxng_valid_query():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/mcp/search", params={"query": "python"})
        assert response.status_code == 200
        data = response.json()
        # Should return a dict with 'query' and 'results'
        assert data["query"] == "python"
        assert isinstance(data["results"], list)
        assert len(data["results"]) > 0

@pytest.mark.asyncio
async def test_searchxng_empty_query():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/mcp/search", params={"query": ""})
        assert response.status_code == 200
        data = response.json()
        # Should gracefully return empty results or error message
        assert "results" in data
        assert isinstance(data["results"], list)
        assert len(data["results"]) == 0 or "error" in data

@pytest.mark.asyncio
async def test_searchxng_invalid_query():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/mcp/search", params={"query": None})
        assert response.status_code == 422  # FastAPI validation should reject None
