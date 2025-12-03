import logging
from typing import Any, Dict
from fastmcp import Client
from fastmcp.client.client import CallToolResult
from backend.mcp_clients import (
    DATETIME_URL,
    #SEARCHXNG_URL,
    DDGS_URL,
    WEATHER_URL,
    GEOCODING_URL
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MCPManager:
    """
    Multi-Server MCP Manager.
    Provides unified async calls to all registered MCP servers.
    """

    def __init__(self):
        # Registry of MCP servers
        self.servers = {
            "datetime": DATETIME_URL,
            #"searchxng": SEARCHXNG_URL,
            "ddgs": DDGS_URL,
            "weather": WEATHER_URL,
            "geocoding": GEOCODING_URL,
        }

    async def call_tool(self, server: str, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on a given MCP server and return normalized output.

        Args:
            server (str): MCP server key ('datetime', 'searchxng', 'weather', 'geocoding')
            tool (str): Name of the tool to call
            args (Dict[str, Any]): Arguments to pass to the tool

        Returns:
            Dict[str, Any]: Normalized MCP response
        """
        logger.info("========== MCPManager.call_tool ==========")
        logger.info(f"Server requested: {server}")
        logger.info(f"Tool requested: {tool}")
        logger.info(f"Arguments: {args}")
        logger.info("==========================================")

        if server not in self.servers:
            error_msg = f"MCP server '{server}' is not registered."
            logger.error(error_msg)
            return {"error": error_msg, "results": []}

        mcp_url = self.servers[server]
        logger.info(f"[MCPManager] Using MCP URL: {mcp_url}")

        try:
            async with Client(mcp_url) as client:
                logger.info(f"[MCPManager] Calling MCP tool: {tool} on server: {server}")
                result: CallToolResult = await client.call_tool(tool, args)

                raw_structured = result.structured_content
                raw_content = result.content

                logger.info(f"[MCPManager] Raw structured_content: {raw_structured}")
                logger.info(f"[MCPManager] Raw content: {raw_content}")

                # Normalize output: prefer structured_content, fallback to content
                normalized = raw_structured or raw_content

                # Ensure we always return a dict
                if not isinstance(normalized, dict):
                    logger.info("[MCPManager] Normalizing non-dict output into dict wrapper")
                    normalized = {"result": normalized}

                logger.info(f"[MCPManager] Final normalized output: {normalized}")
                logger.info("==========================================\n")
                return normalized

        except Exception as e:
            logger.error(f"[MCPManager] Fatal error calling {server}.{tool}: {e}")
            return {"error": str(e), "results": []}
