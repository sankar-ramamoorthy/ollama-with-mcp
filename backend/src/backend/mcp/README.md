# **MCP Client Layer (`backend/src/backend/mcp`)**

This directory contains the **MCP (Model Context Protocol) coordination layer** for the backend.
It enables the LLM Orchestrator to call external microservices such as:

* `datetime-mcp`
* `ddgs-mcp` (DuckDuckGo search)
* `weather-mcp`
* `geocoding-mcp`

These MCP servers act as lightweight “tools” the LLM can invoke when needed.

---

# 📁 Directory Structure

```
backend/src/backend/mcp/
├── manager.py       # Multi-tool MCP manager used by Orchestrator
└── __init__.py
```

> **Note**: Direct router-level MCP calls (`call_get_current_datetime`, `call_weather`, etc.)
> live in **`mcp_clients.py`** at the root of the backend package.
>
> This `mcp` directory focuses on the **agent/tool orchestration path**, not the REST endpoints.

---

# 🧠 Purpose

This module provides:

* A unified interface for all MCP servers
* Automatic connection logic (host, port, tool name)
* A thin wrapper around FastMCP client calls
* Simplified error handling for tool failures
* A stable API that the **LLM Orchestrator** uses to call tools

It is the glue that connects:

```
LLM (decides a tool is needed)
     → MCP Manager (executes the tool)
          → MCP Server (provides data)
```

---

# 🔧 How It Works

## **1. Tool Registry**

`manager.py` defines a mapping such as:

```python
{
    "get_current_datetime": {"host": "datetime-mcp", "port": 50051},
    "search_ddgs":         {"host": "ddgs-mcp",      "port": 50052},
    "get_weather":         {"host": "weather-mcp",   "port": 50053},
    "geocode":             {"host": "geocoding-mcp", "port": 50054},
}
```

Each entry tells the manager:

* Which MCP server to call
* What port it runs on
* What function/tool name exists on that server

This allows the orchestrator to simply say:

```
execute_tool("get_weather", {"location": "Paris"})
```

and the manager handles the entire call.

---

## **2. Executing a Tool Call**

When the orchestrator requests a tool:

```python
result = await mcp_manager.call_tool(tool_name, args)
```

The manager:

1. Looks up correct host/port for the tool
2. Creates a FastMCP client
3. Calls the tool using:

   ```
   await client.call(tool_name, args)
   ```
4. Returns structured JSON back to the orchestrator

If the tool fails or returns malformed data, the manager standardizes the error:

```json
{ "error": "Weather MCP unavailable on port 50053" }
```

---

# 🧱 Responsibilities of MCP Manager

### ✔ Normalize MCP connections

Provides a stable way to connect to multiple MCP servers.

### ✔ Abstract network differences

Routers and orchestrator don’t need to know ports or hosts.

### ✔ Validate tool existence

Avoids calling non-existent tools.

### ✔ Provide predictable error structure

LLM can reason about failures if needed.

### ✔ Provide async interface

All MCP interactions are `async` to avoid blocking FastAPI.

---

# 🧩 Integration with Other Components

### **Orchestrator → MCP Manager**

The orchestrator uses MCP Manager for all tool calls.

Example flow:

```
User asks “Weather in Tokyo?”
↓
LLM decides: tool weather.get_weather({
    "location": "Tokyo"
})
↓
MCP Manager calls weather-mcp:50053
↓
Weather MCP calls Geocoding MCP (internal)
↓
Result returned to Orchestrator
↓
LLM writes final answer
```

Routing and retry logic is entirely hidden inside MCP Manager.

---

# ⚠️ Difference Between `mcp` and `mcp_clients.py`

| Component            | Purpose                                                                         |
| -------------------- | ------------------------------------------------------------------------------- |
| **`mcp/manager.py`** | Used by the LLM **orchestrator** for agent tool execution                       |
| **`mcp_clients.py`** | Used by FastAPI **routers** as REST endpoints (`/datetime/get`, `/weather/get`) |

Both call the same MCP servers — but for different use cases.

---

# 🔧 Adding a New Tool (Example)

To add a new MCP server:

### Step 1 — Add service to `docker-compose.yml`

### Step 2 — Register tool in `manager.py`

```python
"get_joke": {"host": "joke-mcp", "port": 50055}
```

### Step 3 — Add a prompt hint in `prompt_templates.py`

### Step 4 — No change needed in orchestrator

It automatically supports the new tool.

---

# 🧪 Testing

Tests for this module should:

* Mock FastMCP clients
* Verify correct host/port resolution
* Ensure errors (timeouts, connection failures) return standardized objects
* Check proper detection of unknown tools

No MCP servers need to run during unit tests.

---

# 📘 Summary

The MCP Manager is the **tool execution backbone** of the entire agent system.

It provides:

* Unified tool calling
* Stable error handling
* Automatic routing
* Async execution
* Clean separation between orchestrator and network logic

Without this module, the LLM wouldn’t be able to delegate tasks to specialized microservices.

