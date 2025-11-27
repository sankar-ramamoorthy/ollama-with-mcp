import logging
from fastmcp import MCPServer
from tool import current_date

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Start MCPServer and register tools
    server = MCPServer()
    server.register_tool(current_date)

    logger.info("[server] Starting MCP server on ws://0.0.0.0:9000")
    server.serve("0.0.0.0", 9000)

if __name__ == "__main__":
    main()
