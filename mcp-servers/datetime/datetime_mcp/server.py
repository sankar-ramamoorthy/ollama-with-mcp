from fastmcp import FastMCP
from datetime_mcp.tool import current_datetime

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("datetime-mcp")

def main():
    mcp = FastMCP("datetime-mcp")

    @mcp.tool
    def get_current_datetime():
        """Return current UTC datetime."""
        return current_datetime()

    # Simply run on a given port
    mcp.run(transport="http",host="0.0.0.0", port=50051)

    logger.info("Starting datetime MCP WebSocket server on ws://0.0.0.0:50051")

if __name__ == "__main__":
    main()
