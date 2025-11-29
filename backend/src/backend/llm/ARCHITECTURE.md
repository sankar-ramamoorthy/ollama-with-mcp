
## **ARCHITECTURE.md**

```markdown
# Ollama-with-MCP Architecture

## **High-Level Architecture**

````

+--------------------+
|      User/API      |
+--------------------+
|
v
+--------------------+
|   /chat Endpoint   |
| (FastAPI Router)   |
+--------------------+
|
v
+--------------------+
|  LLM Orchestrator  |
| - Decides if tool  |
|   is required      |
| - Calls MCPManager |
+--------------------+
|
v
+--------------------+
|   MCPManager       |
| - Handles multiple |
|   MCP servers      |
| - Normalizes output|
+--------------------+
|      |      |
v      v      v
+-------+ +-------+ +---------+
|Weather| |Geocoding| |Datetime|
| MCP   | | MCP     | | MCP    |
+-------+ +-------+ +---------+
|
v
+--------------------+
|  LLM Final Answer  |
| - Synthesizes tool |
|   output & user    |
+--------------------+
|
v
+--------------------+
|      User/API      |
+--------------------+

```

---

## **Components**

### **LLM Orchestrator**
- Determines if a tool call is needed.
- Returns direct answer if no tool required.
- Calls `MCPManager` for tool execution.
- Synthesizes final response.

### **MCPManager**
- Registry of MCP servers:
  - Datetime, SearchXNG, Weather, Geocoding
- Unified `call_tool(server, tool, args)` interface.
- Normalizes responses.

### **MCP Servers**
- Individual services (Docker containers)
- Each exposes tools like `get_weather_tool`, `geocode_tool`, `datetime_tool`.
- Communicate via HTTP + MCP protocol.

### **Gradio Frontend**
- Interacts with `/chat` endpoint.
- Receives final LLM answer + optional tool outputs.

---

## **Data Flow**

1. User submits a message to `/chat`.
2. Orchestrator sends a decision prompt to LLM.
3. LLM responds with `ToolDecision` JSON.
4. If a tool is required:
   - MCPManager calls the corresponding MCP server tool.
   - Normalized output is returned.
5. Orchestrator sends tool output back to LLM for final synthesis.
6. Response returned to user.

---

## **Notes**
- Each MCP server runs in its own Docker container.
- LLM calls are asynchronous.
- Normalized outputs ensure consistent JSON structure.
- `__init__.py` present in all directories to mark them as Python packages.
```

