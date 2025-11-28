FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy only pyproject files for caching
COPY pyproject.toml uv.lock README.md ./

# Copy package code
COPY searchxng_mcp ./searchxng_mcp

# Install dependencies
RUN uv sync --frozen

# Expose MCP port
EXPOSE 50052

# Run MCP server as a module
CMD ["uv", "run", "python", "-m", "searchxng_mcp.server"]
