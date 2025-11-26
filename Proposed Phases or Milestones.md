PHASE 1 — Repository and Infrastructure Setup
🎯 Goals

Prepare a clean, empty project structure using UV.

Define full architecture layout.

Establish development tooling.

📦 Deliverables

docker-compose.yml skeleton

/backend, /mcp-servers, /frontend directories

FastAPI + UV dependency environment

README with instructions

GitHub project configured

🧪 TDD Tests

The repo builds with uv sync

docker-compose up successfully creates all containers (even empty placeholders)

Health check endpoint for FastAPI returns 200

🔗 Dependencies

None.

PHASE 2 — Implement Basic FastAPI Backend (No LLM Yet)
🎯 Goals

Create FastAPI app scaffold

Implement /health and /chat endpoints

Integrate proper project layout: routers, services, models

📦 Deliverables

Working backend HTTP API (no LLM or MCP yet)

Unit tests for API endpoints

Dockerfile for backend

🧪 TDD Tests

GET /health returns "ok"

POST /chat returns static data

Backend container builds and runs

🔗 Dependencies

Phase 1.

PHASE 3 — Ollama Integration (LLM Only)
🎯 Goals

Connect FastAPI backend to Ollama Granite model

Add LLM response pipeline

📦 Deliverables

/chat now uses ollama.chat() or HTTP API

LLM responds to user messages (no tools yet)

Early logging + monitoring hooks

🧪 TDD Tests

Backend returns real responses from Granite

Errors from Ollama are properly handled

Test suite mocks the Ollama client

🔗 Dependencies

Backend skeleton from Phase 2.

PHASE 4 — Build First MCP Server (“datetime”)

(This is intentionally simple for early validation.)

🎯 Goals

Build MCP server using FastMCP

Expose tool: current_date()

📦 Deliverables

mcp-servers/datetime service

Dockerfile

MCP server running on WebSocket or TCP port

Automatic loading of tool schema via backend MCP client

🧪 TDD Tests

MCP client can connect and retrieve tool metadata

Tool returns correct date

LLM can call tool when instructed (manual prompt)

🔗 Dependencies

FastAPI with LLM integration.

PHASE 5 — Add SearchXNG MCP Server
🎯 Goals

Wrap your SearchXNG container with a FastMCP server

Expose tool: search_web(query)

📦 Deliverables

mcp-servers/searchxng service

Tool calls SearchXNG API internally

Docker container functional

🧪 TDD Tests

MCP tool returns SearchXNG results

Error conditions handled (no results, rate limit, etc.)

LLM chooses tool when asked to “search something”

🔗 Dependencies

Working MCP integration in backend.

PHASE 6 — Add Weather MCP Server
🎯 Goals

Use SearchXNG or another API to get weather

Expose tool: get_weather(location)

📦 Deliverables

mcp-servers/weather service

Weather lookup logic

Environment variable config

🧪 TDD Tests

Weather tool returns structured JSON

Handles “unknown location” gracefully

LLM can chain: search → weather

🔗 Dependencies

SearchXNG MCP stability.

PHASE 7 — FastAPI Orchestration for Multi-Tool Calls
🎯 Goals

Implement multi-server MCP manager

Provide decision routing (LLM → MCP server → LLM)

Add conversation state & context window handling

📦 Deliverables

MCP manager class

Tool call resolution logic

Tool→LLM response chaining

Logging for all tool calls

🧪 TDD Tests

LLM triggers correct MCP tools for different queries

Multi-step workflows succeed (weather after search)

Timeouts handled for slow tools

🔗 Dependencies

All MCP servers built.

PHASE 8 — Frontend (Gradio) Integration
🎯 Goals

Connect Gradio chat UI to FastAPI

Stream responses if desired

Add minimal UI styling

📦 Deliverables

Gradio container

/chat integration with FastAPI

Optional streaming responses

session state

🧪 TDD Tests

Full conversation works through UI

Tool calls visible in logs

Edge-case UI handling (empty input, long queries)

🔗 Dependencies

Backend + MCP orchestration complete.

PHASE 9 — Observability, Logging & Production Hardening
🎯 Goals

Add structured logging

Add Prometheus/Grafana or simpler metrics

Add error reporting

Add environment-specific configs

📦 Deliverables

Centralized logs for LLM + MCP servers

Health checks for each container

Graceful shutdown and restart policies

🧪 TDD Tests

Logging verified in all services

Failing MCP server doesn’t crash backend

Timeouts + fallback logic tested

🔗 Dependencies

Everything functioning end-to-end.

PHASE 10 — Final Documentation and Release
🎯 Goals

Complete documentation

Provide setup guide, architecture diagrams, examples

Prepare production-ready release (v1.0)

📦 Deliverables

README.md

ARCHITECTURE.md

USAGE.md

Sample prompts, test cases

Release build on GitHub

🧪 TDD Tests

New developer can set up system using docs

All containers run cleanly with one command

All previous tests pass in CI

🔗 Dependencies

Full system ready.

