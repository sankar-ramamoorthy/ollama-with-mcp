# backend/mcp_clients.py
from typing import Any, Dict
from fastmcp import Client
from fastmcp.client.client import CallToolResult

# MCP server host and port (Docker Compose service name)
SEARCHXNG_MCP_HOST = "searchxng-mcp"
SEARCHXNG_MCP_PORT = 50052

# Build full MCP URL
MCP_URL       = f"http://{SEARCHXNG_MCP_HOST}:{SEARCHXNG_MCP_PORT}/mcp"
SEARCHXNG_URL = f"http://{SEARCHXNG_MCP_HOST}:{SEARCHXNG_MCP_PORT}/mcp"


WEATHER_MCP_HOST = "weather-mcp"
WEATHER_MCP_PORT = 50053
WEATHER_URL = f"http://{WEATHER_MCP_HOST}:{WEATHER_MCP_PORT}/mcp"

# MCP server host and port (Docker Compose service names)
GEOCODING_MCP_HOST = "geocoding-mcp"
GEOCODING_MCP_PORT = 50054
GEOCODING_URL = f"http://{GEOCODING_MCP_HOST}:{GEOCODING_MCP_PORT}/mcp"

DATETIME_MCP_HOST = "datetime-mcp"
DATETIME_MCP_PORT = 50051
DATETIME_URL = f"http://{DATETIME_MCP_HOST}:{DATETIME_MCP_PORT}/mcp"



# NOTE: The Client instance must be used within an async context manager.
# Do not create it at the module level for direct use.

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
        # Create a new Client instance and use it within an async context
        # to ensure proper connection lifecycle management.
        async with Client(MCP_URL) as client:
            mcp_response: CallToolResult = await client.call_tool("search_web", {"query": query})
            # Return the actual dictionary data, not the CallToolResult object
            return mcp_response#.structured_content or mcp_response.content

    except Exception as e:
        # Graceful error handling
        return {"error": str(e), "results": []}


async def call_weather(location: str) -> Dict[str, Any]:
    if not location or not isinstance(location, str):
        return {"error": "Location must be a non-empty string", "results": []}
    try:
        async with Client(WEATHER_URL) as client:
            response: CallToolResult = await client.call_tool("get_weather_tool", {"location": location})
            return response.structured_content
    except Exception as e:
        return {"error": str(e), "results": []}

async def call_geocoding(address: str) -> Dict[str, Any]:
    """
    Call the Geocoding MCP server to get latitude, longitude, and other details.
    
    Args:
        address (str): The address to geocode.
    
    Returns:
        dict: Geocoding result (latitude, longitude, etc.).
    """
    if not address or not isinstance(address, str):
        return {"error": "Address must be a non-empty string", "results": []}
    
    try:
        async with Client(GEOCODING_URL) as client:
            mcp_response: CallToolResult = await client.call_tool("geocode_tool", {"address": address})
            return mcp_response.structured_content or mcp_response.content
    except Exception as e:
        return {"error": str(e), "results": []}

async def call_datetime() -> Dict[str, Any]:
    """
    Call the Datetime MCP server to get current date in UTC.
    
    Args:
        None
    
    Returns:
        dict: current UTC date/time.
    """
    
    try:
        async with Client(DATETIME_URL) as client:
            mcp_response: CallToolResult = await client.call_tool("get_current_datetime", {})
            return mcp_response.structured_content or mcp_response.content
    except Exception as e:
        return {"error": str(e), "results": []}

