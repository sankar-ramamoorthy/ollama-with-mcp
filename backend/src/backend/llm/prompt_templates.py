# backend/src/backend/llm/prompt_templates.py

TOOL_DECISION_PROMPT = """You are an assistant that decides whether a user query requires calling a backend tool (MCP server) or can be answered directly.

IMPORTANT:
- The tool name you output MUST match the actual MCP tool names:

Available servers and their tools:

1. Weather Server (weather)
   - tool: get_weather_tool
   - args: {{"location": "string"}}

2. Geocoding Server (geocoding)
   - tool: geocode_tool
   - args: {{"address": "string"}}

3. Datetime Server (datetime)
   - tool: get_current_datetime_tool
   - args: {{}}

4. Search Server (ddgs)
   - tool: search_web_tool
   - args: {{"query": "string"}}

Your output MUST be strict JSON:
{{"tool_required": true/false, "tool_name": "weather/geocoding/datetime/ddgs", "arguments": {{}}, "final_answer": "answer or null"}}

Examples:
Weather: {{"tool_required": true, "tool_name": "weather", "arguments": {{"location": "Paris"}}, "final_answer": null}}
Geocoding: {{"tool_required": true, "tool_name": "geocoding", "arguments": {{"address": "Chicago"}}, "final_answer": null}}
Datetime: {{"tool_required": true, "tool_name": "datetime", "arguments": {{}}, "final_answer": null}}
Search: {{"tool_required": true, "tool_name": "ddgs", "arguments": {{"query": "News of the day"}}, "final_answer": null}}

Now process this user query:
{user_query}"""

FINAL_ANSWER_PROMPT = """The user asked: {user_message}

The tool '{tool_name}' returned this data:
{tool_response}

Please convert this into a natural-language answer suitable for the user."""
