# mcp-servers/searchxng/server.py
import logging
import asyncio
from fastmcp import FastMCP
from searchxng_mcp.tool import search_web  as search_web_internal 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("searchxng-mcp")

def main():
    mcp = FastMCP("searchxng-mcp")

    # Register the tool with the correct name "search_web" and as an async function
    @mcp.tool
    async def search_web(query: str):
        try:
            # Await the async function from tool.py
            results = await search_web_internal(query)
            logger.info(f"Tool returned {len(results)} results")
            return {"results": results} # Return a dict to match client expectations
        except Exception as e:
            logger.error(f"Error in search_web tool: {e}")
            return {"error": str(e), "results": []}

    logger.info("Starting SearchXNG MCP HTTP server on http://0.0.0.0:50052")
    mcp.run(transport="http", host="0.0.0.0", port=50052)

if __name__ == "__main__":
    main()

