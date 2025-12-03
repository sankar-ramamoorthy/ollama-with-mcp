# **Backend Models (`backend/src/backend/models`)**

This directory contains all **Pydantic models** used by the FastAPI backend.
These models define the **shape of requests and responses** for the API and internal components.

They serve two main purposes:

1. **Input validation** — Ensuring user-facing HTTP endpoints receive proper JSON.
2. **Structured responses** — Guaranteeing consistent schemas for API and LLM outputs.

---

# 📁 Directory Structure

```
backend/src/backend/models/
├── chat.py        # ChatRequest, ChatResponse
└── __init__.py
```

> Currently the backend uses only a few models.
> Additional models will be added later when test coverage increases or new endpoints need better typing.

---

# 🧩 Model Overview

## **1. Chat Models**

Defined in: `chat.py`

### **`ChatRequest`**

Represents the input to the `/chat` endpoint:

```python
class ChatRequest(BaseModel):
    message: str
```

Used when a user sends a message from:

* Gradio frontend
* External API client
* CLI testing

Ensures that the backend always receives a single, clean string message.

---

### **`ChatResponse`**

Represents the output of the `/chat` endpoint:

```python
class ChatResponse(BaseModel):
    response: str
```

This response includes the **final LLM-generated text**, after:

* tool calling
* MCP chaining
* orchestrator formatting

---

# 🧠 Role in Backend Architecture

Models form the boundary layer around the FastAPI routers:

```
User → Gradio → POST /chat → ChatRequest
           Backend processes via:
           LLM Orchestrator → MCP Tools → Format reply
Response → ChatResponse → UI
```

These models ensure:

* predictable structures for API consumers
* schema validation during development
* consistent OpenAPI documentation

---

# 🛠️ Extending the Models

As the project evolves, models may be added for:

| Feature                 | Model Example                       |
| ----------------------- | ----------------------------------- |
| Geocoding endpoint      | `GeocodeRequest`, `GeocodeResponse` |
| Weather endpoint        | `WeatherRequest`, `WeatherResponse` |
| Search endpoint         | `SearchRequest`, `SearchResponse`   |
| Internal tool-call DTOs | `ToolCallRequest`, `ToolCallResult` |
| LLM orchestration       | `LLMMessage`, `LLMToolCall`, etc.   |

As an enhancement, we may need to  create a **uniform naming convention** such as:

```
<Feature>Request
<Feature>Response
<Feature>Error
```

Just say "generate expanded models" if you'd like to build those out now.

---

# 🧪 Testing Expectations

Models should be covered by simple unit tests:

* Type validation (strings, ints, required fields)
* Missing field handling
* OpenAPI inclusion

Currently tests may be incomplete, and expanding the model suite will make test coverage more robust.

---

# 📘 Summary

The `models` directory defines the core request/response formats used throughout the backend.

* They keep API behavior predictable.
* They guarantee clean JSON structures.
* They serve as a contract between Frontend ↔ Backend ↔ LLM orchestrator.

As the multi-tool architecture expands, additional models can be added at any time.

