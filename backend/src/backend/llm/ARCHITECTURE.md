---

```markdown
# Architecture — Ollama with MCP Backend

## Overview

This system provides a **multi-step orchestration engine** for processing user queries via an LLM (Ollama) with optional tool execution through multiple MCP servers. It is designed for modularity, testability, and clear separation of concerns.

---

## Components

### 1. FastAPI Backend
- Receives user requests via `/chat` or other MCP-specific endpoints.
- Routes queries to `LLMOrchestrator` for decision-making.
- Includes routers for specific MCP tools (weather, geocoding, search, datetime).

### 2. LLM Orchestrator (`LLMOrchestrator`)
- Core class responsible for multi-step orchestration:
  1. Sends the user query to the LLM.
  2. Parses LLM JSON response using `ToolDecision` schema.
  3. Calls appropriate tool via `MCPManager` if required.
  4. Sends tool output back to LLM for final answer synthesis.
  5. Returns unified JSON response to API client.

- Handles both **direct answer scenarios** and **tool-required scenarios**.
- Logs each step for observability.

### 3. MCPManager
- Provides a **unified API** to interact with multiple MCP servers.
- Maintains a registry of available MCP servers:
  - `datetime`
  - `searchxng`
  - `weather`
  - `geocoding`
- Normalizes responses to a consistent dictionary format.
- Manages errors gracefully.

### 4. MCP Servers
Each MCP server runs as a separate Docker service:

| Service          | Port  | Responsibility                         |
|-----------------|-------|----------------------------------------|
| `datetime-mcp`   | 50051 | Returns formatted datetime for timestamps |
| `searchxng-mcp`  | 50052 | Executes web searches                  |
| `weather-mcp`    | 50053 | Returns weather information            |
| `geocoding-mcp`  | 50054 | Returns latitude/longitude for addresses |

- Servers communicate via HTTP APIs using the `fastmcp.Client`.

### 5. Ollama LLM
- Runs on host at `http://host.docker.internal:11434/api/generate`.
- Provides decision-making and response synthesis for queries.
- Returns JSON responses for tool decisions and final answers.

---

## Data Flow

```

User
│
│ POST /chat {"message": "What is the weather in Paris?"}
▼
FastAPI Chat Router
│
│ forwards message
▼
LLMOrchestrator.process_query()
│
│ Step 1: Send LLM decision prompt
▼
Ollama LLM
│
│ returns JSON: {"tool_required": true, "tool_name": "weather", "arguments": {"location": "Paris"}}
▼
LLMOrchestrator
│
│ Step 2: Parse JSON → ToolDecision
│
│ Step 3: Call MCP tool if needed
▼
MCPManager.call_tool("weather", {"location": "Paris"})
│
▼
Weather MCP Server
│
│ returns weather data
▼
MCPManager → LLMOrchestrator
│
│ Step 4: Send tool output back to LLM for final answer
▼
Ollama LLM
│
│ returns synthesized final answer
▼
LLMOrchestrator → FastAPI
│
│ Step 5: Return unified JSON response
▼
User receives final response

```

---

## Key Design Principles

1. **Modularity**  
   Each MCP tool and LLM logic is separated for easy testing and future extension.

2. **Unified Output**  
   All MCP responses are normalized by `MCPManager` to a consistent dictionary structure.

3. **Error Handling**  
   LLM parsing errors, MCP tool errors, and network issues are logged and returned gracefully.

4. **Async First**  
   All API calls, LLM interactions, and MCP calls are async for optimal performance.

5. **Extensible Orchestration**  
   Adding new MCP tools or modifying LLM prompts requires minimal changes in `LLMOrchestrator`.

---

## Next Steps / Future Enhancements

- Finalize **prompt templates** for consistent `ToolDecision` JSON output.
- Add **unit and integration tests** for orchestration flow.
- Extend support for additional MCP tools (e.g., NLP, analytics, file processing).
- Implement **streaming responses** for long-running LLM tasks.
```

---
