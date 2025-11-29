import asyncio
from fastmcp import Client

async def test_weather():
    mcp_url = "http://localhost:50053/mcp"
    async with Client(mcp_url) as client:
        result = await client.call_tool("get_weather_tool", {"location": "New York"})
        print("Weather MCP result:", result)

if __name__ == "__main__":
    asyncio.run(test_weather())
