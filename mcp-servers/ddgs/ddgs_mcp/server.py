# ddgs_mcp/server.py
from fastmcp import FastMCP
from ddgs_mcp.tool import web_search

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ddgs-mcp")

def main():
    mcp = FastMCP("ddgs-mcp")
    
    @mcp.tool
    def web_search_tool(query: str, max_results: int = 5):
        """DuckDuckGo web search. Returns title, link, and snippet for top results."""
        return web_search(query, max_results)
    
    mcp.run(transport="http", host="0.0.0.0", port=50052)
    logger.info("DDGS MCP server running on http://0.0.0.0:50052/mcp")

if __name__ == "__main__":
    main()
