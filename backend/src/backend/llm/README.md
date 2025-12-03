# **LLM Orchestration Module (`backend/src/backend/llm`)**

This directory contains the full **LLM reasoning + tool orchestration layer** for the backend.
It is responsible for:

1. Sending user prompts to **Ollama**
2. Letting the model decide whether to call an **MCP tool**
3. Executing tools via the **MCP Manager**
4. Feeding tool results back into the LLM
5. Returning the final natural-language answer

This is the “brain” of the entire system.

---

# 📁 Directory Structure

```
backend/src/backend/llm/
├── orchestrator.py         # LLM reasoning + tool planning pipeline
├── prompt_templates.py     # System prompts & tool-call formatting logic
├── ollama_service.py       # HTTP client for Ollama models
├── schemas.py              # Pydantic models for LLM messages & tool calls
└── __init__.py
```

---

# 🧠 Overview of Responsibilities

## **1. Orchestrator (`orchestrator.py`)**

Handles *all* LLM interactions and MCP tool workflows.

### Responsibilities:

* Build system + user prompts
* Send prompt to Ollama
* Parse model output
* Detect when a tool should be executed
* Route tool calls to MCP Manager
* Re-ask the LLM with tool results to produce final answer
* Return clean final text to `/chat`

### Core Flow:

```
User → Orchestrator → Ollama → (Tool?) → MCP Manager → LLM → Final Answer
```

This file contains the core algorithm that makes your project an **agent**, not just a chatbot.

---

## **2. Prompt Templates (`prompt_templates.py`)**

Contains reusable message templates including:

* System instructions
* Tool-use guidelines
* Format for tool calls
* Formatting rules for returning tool results to the LLM

This gives models (like Qwen3 or Granite) a consistent structure for:

* Planning
* Deciding tools
* Responding with JSON-based tool call instructions

---

## **3. Ollama Service (`ollama_service.py`)**

A minimal async client that communicates with an Ollama model via:

```
POST http://host.docker.internal:11434/api/generate
```

### Responsibilities:

* Format payload for Ollama
* Handle streaming or non-streaming responses
* Extract model response text
* Surface model or connection errors cleanly

This module isolates all LLM-specific networking.

---

## **4. Schemas (`schemas.py`)**

Defines Pydantic models for:

* LLM messages
* Tool call blocks
* Parsed LLM outputs
* Final orchestrated result models

Examples include:

* `LLMMessage`
* `ToolCall`
* `LLMResponse`
* `OrchestratedResult`

These ensure stable internal typing and clean error handling.

---

# 🔧 How the Orchestrator Works Internally

### **1. Build the conversation structure**

```
system_prompt = build_system_prompt()
user_message = {"role": "user", "content": query}
```

### **2. Send to Ollama**

```
response = ollama_service.ask(messages)
```

### **3. Parse model output**

Look for:

```
<tool name="get_weather">
{ "location": "Tokyo" }
</tool>
```

If found → extract name + arguments.

### **4. Execute tool via MCP Manager**

```
tool_result = mcp_manager.call_tool(name, args)
```

### **5. Send tool result back to the LLM**

```
assistant: "Tool result: { ...json... }"
```

### **6. Return final natural-language answer**

The LLM formats the message for the user.

---

# 🚀 Adding New Tools

To add a new MCP server:

1. Launch MCP server in docker-compose
2. Register it in `mcp/manager.py`
3. Add a new prompt block in `prompt_templates.py`
4. Nothing else — the orchestrator already supports multi-tool execution

---

# 🧪 Testing Strategy

Tests should mock:

* Ollama responses
* MCP tool responses
* Decision-making flow (tool use vs direct answer)

This ensures:

* Deterministic output
* No dependency on LLM variability
* No need for real MCP servers during unit tests

---

# 📘 Additional Notes

### ✔ The orchestrator is model-agnostic

Any Ollama model (Qwen, Granite, LLaMA, Mistral) can be swapped via:

```
model_name="Qwen3:4b"
```

### ✔ Prompt templates are the key to reliability

Minor prompt changes can significantly affect:

* Tool call accuracy
* Planning behavior
* Multi-step workflows

### ✔ Errors are trapped early

Both LLM errors and MCP errors return structured logs to help debugging.

---

# 🧩 Summary

This module is responsible for:

* Reasoning
* Tool selection
* Tool execution
* Final answer generation

It turns a raw LLM into an **autonomous, multi-tool agent** capable of:

* Searching the web
* Fetching weather
* Getting dates/times
* Performing geocoding
* Integrating multiple tools in one conversation

