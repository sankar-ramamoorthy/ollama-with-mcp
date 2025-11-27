# Use the Astral UV Python slim image
FROM astral/uv:python3.12-bookworm-slim

# Set working directory inside the container
WORKDIR /app

# Copy backend source code
COPY ./backend/src/backend /app

# Upgrade pip and install dependencies in one layer with logging
RUN set -eux; \
    echo "Upgrading pip..."; \
    uv run python -m pip install --no-cache-dir --upgrade pip; \
    echo "Installing FastMCP and httpx..."; \
    uv run pip install --no-cache-dir fastmcp httpx; \
    echo "Dependencies installed successfully."

# Expose default MCP port
EXPOSE 50051

# Set the entrypoint to run your MCP server
# Replace 'server.py' with the actual entrypoint of your MCP server
CMD ["uv", "run", "python", "server.py"]
