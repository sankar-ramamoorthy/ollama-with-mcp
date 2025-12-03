# Backend Router Architecture

This document describes how **FastAPI routers** connect to **MCP servers** and the **LLM orchestrator**, including the flow of requests from the frontend UI to the backend services.

---

## 1. High-Level Flow

```
Frontend / UI
     |
     v
+---------------------------+
| FastAPI Backend           |
|  Routers                  |
|---------------------------|
| /chat                     | ---> chat_reply() --> LLM Orchestrator (Granite)
| /mcp/ddgs                 | ---> call_ddgs()      --> DDGS MCP (50052)
| /mcp/weather              | ---> call_weather()   --> Weather MCP (50053)
| /mcp/geocoding            | ---> call_geocoding() --> Geocoding MCP (50054)
| /mcp/datetime             | ---> call_datetime()  --> Datetime MCP (50051)
+---------------------------+
     |
     v
```

---

## 2. MCP Server Overview

| MCP Server    | Router Endpoint  | Port  | Purpose / Notes                       |
| ------------- | ---------------- | ----- | ------------------------------------- |
| DDGS MCP      | `/mcp/ddgs`      | 50052 | DuckDuckGo web search results         |
| Weather MCP   | `/mcp/weather`   | 50053 | Current weather info via Open-Meteo   |
| Geocoding MCP | `/mcp/geocoding` | 50054 | Convert location → latitude/longitude |
| Datetime MCP  | `/mcp/datetime`  | 50051 | Returns current UTC datetime          |

---

## 3. Router → MCP Flow Diagram

```
Frontend / UI
     |
     v
+---------------------------+
| FastAPI Backend           |
|  Routers                  |
+---------------------------+
     |
     v
+-----------------+       +-----------------+       +-----------------+
| DDGS MCP        |       | Weather MCP     |       | Geocoding MCP   |
| Port 50052      |       | Port 50053      |       | Port 50054      |
+-----------------+       +-----------------+       +-----------------+
     |                         |                         |
     v                         v                         v
DuckDuckGo API           Weather source           Geocoding API
```

```
+-----------------+
| Datetime MCP    |
| Port 50051      |
+-----------------+
     |
     v
 System Clock / ISO Time
```

---

## 4. Key Notes

* `/chat` is **LLM-focused**, calling `chat_reply()` which may in turn call MCP tools via orchestrator.
* MCP routers `/mcp/*` **proxy async calls** to MCP servers. The frontend never calls MCP directly.
* Multi-step flows are supported. Example:

  1. `/mcp/weather?location=Paris` → calls Geocoding MCP → Weather MCP → returns structured JSON.
* MCP servers are **independent**, each handling one domain of functionality.
* All routers return **structured JSON**, including errors.
* MCP ports are standardized and fixed for consistent orchestration.

