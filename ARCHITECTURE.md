# 🏗️ **ARCHITECTURE.md**

# **System Architecture Overview**

This project implements a **full MCP-enabled LLM application stack** using:

* **FastAPI backend** with LLM orchestration
* **Gradio frontend**
* **Multiple MCP servers** (Datetime, DDGS Search, Geocoding, Weather)
* **Ollama ( Qwen3:4b)** as the reasoning engine
* **Docker Compose** for orchestration

The architecture is modular, tool-driven, and cleanly layered.

---

# 🔷 High-Level Diagram

```
             ┌──────────────────────────┐
             │        Gradio UI         │
             └──────────────┬───────────┘
                            │  HTTP /chat
                            ▼
             ┌──────────────────────────┐
             │ FastAPI Backend          │
             │ - MCP Client Manager     │
             │ - LLM Orchestrator       │
             └──────────────┬───────────┘
                            │  MCP Calls
      ┌─────────────────────┼─────────────────────────────┐
      ▼                     ▼                             ▼
┌───────────────┐   ┌────────────────┐         ┌─────────────────┐
│ DDGS-MCP       │   │ Weather-MCP    │         │ Datetime-MCP     │
│ (DuckDuckGo)   │   │ (Open-Meteo)   │         │ (UTC datetime)   │
└───────────────┘   └───────┬────────┘         └─────────────────┘
                              │ (depends on)
                              ▼
                   ┌────────────────────┐
                   │ Geocoding-MCP      │
                   │ (Nominatim)        │
                   └────────────────────┘

                      ▼
            ┌────────────────────┐
            │     Ollama LLM     │
            │  (Granite/Qwen3)   │
            └────────────────────┘
```

---

# 🔷 System Components

## 1. **Gradio Frontend**

* Runs at **port 7860**
* Communicates only with backend (`/chat`)
* Maintains chat history and logs
* Displays final LLM responses

---

## 2. **FastAPI Backend**

The backend makes all decisions and orchestrates the full system.

### Internal responsibilities:

* **/chat endpoint** (main entrypoint)
* **LLM Orchestrator**

  * Calls Ollama for planning and final answer generation
* **MCP Manager**

  * Discovers tools
  * Calls the correct MCP server automatically
  * Returns JSON results back to the orchestrator

### Files:

```
backend/src/backend/
└── llm/
    ├── orchestrator.py
    ├── prompt_templates.py
    ├── ollama_service.py
└── mcp/manager.py
└── routers/chat.py
```

### Data flow:

1. User sends message → FastAPI
2. LLM decides if a tool is required
3. Orchestrator calls MCP tool
4. MCP server performs external API logic
5. Backend gives results to LLM
6. LLM creates final message
7. Backend returns response to UI

---

## 3. **MCP Servers (Tools)**

### 🟦 **DDGS-MCP (DuckDuckGo search)**

* Tool: `ddgs_search(query)`
* Fast, no API key required
* Used for general web lookups

### 🟩 **Weather-MCP**

* Tool: `get_weather(location)`
* Uses **Geocoding-MCP** first
* Uses **Open-Meteo** for realtime weather

### 🟨 **Geocoding-MCP**

* Tool: `geocode(location)`
* Uses **Nominatim OpenStreetMap**
* Returns lat/lon for weather

### 🟧 **Datetime-MCP**

* Tool: `get_current_datetime()`
* Returns current UTC timestamp

### Server File Pattern:

```
mcp-servers/<name>/<name>_mcp/
   ├── server.py  (@mcp.tool)
   └── tool.py    (business logic)
```

---

## 4. **Ollama LLM**

* Local inference server on port **11434**
* Models: **Granite**, **Qwen3:4b**, or any supported model
* Handles:

  * Planning ("should I call a tool?")
  * Final natural output after tool results

---

# 🔷 Detailed Data Flow

Below is the exact sequence for a full tool-enabled chat request.

| Step                      | Source → Destination                | Description                                    |
| ------------------------- | ----------------------------------- | ---------------------------------------------- |
| **1. User Input**         | User → Gradio                       | User types a message.                          |
| **2. API Call**           | Gradio → FastAPI `/chat`            | Sends JSON with message + history.             |
| **3. LLM Planning**       | FastAPI → Orchestrator → Ollama     | LLM decides whether a tool is necessary.       |
| **4. Tool Decision**      | LLM → MCP Manager                   | Orchestrator reads tool instructions from LLM. |
| **5. MCP Execution**      | MCP Manager → MCP Server            | Backend calls the correct MCP server.          |
| **6. External API Calls** | MCP Server → External API           | DDGS, Nominatim, Open-Meteo, etc.              |
| **7. Tool Response**      | MCP Server → MCP Manager            | MCP returns structured JSON.                   |
| **8. LLM Finalization**   | MCP Manager → Orchestrator → Ollama | LLM integrates tool results into final answer. |
| **9. Backend Response**   | FastAPI → Gradio                    | JSON response returned to UI.                  |
| **10. UI Display**        | Gradio                              | Chat window shows assistant message.           |

---

# 🔷 Port Mapping

| Service               | Port      | Notes                      |
| --------------------- | --------- | -------------------------- |
| **FastAPI Backend**   | **8000**  | Main API                   |
| **Gradio Frontend**   | **7860**  | UI                         |
| **Datetime-MCP**      | **50051** | MCP                        |
| **DDGS-MCP**          | **50052** | MCP                        |
| **Weather-MCP**       | **50053** | MCP                        |
| **Geocoding-MCP**     | **50054** | MCP                        |
| **SearchXNG Service** | **8181**  | SearxNG backend (optional) |
| **Ollama**            | **11434** | LLM inference              |

---

# 🔷 Component Responsibility Matrix

| Component            | Category          | Responsibilities                              |
| -------------------- | ----------------- | --------------------------------------------- |
| **Gradio UI**        | Frontend          | Render chat UI, send requests, show responses |
| **FastAPI Backend**  | Application Layer | Routes requests, orchestrates LLM + tools     |
| **Chat Router**      | API               | `/chat` endpoint                              |
| **LLM Orchestrator** | AI Logic          | Tool planning, final answer generation        |
| **Prompt Templates** | AI Logic          | System + tool instructions                    |
| **MCP Manager**      | Coordination      | Calls MCP servers, returns JSON               |
| **Datetime-MCP**     | Tool              | Current UTC datetime                          |
| **DDGS-MCP**         | Tool              | DuckDuckGo Web Search                         |
| **Geocoding-MCP**    | Tool              | Convert text → coordinates                    |
| **Weather-MCP**      | Tool              | Current weather                               |
| **Nominatim**        | External          | Geocoding backend                             |
| **Open-Meteo**       | External          | Weather backend                               |
| **Ollama**           | LLM               | Model reasoning + output                      |

---

# 🔷 Summary

This architecture provides:

### ✅ Modular MCP-based tools

### ✅ Local LLM with tool reasoning

### ✅ Chained tools: DDGS → Geocoding → Weather

### ✅ Clean separation between Frontend, Backend, Tools

### ✅ Dockerized and production-ready

It is designed to scale as more MCP servers or LLM backends are added.

---
