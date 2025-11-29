from fastmcp import FastMCP
from weather_mcp.tool import get_weather
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-mcp")

def main():
    mcp = FastMCP("weather-mcp")

    @mcp.tool
    async def get_weather_tool(location: str):
        """Return weather data for a location."""
        return await get_weather(location)

    mcp.run(transport="http", host="0.0.0.0", port=50053)
    logger.info("Starting weather MCP WebSocket server on ws://0.0.0.0:50053")

if __name__ == "__main__":
    main()
