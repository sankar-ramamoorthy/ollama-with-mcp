# Gradio Frontend API

This directory contains the **Gradio frontend application** for interacting with the backend LLM and MCP tools.

The Gradio app provides a simple chat UI where users can:

* Send messages to the backend `/chat` endpoint.
* Receive LLM responses.
* Trigger MCP tool calls (weather, search, geocoding) indirectly via the backend.

---

## 🏗️ Project Structure

```
frontend/src/gradio_api/
├── app.py          # Main Gradio app
├── __init__.py
```

* `app.py` – Launches the Gradio chat interface, handles input/output, maintains session state.
* `__init__.py` – Marks this folder as a Python package.

---

## ⚡ Key Features

* **Chat interface:** Users type messages and receive responses from the backend LLM.
* **History tracking:** Conversation history is stored in-memory per session using `gr.State`.
* **Debug logging:** Detailed logs of messages sent to the backend and responses received.
* **Automatic clearing of input box** after each submission for smooth UX.
* **Backend integration:** Sends POST requests to the configured backend endpoint (`BACKEND_URL`) and updates the chat interface asynchronously.

---

## 🔌 Configuration

```python
BACKEND_URL = "http://backend:8000/chat"
```

* Adjust `BACKEND_URL` if the backend is hosted elsewhere.
* The frontend relies on structured JSON responses from the backend.

---

## 🚀 Running the App

**Locally (with uv):**

```bash
cd frontend
uv sync      # Install dependencies from pyproject.toml
uv run -m src.gradio_api.app
```

* Default server: `0.0.0.0:7860`
* Access via browser: `http://localhost:7860`

**Docker:**

```bash
docker build -t gradio-frontend ./frontend
docker run -p 7860:7860 gradio-frontend
```

---

## 🧩 How It Works

1. User types a message in the chat textbox.
2. Message is submitted via Gradio to `chat_with_backend`.
3. Function formats message and history, sends POST request to backend `/chat`.
4. Backend responds with either:

   * LLM reply
   * MCP tool output (if the LLM triggered a tool)
5. Gradio updates:

   * `Chatbot` UI
   * `state` history
   * `debug_output` textbox

---

## 💡 Notes for Developers

* Keep frontend logic **stateless**, session state is maintained via `gr.State`.
* Avoid direct MCP calls from frontend — always go through the backend for security and orchestration.
* Debug log output is useful for testing multi-step tool workflows.
* Can be extended to **streaming responses** if backend supports streaming.


```
User (Browser)
     │
     ▼
+---------------------+
|   Gradio Frontend   |  <-- app.py
|  (Chat UI + State)  |
+---------------------+
     │ POST /chat
     ▼
+---------------------+
| FastAPI Backend     |  <-- routers/chat.py
| LLM Orchestrator    |
+---------------------+
     │ MCP Tool Calls
     ▼
+----------------------+       +----------------------+
| SearchXNG MCP Server |       | Weather MCP Server   |
| Port 50052           |       | Port 50053           |
+----------------------+       +----------------------+
     │                              │
     ▼                              ▼
  Search API / DB               Weather API / Source
```

**Legend / Notes:**

* All MCP tool calls go through the backend; the frontend never calls MCP servers directly.
* `Gradio Frontend` handles session history and debug logs.
* LLM orchestrator in the backend decides if an MCP tool needs to be called based on the user message.
* Can be extended to include `datetime` or `geocoding` MCP servers similarly.

---
