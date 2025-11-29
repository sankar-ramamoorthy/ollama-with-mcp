---

## **README.md**

```markdown
# Ollama-with-MCP

A modular backend system integrating multiple MCP (Multi-Container-Protocol) servers with an LLM orchestration layer and a Gradio frontend. Supports multi-step queries with tool selection via LLM.

---

## **Project Overview**

- **Phase 5-6**: Added MCP servers for SearchXNG, Weather, Geocoding, and Datetime.
- **Phase 7**: Added LLM Orchestrator and MCPManager for multi-step query execution.
- **Phase 8**: Gradio frontend integration.

**Core Flow**:

```

User → /chat endpoint → LLM Orchestrator → MCPManager → MCP Tools → LLM → Response

```

---

## **Directory Structure**

```

backend/
├── src/backend/
│   ├── llm/
│   │   ├── **init**.py
│   │   ├── orchestrator.py
│   │   └── schemas.py
│   ├── mcp/
│   │   ├── **init**.py
│   │   └── manager.py
│   ├── routers/
│   │   ├── chat.py
│   │   ├── weather.py
│   │   ├── geocoding.py
│   │   ├── datetime.py
│   │   ├── search.py
│   │   └── health.py
│   ├── services/
│   │   ├── chat_service.py
│   │   └── ollama_service.py
│   ├── models/
│   │   └── chat.py
│   ├── mcp_clients.py
│   └── app.py
docker-compose.yml
frontend/ (Gradio)
mcp-servers/

````

---

## **Requirements**

- Python 3.11+
- Docker & Docker Compose
- Dependencies managed via `pyproject.toml` and `uv.lock`

---

## **Setup & Run**

1. **Build & start services**

```bash
docker-compose up --build
````

2. **Available services**

* Backend FastAPI: `http://localhost:8000`
* Gradio frontend: `http://localhost:7860`
* MCP servers ports:

  * Datetime: 50051
  * SearchXNG: 50052
  * Weather: 50053
  * Geocoding: 50054

3. **Test /chat endpoint**

```bash
POST http://localhost:8000/chat
Body: {"message": "What is the weather in New York tomorrow?"}
```

* Orchestrator will automatically decide which tools to call.
* Tools are called via `MCPManager` for normalized outputs.

---

## **Logging**

* Logs are printed for LLM decisions, tool calls, and errors.
* Use `logging` module in Python to configure logging level/output.

---

## **Future Work**

* Handle datetime formatting issues.
* Implement rate limiting on Geocoding MCP.
* Expand integration tests for full tool chaining.

````

