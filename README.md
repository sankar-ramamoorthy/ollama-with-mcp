
**Core Flow:** `curl /chat` → `orchestrator.py` → **LLM decides tool** → `FastMCP Client` → **MCP Server** → **LLM formats answer**
```

### ** `README.md` **

```markdown
# 🧠 Ollama + MCP Agent System  
**A fully local, framework-free, ReAct-style AI agent powered by modular MCP microservices.**

This project demonstrates how to build **real agentic AI systems** using only:

- **Local LLMs (Ollama + Qwen3:4B)**  
- **FastMCP microservices (datetime, weather, geocoding, search)**  
- **FastAPI**  
- **Docker Compose**

No LangChain.  
No cloud LLMs.  
No closed-source toolchains.

Just **a clean, transparent,  agent architecture** that anyone can run locally.

Modular AI Agent platform using **Ollama (Qwen3:4B)** + **FastMCP tools** + **FastAPI** + **Docker Compose**.

**LLM intelligently delegates to specialized MCP microservices** (datetime, weather, search, geocoding).


# 📌 Prerequisites

Before running the system, you must have:

### ✔ **Docker** installed and running  
https://www.docker.com/get-started/

### ✔ **Ollama** installed and running  
https://ollama.com/download

### ✔ **Qwen3:4B model already pulled in Ollama**
```bash
ollama pull qwen3:4b

🧩 What Kind of Agent Is This?

This system implements a ReAct-style, tool-using LLM agent, also known as a Toolformer-style single-step agent.

Agent Loop:
Thought → Tool Call → Observation → Final Answer

LLM decides if a tool is needed
Orchestrator routes the call to the correct MCP server
Tool returns structured JSON
LLM synthesizes the final natural-language answer

🔧 Core Architecture

Flow:
User → FastAPI /chat → LLM → MCP Tool → LLM synthesis → Response
User
  ↓
FastAPI /chat
  ↓
LLM (Ollama + Qwen3)
  ↓ decides tool
Orchestrator → FastMCP Client → MCP Tool Server
  ↓ tool result
LLM formats final answer
  ↓
Response

Each tool is its own isolated MCP microservice running in Docker.
🎯 Features
🤖 Autonomous tool-using agent (LLM chooses which MCP tool to call)
🧩 Microservice architecture using MCP
🕸️ Search tool via DuckDuckGo MCP 
🌦️ Weather tool using Open-Meteo
🌍 Geocoding tool using Nominatim
🗓️ Datetime tool returning the current UTC date/time
🎨 Gradio UI interface
🐳 Fully Dockerized

🔒 100% local; no cloud LLMs
## 🎯 Features

- ✅ **Chat Orchestrator**: LLM decides tool → executes → formats natural response
- ✅ **Datetime MCP**: "What's today's date?" → `datetime-mcp:50051`
- ✅ **Weather MCP**: "Weather in Dallas?" → `weather-mcp:50053` → Open-Meteo
- ✅ **Search MCP**: DDGS  integration (port 50052)
- ✅ **Geocoding MCP**: Weather geocoding support (port 50054)
- 🎨 **Gradio UI**: `http://localhost:7860`
- 🚀 **Production-ready**: Dockerized, uv dependency management


| Service              | Port  | Status | Description                                    |
| -------------------- | ----- | ------ | ---------------------------------------------- |
| Backend Orchestrator | 8000  | ✅      | FastAPI + LLM tool decision + MCP execution    |
| Datetime MCP         | 50051 | ✅      | "What's today's date?"→ UTC ISO datetime       |
| Weather MCP          | 50053 | ✅      | "Weather in Dallas?"→ Open-Meteo via geocoding |
| Geocoding MCP        | 50054 | ✅      | Address → lat/lon (Nominatim, used by weather) |
| Search MCP           | 50052 | ⚠️     |  DDGS Duck Duck Go Search            |
| Gradio UI            | 7860  | ✅      | Web interface                                  |

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

**Response:** `"Today's date is November 30, 2025."`

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

**See [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) for details.**


## 🐳 Docker Compose Services

| Service | Port | Purpose |
|---------|------|---------|
| `backend` | 8000 | FastAPI orchestrator |
| `datetime-mcp` | 50051 | Date/time tool ✅ |
| `weather-mcp` | 50053 | Weather tool ✅ |
| `ddgs` | 50052 | Web search  |
| `frontend` | 7860 | Gradio UI |


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

## 🙏 Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP servers
- [Ollama](https://ollama.com) - Local LLM (Qwen3:4B )
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) - Web search
- [Open-Meteo](https://open-meteo.com) - Weather API
- [Nominatim](https://nominatim.org/) — OpenStreetMap geocoding service
```

