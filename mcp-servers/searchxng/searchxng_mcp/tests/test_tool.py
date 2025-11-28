import pytest
from searchxng_mcp.tool import search_web

@pytest.mark.asyncio
async def test_search_web_basic():
    query = "OpenAI"
    result = search_web(query)
    assert isinstance(result, dict) or isinstance(result, list)
    # Optional: check expected fields if API returns structured data
    if isinstance(result, dict):
        assert "results" in result

def test_search_web_empty_query():
    result = search_web("")
    assert result == [] or result == {"results": []}

def test_search_web_invalid_query():
    result = search_web(None)
    assert result == [] or result == {"results": []}
