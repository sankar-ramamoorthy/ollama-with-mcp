# **Ollama + MCP Agent System**


Modular AI Agent platform using **Ollama (Qwen3:4B)** + **FastMCP tools** + **FastAPI** + **Docker Compose**.

**A fully local, framework-free ReAct-style AI agent using Ollama, FastAPI, and MCP microservices (weather, search, geocoding, datetime).**

---

## 🎯 Features

* ✅ **Chat Orchestrator**: LLM decides tool → executes → formats natural response
* 🗓️ **Datetime MCP**: Returns the **current UTC date & time** (ISO 8601)
* 🌤️ **Weather MCP**: "Weather in Dallas?" → `weather-mcp:50053` (Open-Meteo)
* 🔎 **Search MCP**:  DDGS (port 50052)
* 🗺️ **Geocoding MCP**: Uses Nominatim to resolve locations (port 50054)
* 🎨 **Gradio UI**: `http://localhost:7860`
* 🐳 **Dockerized system**: Each tool runs as an MCP microservice
* 🔒 **Fully local**: Requires **Ollama + Qwen3:4B** pre-installed

---

## 📦 Requirements

* **Docker & Docker Compose** (installed and running)
* **Ollama installed and running**
* **Qwen3:4B pulled locally:**

```
ollama pull qwen2.5:4b
```

---

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

| Endpoint             | Purpose           | Example                             |
| -------------------- | ----------------- | ----------------------------------- |
| `POST /chat`         | Main orchestrator | `{"message": "Weather in Dallas?"}` |
| `POST /datetime/get` | Direct datetime   | Returns UTC ISO datetime            |
| `POST /weather`      | Direct weather    | `{"location": "Dallas"}`            |
| `GET /health`        | System status     | Health check                        |
| `POST /search/get`   | Web Search        | `{"message": "News in Dallas?"}`    |


---

## 🏗️ Architecture

```
User → FastAPI (/chat) → LLM Decision → MCP Tool → LLM Synthesis → Response
                    ↓
              orchestrator.py orchestrates it all
```

---

## 🐳 Docker Compose Services

| Service       | Port  | Purpose                 |
| ------------- | ----- | ----------------------- |
| backend       | 8000  | FastAPI orchestrator    |
| datetime-mcp  | 50051 | Date/time MCP           |
| weather-mcp   | 50053 | Weather MCP             |
| ddgs-mcp      | 50052 | Web search MCP          |
| geocoding-mcp | 50054 | Nominatim geocoding MCP |
| frontend      | 7860  | Gradio UI               |

---

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

* [FastMCP](https://github.com/jlowin/fastmcp) – MCP servers
* [Ollama](https://ollama.com) – Local LLM
* [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) – Search 
* [Nominatim](https://nominatim.org/) – OpenStreetMap geocoding
* [Open-Meteo](https://open-meteo.com) – Weather API

---
