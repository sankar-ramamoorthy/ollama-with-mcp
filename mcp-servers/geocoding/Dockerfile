FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

#  Copy only pyproject files for caching
COPY pyproject.toml  uv.lock README.md ./

#  Install dependencies via UV
RUN uv sync --frozen

#  Copy MCP server code
#COPY . .
# Copy the package code
COPY geocoding_mcp ./geocoding_mcp

#  Expose MCP port
EXPOSE 50054

# Run the MCP server as a module
CMD ["uv", "run", "python", "-m", "geocoding_mcp.server"]
