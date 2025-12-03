
````markdown
# Ollama with MCP Backend

A multi-component backend for orchestrating LLM queries with external MCP tools.  
This project allows user queries to be processed by an LLM and routed to specialized tool servers (weather, geocoding, search, datetime) when required.

---

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

---

## Architecture

This backend uses a **Orchestration engine** with the following flow:

1. **User Query → `/chat` Endpoint**  
   The query is received at FastAPI `/chat`.

2. **LLM Decision**  
   The `LLMOrchestrator` sends a prompt to the Ollama LLM to determine whether a tool is needed.  
   Output must follow the `ToolDecision` JSON schema:

   ```json
   {
       "tool_required": true,
       "tool_name": "weather",
       "arguments": {"location": "San Francisco"},
       "final_answer": null
   }
````

3. **Tool Execution**
   If a tool is required, the orchestrator calls `MCPManager.call_tool(tool_name, arguments)` to execute the corresponding MCP server tool.

4. **Final Answer Generation**
   Tool output is sent back to the LLM for final synthesis if necessary.
   The orchestrator returns a unified JSON response to the user.

---

## Features

* Multi-step orchestration: User → LLM → Tool → LLM final answer.
* Support for multiple MCP tools:

  * Weather (`weather-mcp`)
  * Geocoding (`geocoding-mcp`)
  * Search (`searchxng-mcp`)
  * Datetime (`datetime-mcp`)
* Robust JSON parsing and error handling.
* Unified logging for tracing LLM decisions and tool calls.
* FastAPI backend with modular routers.

---

## Directory Structure

```text
backend/
├── src/
│   └── backend/
│       ├── llm/
│       │   ├── orchestrator.py
│       │   ├── mcp_manager.py
│       │   └── schemas.py
│       ├── mcp/
│       │   └── manager.py
│       ├── models/
│       ├── routers/
│       ├── services/
│       ├── tests/
│       └── app.py
frontend/
mcp-servers/
searchxng_svc/
docker-compose.yml
```

---

## Getting Started

1. **Clone the repository**

```bash
git clone <repo_url>
cd ollama-with-mcp
```

2. **Install dependencies for backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Start Docker services**

```bash
docker-compose up --build
```

Services:

* `backend` (FastAPI)
* `weather-mcp`
* `geocoding-mcp`
* `searchxng-mcp`
* `datetime-mcp`
* `frontend`
* `searchxng_svc`

---

## Usage

* **Chat endpoint**: `/chat`
* **Weather endpoint**: `/weather/get`
* **Other MCP tools** are invoked automatically via the orchestrator when necessary.

Example `/chat` request:

```json
{
    "message": "What is the weather in Paris?"
}
```

Example `/chat` response:

```json
{
    "response": "The weather in Paris is sunny with 20°C.",
    "tool_output": {
        "temperature": 20,
        "condition": "sunny",
        "location": "Paris"
    }
}
```

---

## API Endpoints

| Endpoint       | Method | Description                             |
| -------------- | ------ | --------------------------------------- |
| `/chat`        | POST   | Main LLM chat endpoint                  |
| `/weather/get` | POST   | Fetch weather via Weather MCP tool      |
| `/search`      | POST   | Search via SearchXNG MCP tool           |
| `/geocode`     | POST   | Geocode via Geocoding MCP tool          |
| `/datetime`    | POST   | Get formatted datetime via Datetime MCP |

---

## Contributing

1. Create a branch for the issue you are working on (e.g., `phase7/issue-30-orchestrator`).
2. Implement and test features locally.
3. Commit and push changes.
4. Open a pull request and request review.

---

## Notes

* LLM interactions are async using `chat_with_ollama`.
* All MCP calls are routed via `MCPManager` for consistent outputs.
* The orchestrator is fully unit-testable with mocked MCP responses.

```

