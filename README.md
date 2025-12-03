# **Ollama + MCP Agent System**


Modular AI Agent platform using **Ollama (Qwen3:4B)** + **FastMCP tools** + **FastAPI** + **Docker Compose**.

**A fully local, framework-free ReAct-style AI agent using Ollama, FastAPI, and MCP microservices (weather, search, geocoding, datetime).**

---

## 🎯 Features

- ✅ **Chat Orchestrator**: LLM decides tool → executes → formats natural response
- ✅ **Datetime MCP**: "What's today's date?" → `datetime-mcp:50051`
- ✅ **Weather MCP**: "Weather in Dallas?" → `weather-mcp:50053` → Open-Meteo
- ✅ **Search MCP**: DDGS/SearxNG integration (port 50052)
- ✅ **Geocoding MCP**: Weather geocoding support (port 50054)
- 🎨 **Gradio UI**: `http://localhost:7860`
- 🚀 **Production-ready**: Dockerized, uv dependency management


| Service              | Port  | Status | Description                                    |
| -------------------- | ----- | ------ | ---------------------------------------------- |
| Backend Orchestrator | 8000  | ✅      | FastAPI + LLM tool decision + MCP execution    |
| Datetime MCP         | 50051 | ✅      | "What's today's date?"→ UTC ISO datetime       |
| Weather MCP          | 50053 | ✅      | "Weather in Dallas?"→ Open-Meteo via geocoding |
| Geocoding MCP        | 50054 | ✅      | Address → lat/lon (Nominatim, used by weather) |
| Search MCP           | 50052 | ⚠️     | SearxNG (planned: DDGS replacement)            |
| Gradio UI            | 7860  | ✅      | Web interface                                  |
| SearxNG              | 8181  | ✅      | Search backend                                 |

## 🚀 Quick Start

``` 
# Clone & start
git clone <repo>
cd ollama-with-mcp
docker compose up -d

# Backend API ready
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is today'\''s date?"}'
```

**Response:**
`"Today's date is November 30, 2025."`

---

## 🛠️ API Endpoints

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `POST /chat` | **Main orchestrator** | `{"message": "Weather in Dallas?"}` |
| `POST /datetime/get` | Direct datetime | Returns UTC ISO datetime |
| `POST /weather` | Direct weather | `{"location": "Dallas"}` |
| `GET /health` | System status | Health check all services |

## 🏗️ Architecture

```
User → FastAPI (/chat) → LLM Decision → MCP Tool → LLM Synthesis → Response
                    ↓
              orchestrator.py orchestrates it all
```

---

## 🐳 Docker Compose Services

| Service | Port | Purpose |
|---------|------|---------|
| `backend` | 8000 | FastAPI orchestrator |
| `datetime-mcp` | 50051 | Date/time tool ✅ |
| `weather-mcp` | 50053 | Weather tool ✅ |
| `searchxng` | 50052 | Web search  |
| `frontend` | 7860 | Gradio UI |
| `searchxng_svc` | 8181 | SearxNG backend |

## 📚 Development

``` 
# Backend (uv)
cd backend
uv sync
uv run pytest

# MCP Servers (uv)  
cd mcp-servers/datetime
uv sync
uv run python datetime_mcp/server.py
```

---

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP servers
- [Ollama](https://ollama.com) - Local LLM (Qwen3:4B, Granite)
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) - Web search
- [Open-Meteo](https://open-meteo.com) - Weather API
```

