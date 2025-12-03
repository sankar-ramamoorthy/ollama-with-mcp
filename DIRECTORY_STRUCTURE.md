# **DIRECTORY_STRUCTURE.md (Updated)**

📦 *Updated to reflect the 2025-12-03 repository structure*

---

# 📁 **Project Directory Structure**

```
ollama-with-mcp/                          # 🏠 Root Project
├── .env
├── .gitignore
├── .python-version
├── docker-compose.yml                    # All services orchestrated
├── LICENSE
├── Project Plan.md
├── Proposed Phases or Milestones.md
├── STATUS.md                             # Project progress
├── README.md                             # Main project documentation
└── DIRECTORY_STRUCTURE.md                # This file
```

---

# 🚀 **Backend Service (FastAPI + LLM Orchestrator)**

**Path:** `backend/`
**Port:** `8000`

```
backend/
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── .venv/                                 # Local virtual environment (ignored)
└── src/backend/
    ├── app.py                             # FastAPI entrypoint
    ├── __init__.py
    │
    ├── routers/                           # 📡 API Endpoints
    │   ├── chat.py                        # POST /chat
    │   ├── datetime.py                    # POST /datetime/get
    │   ├── geocoding.py                   # POST /geocoding/get
    │   ├── weather.py                     # POST /weather/get
    │   ├── search.py                      # POST /search/get (DDGS)
    │   ├── health.py                      # GET /health
    │   └── README.md
    │
    ├── llm/                               # 🤖 LLM Orchestration
    │   ├── orchestrator.py                # LLM → Tool → LLM logic
    │   ├── prompt_templates.py
    │   ├── schemas.py
    │   ├── README.md
    │   └── __init__.py
    │
    ├── services/                          # Application Services
    │   ├── ollama_service.py              # HTTP client for Ollama
    │   └── chat_service.py
    │
    ├── mcp/                               # MCP Manager
    │   └── manager.py                     # Multi-tool orchestration
    │
    ├── models/                            # Pydantic models
    │   ├── chat.py                        # ChatRequest / ChatResponse
    │   └── ...
    │
    ├── mcp_clients.py                     # HTTP clients for MCP servers
    │
    └── tests/                             # (Needs work)
```

---

# 🎨 **Frontend Service (Gradio UI)**

**Path:** `frontend/`
**Port:** `7860`

```
frontend/
├── Dockerfile
└── src/
    └── gradio_api/
        ├── app.py                         # Gradio Chat UI
        └── ...
```

---

# 🔧 **MCP Tool Servers**

All MCP servers follow this pattern:

```
mcp-servers/<tool-name>/
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── <tool-name>_mcp/
    ├── server.py                          # FastMCP server
    └── tool.py                            # Actual API logic
```

---

## ⏰ **1. Datetime MCP Server**

**Path:** `mcp-servers/datetime/`
**Port:** `50051`

```
mcp-servers/datetime/
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── datetime_mcp/
    ├── server.py                          # get_current_datetime_tool
    └── tool.py                            # datetime.now()
```

---

## 🔍 **2. DDGS Web Search MCP**

**Path:** `mcp-servers/ddgs/`
**Port:** (defined in compose)

```
mcp-servers/ddgs/
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── ddgs_mcp/
    ├── server.py                          # @mcp.tool: ddgs_search
    ├── tool.py                            # DuckDuckGo search implementation
    └── ...
```

> ❗ Replaces old SearchXNG MCP in earlier project plan.
> (The actual SearXNG backend still exists under `searchxng_svc/` but is not used here.)

---

## 📍 **3. Geocoding MCP**

**Path:** `mcp-servers/geocoding/`
**Port:** `50054`

```
mcp-servers/geocoding/
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── tests/
└── geocoding_mcp/
    ├── server.py                          # geocode_tool
    ├── tool.py                            # Nominatim API client
    ├── mcp_client.py                      # For internal chaining (weather)
    └── __init__.py
```

---

## 🌤️ **4. Weather MCP**

**Path:** `mcp-servers/weather/`
**Port:** `50053`

```
mcp-servers/weather/
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── tests/
└── weather_mcp/
    ├── server.py                          # get_weather_tool
    ├── tool.py                            # Calls geocoding → then weather API
```

---

## 📰 **5. SearchXNG Backend (Not MCP)**

**Path:** `searchxng_svc/`
**Purpose:** Optional local SearXNG engine
**Port:** `8181`

```
searchxng_svc/
├── Dockerfile
├── settings.yml
└── limiter.toml
```

> Note: MCP Search is now implemented via **DDGS**, not SearXNG.

---

# 📌 **Simplified High-Level Overview**

```
Frontend (Gradio)
        ↓ HTTP
Backend (FastAPI / LLM Orchestrator)
        ↓ calls
Ollama (LLM)
        ↓ tool decisions
MCP Manager → MCP Servers
     ↳ datetime
     ↳ geocoding
     ↳ weather
     ↳ DDGS search
```

---

# ⚠️ Files to Ignore (Dev Only)

```
*/.venv/
__pycache__/
.pytest_cache/
*.egg-info/
```

---

