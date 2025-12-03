
# 📡 FastAPI Routers Overview

This directory contains all **API routers** for the backend service. Each router exposes endpoints for either **LLM chat requests** or **tool calls via MCP servers**.

These routers **decouple FastAPI endpoints from MCP server logic**, making it easier to extend, test, and maintain.

---

## 1. `chat.py`

**Purpose:**
Handles conversational chat requests and responses using the internal LLM pipeline. This is the main endpoint for user interaction with the AI.

**Structure:**

* `router = APIRouter()` – no prefix, endpoint `/chat`.
* Endpoint:

```python
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await chat_reply(request)
```

* Uses **Pydantic models** `ChatRequest` and `ChatResponse` for structured input/output.
* Delegates all logic to `chat_reply` in `backend/services/chat_service.py`.
* Fully async to support concurrent requests and LLM calls.

**Key Notes:**

* Focused on LLM responses only; no external tools involved.
* Error handling and response formatting handled inside `chat_reply`.
* Easily extended to add conversation context, streaming, or logging.

---

## 2. `search.py`

**Purpose:**
Exposes a backend endpoint to query the **DDGS MCP tool**. Acts as a bridge between FastAPI and the external MCP server for web search.

**Structure:**

* `router = APIRouter(prefix="/mcp", tags=["MCP"])`
* Endpoint:

```python
@router.get("/search")
async def search_endpoint(query: str = Query(..., description="Search query")):
    mcp_result: CallToolResult = await call_ddgs(query)
    result_data = mcp_result.structured_content or mcp_result.content
    if "error" in result_data:
        return {"success": False, "error": result_data["error"], "results": []}
    return {"success": True, "query": query, "results": result_data.get("results", [])}
```

* Uses **async MCP client** `call_ddgs` to fetch results.
* Wraps MCP call results into a **consistent JSON response** for the frontend.

**Key Notes:**

* Acts as a “proxy” to the MCP server; frontend never communicates with MCP directly.
* Handles errors gracefully: if the MCP tool fails, the endpoint returns a structured error response.
* Fully async for concurrency and performance.

---

## 3. `weather.py`

**Purpose:**
Exposes a backend endpoint to fetch weather data via the **Weather MCP tool**. Follows the same design pattern as `search.py`.

**Structure:**

* `router = APIRouter(prefix="/mcp", tags=["MCP"])`
* Endpoint:

```python
@router.get("/weather")
async def weather_endpoint(location: str = Query(..., description="Location name")):
    weather_data = await call_weather(location)
    if "error" in weather_data:
        return {"success": False, "error": weather_data["error"], "data": {}}
    return {"success": True, "location": location, "data": weather_data}
```

* Uses **async MCP client** `call_weather`.
* Returns **structured JSON**, e.g., temperature, condition, and source.

**Key Notes:**

* Decouples FastAPI backend from MCP logic.
* Handles errors and invalid inputs gracefully.
* Can be extended to include caching, logging, or multi-step tool chaining.

---

## 4. Comparison Table

| Aspect             | `chat.py`                       | `search.py`           | `weather.py`             |
| ------------------ | ------------------------------- | --------------------- | ------------------------ |
| **Purpose**        | LLM chat                        | DDGS MCP              | Weather MCP              |
| **Endpoint**       | `/chat`                         | `/mcp/search`         | `/mcp/weather`           |
| **Input**          | ChatRequest                     | query string          | location string          |
| **Output**         | ChatResponse                    | JSON with results     | JSON with weather data   |
| **Backend Call**   | internal `chat_reply`           | async MCP `call_ddgs` | async MCP `call_weather` |
| **Error Handling** | inside chat service             | wraps MCP error       | wraps MCP error          |
| **Async**          | yes                             | yes                   | yes                      |
| **Extensibility**  | conversation context, streaming | additional MCP tools  | additional MCP tools     |

---

## 5. Router Template for New MCP Tools

Use this template to add new MCP endpoints consistently:

```python
from fastapi import APIRouter, Query
from backend.mcp_clients import call_<tool_name>

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.get("/<tool_name>")
async def <tool_name>_endpoint(param: str = Query(..., description="Input description")):
    """
    Call the <ToolName> MCP tool via backend client.
    Returns MCP server results.
    """
    tool_data = await call_<tool_name>(param)
    if "error" in tool_data:
        return {"success": False, "error": tool_data["error"], "data": {}}
    return {"success": True, "param": param, "data": tool_data}
```

**Instructions:**

1. Replace `<tool_name>` with the lowercase name of your MCP tool.
2. Replace `param` and description with your tool-specific input.
3. Implement the corresponding async client function in `backend/mcp_clients.py`.
4. Add proper error handling and structured JSON output.

This ensures all MCP routers are **consistent**, easy to maintain, and fully async.

---

## 6. ASCII Architecture Diagram

```
Frontend (Gradio)
        |
        v
+-----------------------+
| FastAPI Backend       |
| Routers + LLM         |
+-----------------------+
| /chat                 | ---> chat_reply() --> LLM
| /mcp/search           | ---> call_ddgs() --> DDGS MCP
| /mcp/weather          | ---> call_weather() --> Weather MCP
+-----------------------+
         |
         v
+----------------+     +----------------+
| ddgs-MCP       |     | weather-MCP    |
| Port 50052     |     | Port 50053     |
+----------------+     +----------------+
                          |
                          v
                     geocoding-MCP
                     Port 50054
```

---

This keeps your **routers documentation up-to-date** with the current DDGS MCP integration.

