from typing import Any, Dict
from fastmcp import Client
from fastmcp.client.client import CallToolResult

# MCP server host and port for geocoding-mcp (using Docker Compose service name)
GEOCODING_MCP_HOST = "geocoding-mcp"
GEOCODING_MCP_PORT = 50054

# Build full MCP URL for geocoding
MCP_URL = f"http://{GEOCODING_MCP_HOST}:{GEOCODING_MCP_PORT}/mcp"

async def call_geocoding(location: str) -> Dict[str, Any]:
    """
    Call the Geocoding MCP server's 'geocode' tool.

    Args:
        location (str): The location to geocode.

    Returns:
        dict: Either a dict containing geocoding results or an 'error' key.
    """
    if not location or not isinstance(location, str):
        return {"error": "Location must be a non-empty string", "results": []}

    try:
        async with Client(MCP_URL) as client:
            mcp_response: CallToolResult = await client.call_tool("geocode", {"location": location})
            # Return structured content or raw content
            return mcp_response.structured_content or mcp_response.content
    except Exception as e:
        return {"error": str(e), "results": []}
