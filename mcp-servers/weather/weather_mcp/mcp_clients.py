# weather_mcp/mcp_clients.py
from typing import Any, Dict
from fastmcp import Client
from fastmcp.client.client import CallToolResult

# MCP server host and port (Docker Compose service name)
SEARCHXNG_MCP_HOST = "searchxng-mcp"
SEARCHXNG_MCP_PORT = 50052

# Build full MCP URL
MCP_URL = f"http://{SEARCHXNG_MCP_HOST}:{SEARCHXNG_MCP_PORT}/mcp"

async def call_searchxng(query: str) -> Dict[str, Any]:
    """
    Call the SearchXNG MCP server's 'search_web' tool.

    Args:
        query (str): The search query string.

    Returns:
        dict: Either a dict containing the search results or an 'error' key.
    """
    if not query or not isinstance(query, str):
        return {"error": "Query must be a non-empty string", "results": []}

    try:
        async with Client(MCP_URL) as client:
            mcp_response: CallToolResult = await client.call_tool("search_web", {"query": query})
            # Return structured content or raw content
            return mcp_response.structured_content or mcp_response.content
    except Exception as e:
        return {"error": str(e), "results": []}
