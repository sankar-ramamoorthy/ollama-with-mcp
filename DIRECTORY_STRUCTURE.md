# DIRECTORY_STRUCTURE.md

## 📁 Complete Project Structure

```
ollama-with-mcp/                                    # 🏠 Root Project
├── .env                                            # Environment variables
├── .gitignore                                      # Git exclusions
├── .python-version                                 # pyenv version
├── docker-compose.yml                              # 7 Docker services orchestration
├── LICENSE                                         # MIT License
├── Project Plan.md                                 # Original roadmap
├── Proposed Phases or Milestones.md                # Development phases
├── Status.md                                       # Progress tracking
├── README.md                                       # Main project docs
└── hello.py                                        # Test script

├── backend/                                        # 🚀 FastAPI Backend (port 8000)
│   ├── Dockerfile                                  # Docker build
│   ├── pyproject.toml                              # uv dependencies
│   ├── uv.lock                                     # uv lockfile
│   ├── .venv/                                      # Local virtualenv (gitignored)
│   └── src/backend/                                # Python package
│       ├── app.py                                  # FastAPI app entrypoint
│       ├── __init__.py
│       ├── mcp_clients.py                          # Direct MCP client wrappers
│       ├── llm/                                    # 🤖 LLM Orchestration
│       │   ├── orchestrator.py                     # LLM → Tool → LLM core logic ✨
│       │   ├── prompt_templates.py                 # Tool decision prompts
│       │   ├── ollama_service.py                   # Ollama client
│       │   ├── schemas.py                          # Pydantic models
│       │   ├── ARCHITECTURE.md
│       │   ├── README.md
│       │   └── __init__.py
│       ├── routers/                                # 📡 API Endpoints
│       │   ├── chat.py                             # POST /chat ← MAIN ENTRYPOINT
│       │   ├── datetime.py                         # POST /datetime/get
│       │   ├── weather.py                          # POST /weather
│       │   ├── geocoding.py                        # POST /geocoding
│       │   ├── search.py                           # POST /search
│       │   ├── health.py                           # GET /health
│       │   └── README.md
│       ├── services/                               # 🛠️ Business Services
│       │   ├── ollama_service.py                   # Ollama HTTP client
│       │   └── chat_service.py
│       ├── mcp/                                    # MCP Client Manager
│       │   └── manager.py                          # Multi-MCP coordination
│       ├── models/                                 # Pydantic models
│       └── tests/                                  # Unit tests

├── frontend/                                       # 🎨 Gradio UI (port 7860)
│   ├── Dockerfile
│   └── src/gradio_api/                             # Gradio app

├── mcp-servers/                                    # 🛠️ FastMCP Tool Servers
│   ├── datetime/                                   # ⏰ Port 50051 ✅
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── uv.lock
│   │   └── datetime_mcp/
│   │       ├── server.py                           # @mcp.tool("get_current_datetime")
│   │       └── tool.py                             # datetime.now()
│   ├── searchxng/                                  # 🔍 Port 50052 ✅ SearxNG
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── uv.lock
│   │   ├── .venv/
│   │   └── searchxng_mcp/
│   │       ├── server.py                           # @mcp.tool("search_web")
│   │       ├── tool.py                             # SearxNG client
│   │       └── tests/
│   ├── weather/                                    # 🌤️ Port 50053 ✅
│   │   ├── Dockerfile
│   │   ├── pyproject.toml
│   │   ├── uv.lock
│   │   ├── .venv/
│   │   ├── tests/
│   │   └── weather_mcp/
│   │       ├── server.py                           # @mcp.tool("get_weather_tool")
│   │       └── tool.py                             # Open-Meteo + Geocoding
│   └── geocoding/                                  # 📍 Port 50054 ✅ (Weather dep)
│       ├── Dockerfile
│       │   ├── pyproject.toml
│       │   ├── uv.lock
│       │   ├── README.md
│       │   └── tests/
│       └── geocoding_mcp/
│           ├── server.py                           # @mcp.tool("geocode_tool")
│           ├── tool.py                             # Nominatim API
│           ├── mcp_clients.py                      # Internal MCP calls
│           └── __init__.py

└── searchxng_svc/                                  # 📰 SearxNG Backend (port 8181)
    ├── Dockerfile
    ├── settings.yml
    └── limiter.toml
```

## 🔍 File Purpose Guide

### **Core Flow Files** ⭐
```
backend/src/backend/llm/orchestrator.py          # LLM decides tool → calls MCP → LLM formats
backend/src/backend/routers/chat.py              # POST /chat → orchestrator
mcp-servers/*/mcp_*/server.py                    # @mcp.tool() definitions
mcp-servers/*/mcp_*/tool.py                      # External API logic
```

### **MCP Server Pattern** (each mcp-servers/*/)
```
mcp-servers/datetime/
├── Dockerfile                    # Docker build
├── pyproject.toml                # uv deps (fastmcp, pydantic)
├── uv.lock                       # Dependency lock
└── datetime_mcp/                 # Python package
    ├── server.py                 # FastMCP + @mcp.tool()
    └── tool.py                   # Business logic
```

### **Backend Pattern**
```
backend/src/backend/
├── app.py                        # FastAPI(app = FastAPI())
├── routers/                      # APIRouter(prefix="/chat")
├── llm/                          # Orchestrator + Ollama client
├── services/                     # Reusable services
└── mcp_clients.py                # Direct MCP calls for routers
```

## 🏗️ Docker Compose Services

| Service | Port | Build From | Purpose |
|---------|------|------------|---------|
| `backend` | 8000 | `./backend` | FastAPI + LLM orchestrator |
| `datetime-mcp` | 50051 | `./mcp-servers/datetime` | Date/time tool |
| `searchxng-mcp` | 50052 | `./mcp-servers/searchxng` | SearxNG web search |
| `weather-mcp` | 50053 | `./mcp-servers/weather` | Open-Meteo weather |
| `geocoding-mcp` | 50054 | `./mcp-servers/geocoding` | Nominatim geocoding |
| `frontend` | 7860 | `./frontend` | Gradio UI |
| `searchxng_svc` | 8181 | `./searchxng_svc` | SearxNG engine |

## ⚠️ Ignore These (Development Artifacts)
```
*.venv/                 # Local virtualenvs
*.egg-info/             # Python packaging
__pycache__/            # Python cache
.pytest_cache/          # pytest cache
```

## 🚀 Development Workflow

```bash
# Full stack
docker compose up --build

# Backend only
cd backend
uv sync
uv run uvicorn backend.app:app --reload

# Single MCP
cd mcp-servers/datetime
uv sync
uv run datetime_mcp/server.py
```

