
# 🛠️ MCP Servers Overview

This directory contains all **FastMCP servers** used by the backend. Each MCP server exposes one or more tools that can be called asynchronously from the FastAPI backend. These servers allow the LLM or backend to delegate specialized tasks like date/time, web search, geocoding, and weather lookups.

---

## 📌 MCP Servers & Ports

| MCP Server      | Port  | Purpose / Tool         | Notes                                                                             |
| --------------- | ----- | ---------------------- | --------------------------------------------------------------------------------- |
| `datetime-MCP`  | 50051 | `get_current_datetime` | Returns current UTC datetime.                                                     |
| `ddgs-MCP`      | 50052 | `search_web`           | Uses DuckDuckGo Search (DDGS) to fetch search results.                            |
| `weather-MCP`   | 50053 | `get_weather`          | Uses Open-Meteo API to return weather for a location; depends on `geocoding-MCP`. |
| `geocoding-MCP` | 50054 | `geocode`              | Uses Nominatim API to resolve location names into coordinates.                    |

---

## 🖥️ ASCII Architecture Diagram

```
           Frontend / UI (Gradio)
                     |
                     v
           +-------------------+
           | FastAPI Backend   |
           | Routers + LLM     |
           +-------------------+
                     |
       ┌─────────────┼─────────────┐
       |             |             |
       v             v             v
+--------------+ +-----------+ +--------------+
| datetime-MCP | | ddgs-MCP | | weather-MCP |
|  Port 50051  | | Port 50052| |  Port 50053 |
+--------------+ +-----------+ +--------------+
                     |
                     v
             +---------------+
             | geocoding-MCP |
             |  Port 50054   |
             +---------------+
                     |
                     v
               External APIs
      (DuckDuckGo Search, Open-Meteo, Nominatim)
```

---

## 📝 MCP Server Patterns

Each MCP server follows a similar layout:

```
mcp-servers/<tool-name>/
├── Dockerfile          # Builds the MCP server container
├── pyproject.toml      # Dependencies for the MCP tool (FastMCP, etc.)
├── uv.lock             # Lockfile from UV
└── <tool_name>_mcp/    # Python package containing MCP logic
    ├── server.py       # FastMCP entrypoint, defines @mcp.tool functions
    └── tool.py         # Core business logic, calls external APIs
```

### Example: `datetime-MCP`

```
mcp-servers/datetime/
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── datetime_mcp/
    ├── server.py       # @mcp.tool("get_current_datetime")
    └── tool.py         # datetime.now()
```

All MCP servers are **fully async** and designed to be called from the backend without blocking the main FastAPI process.

---

## 🚀 Development & Running MCP Servers

```bash
# Build & run all MCP servers (via docker-compose)
docker compose up --build

# Or run individual MCP server locally
cd mcp-servers/ddgs
uv sync
uv run ddgs_mcp/server.py
```

---

## ⚡ Notes

* `weather-MCP` depends on `geocoding-MCP` to resolve locations.
* `ddgs-MCP` replaces the old `searchxng-MCP` for web search functionality.
* MCP servers are **modular**, making it easy to add new tools in the future.
* Ports are fixed in docker-compose to allow backend orchestration.

