# **Backend Service (`backend/src/backend`)**

This directory contains the full **FastAPI backend**, including:

* The `/chat` API entrypoint
* The **LLM Orchestrator** (Ollama reasoning + tool planning)
* The **MCP Client Manager** (tool execution through MCP servers)
* Routers, services, models, and tests

The backend acts as the central controller that connects the **UI → LLM → MCP tools**.

---

# 📦 **Directory Structure**

```
backend/src/backend/
├── app.py                  # FastAPI app entrypoint
├── llm/                    # LLM logic + tool orchestration
│   ├── orchestrator.py     # Core tool/LLM pipeline
│   ├── prompt_templates.py # System + tool prompting logic
│   ├── ollama_service.py   # Ollama HTTP client
│   ├── schemas.py          # Internal LLM models
│   └── __init__.py
├── mcp/                    # MCP client integration layer
│   └── manager.py          # Multi-MCP server manager
├── models/                 # Pydantic request/response models
│   ├── chat.py
│   └── __init__.py
├── routers/                # FastAPI endpoints
│   ├── chat.py             # /chat endpoint (main entrypoint)
│   ├── datetime.py         # (Optional) direct testing routes
│   ├── geocoding.py
│   ├── search.py
│   ├── weather.py
│   ├── health.py
│   └── README.md
├── services/               # Backend utility services
│   ├── chat_service.py     # Bridges API requests → orchestrator
│   ├── ollama_service.py   # (Deprecated - see llm/ollama_service.py)
│   └── __init__.py
└── tests/                  # pytest test suite
```

---

# 🚀 **What the Backend Does**

The backend performs **three major roles**:

---

## **1. API Layer (FastAPI)**

Main endpoints:

| Endpoint                                         | Purpose                               |
| ------------------------------------------------ | ------------------------------------- |
| `POST /chat`                                     | Primary chat interface used by Gradio |
| `GET /health`                                    | Container health check                |
| (Optional) `/weather`, `/geocoding`, `/datetime` | Direct testing/micro-endpoints        |

These map external client requests into an internal **Chat Service** which then calls the LLM orchestrator.

---

## **2. LLM Layer (Ollama Orchestrator)**

Located in `llm/orchestrator.py`.

This component:

1. Sends user messages to Ollama
2. Lets the model decide **whether a tool call is needed**
3. If yes → calls MCP Manager
4. Provides MCP tool results back to the LLM
5. LLM generates the final response

Tool-thinking prompts and formatting are defined in:

```
llm/prompt_templates.py
```

The LLM is accessed through:

```
llm/ollama_service.py
```

---

## **3. MCP Manager Layer**

Located in:

```
mcp/manager.py
```

The manager:

* Connects to each MCP server (Datetime, DDGS, Geocoding, Weather)
* Caches available tools + schemas
* Executes tool calls requested by the LLM
* Normalizes and returns structured JSON results

This abstraction hides the complexity of:

* HTTP vs WebSocket MCP transports
* Tool schemas and argument validation
* Multi-server tool discovery

---

# 🔧 **How /chat Works Internally**

### 1️⃣ **User → Frontend → Backend**

Frontend sends:

```json
{
  "message": "What's the weather in Tokyo?",
  "history": [...]
}
```

---

### 2️⃣ **Backend → LLM (Planning)**

Ollama receives instructions + context via orchestrator:

```
System: You may call tools when needed.
User: What's the weather in Tokyo?
```

LLM responds with either:

* A reasoning + tool call request
* OR a natural-language answer

---

### 3️⃣ **If a Tool Call is Needed**

Example reasoning:

```
<tool>
{
   "name": "get_weather",
   "arguments": { "location": "Tokyo" }
}
</tool>
```

Backend passes this to:

```
mcp/manager.py
```

---

### 4️⃣ **MCP Manager → Weather-MCP Server**

Weather-MCP internally calls **Geocoding-MCP → Open-Meteo API**.

Returns structured JSON:

```json
{
  "temp_c": 17.3,
  "description": "Clear sky"
}
```

---

### 5️⃣ **Backend → LLM (Final Answer)**

LLM receives tool results and generates natural language:

> "The current weather in Tokyo is 17°C with clear skies."

---

### 6️⃣ **Backend → Frontend**

JSON returned to UI.

---

# 🐋 **Running the Backend (Standalone)**

### Using Docker Compose (recommended)

```bash
docker compose up backend
```

### Running locally

```bash
cd backend
uv sync
uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

---

# 📘 Development Notes

### ✔ Backend expects:

* **Docker + Ollama running**
* At least one model pulled (e.g. `qwen2.5`, `qwen3:4b`)

### ✔ MCP servers must be reachable:

```
datetime-mcp   → 50051
ddgs-mcp       → 50052
weather-mcp    → 50053
geocoding-mcp  → 50054
```

### ✔ Frontend requires only:

* Backend reachable at: `http://backend:8000/chat`

---

# 🧪 Tests

Tests live in:

```
backend/src/backend/tests/
```

They verify:

* `/chat` endpoint behavior
* MCP integration (mocked)
* Orchestrator planning logic
* Health checks

---

# 📄 License

This backend is part of the main project repository and follows the project-wide license.

