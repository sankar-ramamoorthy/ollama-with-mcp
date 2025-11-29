from fastmcp import FastMCP
from geocoding_mcp.tool import geocode_location
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geocoding-mcp")

def main():
    mcp = FastMCP("geocoding-mcp")

    @mcp.tool
    async def geocode_tool(address: str):
        """Return geocoding data (latitude/longitude) for an address."""
        return await geocode_location(address)

    mcp.run(transport="http", host="0.0.0.0", port=50054)
    logger.info("Starting geocoding MCP WebSocket server on ws://0.0.0.0:50054")

if __name__ == "__main__":
    main()


