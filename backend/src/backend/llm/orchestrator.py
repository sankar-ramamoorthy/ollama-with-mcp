# backend/src/backend/llm/orchestrator.py

import json
import logging
from typing import Any, Dict

from backend.llm.prompt_templates import TOOL_DECISION_PROMPT, FINAL_ANSWER_PROMPT
from fastmcp import Client
from fastmcp.client.client import CallToolResult
from backend.mcp.manager import MCPManager
from backend.services.ollama_service import chat_with_ollama

logger = logging.getLogger(__name__)
DEFAULT_MODEL = "Qwen3:4b"

# MCP server URLs
MCP_SERVERS = {
    "weather": "http://weather-mcp:50053/mcp",
    "geocoding": "http://geocoding-mcp:50054/mcp",
    "datetime": "http://datetime-mcp:50051/mcp",
    #"searchxng": "http://searchxng-mcp:50052/mcp",
    "ddgs": "http://ddgs-mcp:50052/mcp",  # ← Replace searchxng
}


# Mapping from high-level tool_name to actual MCP function names
TOOL_NAME_TO_MCP_FUNCTION = {
    "weather": "get_weather_tool",      # ✅ Matches weather_mcp/server.py
    "get_weather_tool": "get_weather_tool",      # ✅ Matches weather_mcp/server.py
    "geocoding": "geocode_tool",        # ✅ Matches geocoding_mcp/server.py
    "geocode_tool": "geocode_tool",        # ✅ Matches geocoding_mcp/server.py
    "datetime": "get_current_datetime_tool", # ✅ Matches datetime_mcp/server.py
    "get_current_datetime": "get_current_datetime_tool", # ✅ Matches datetime_mcp/server.py
    #"searchxng": "search_web",          # ✅ Matches searchxng_mcp/server.py
    #"search_web": "search_web",          # ✅ Matches searchxng_mcp/server.py
    "ddgs": "web_search_tool",      # ← Replace searchxng
    "web_search": "web_search_tool",

}


class ChatOrchestrator:
    """
    Handles multi-step orchestration: user -> LLM -> tool -> LLM final answer
    """

    def __init__(self, model_name: str = "Qwen3:4b"):
        self.model_name = model_name
        print("in __init__")
        self.mcp_manager = MCPManager()

    async def process_query(self, user_query: str) -> str:
        """
        Process a user query through the LLM to decide on a tool call,
        execute the tool if required, and synthesize the final answer.
        """
        print("ChatOrchestrator user_query",user_query)
        logger.info("\n==================== NEW REQUEST ====================")
        logger.info(f"User Query: {user_query}")

        # 1. Build decision prompt for LLM
        decision_prompt = TOOL_DECISION_PROMPT.format(user_query=user_query)
        print(f"\n\n--- DECISION PROMPT SENT TO LLM ---\n{decision_prompt}\n\n")


        # 2. Call LLM to decide tool usage
        #llm_response = await self.call_llm(decision_prompt)
        llm_response = await chat_with_ollama(decision_prompt, self.model_name)
        print(f"\n\n--- LLM RESPONSE WITH DECISION ---\n{llm_response}\n\n")


        # 3. Parse JSON safely
        try:
            #decision = json.loads(llm_response)
            # Extract JSON string from Ollama response format
            if isinstance(llm_response, dict):
                llm_response = llm_response.get('message', '{}')
            decision = json.loads(llm_response)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM decision JSON: {e}")
            return "Sorry, I could not understand the request."
        # 4. Check if tool_name exists (ignore tool_required)
        tool_name = decision.get("tool_name")
        if not tool_name:  # "", null, None
            final_answer = decision.get("final_answer")
            return final_answer or "No specific answer available."

        #tool_required = decision.get("tool_required", False)

        #if not tool_required:
        #    # No tool call – just return the LLM's direct answer
        #    return decision.get("final_answer", "Sorry, I have no answer.")

        # 4. Map high-level tool name to MCP function
        #tool_name = decision.get("tool_name")
        mcp_function = TOOL_NAME_TO_MCP_FUNCTION.get(tool_name)

        if not mcp_function:
            logger.error(f"No MCP function mapping found for tool_name={tool_name}")
            return "Sorry, the requested tool is not available."

        mcp_url = MCP_SERVERS.get(tool_name)
        if not mcp_url:
            logger.error(f"No MCP server URL found for tool_name={tool_name}")
            return "Sorry, the requested tool server is not available."
        print("tool_name",tool_name,"mcp_function",mcp_function,"mcp_url",mcp_url)    
        print("decision.get arguments, {}",decision.get("arguments", {}))

        # 5. Call the MCP tool
        try:
            async with Client(mcp_url) as client:
                mcp_response: CallToolResult = await client.call_tool(
                    mcp_function,
                    decision.get("arguments", {}) or {},
                )
        except Exception as e:
            logger.error(f"Error calling MCP tool: {e}")
            return f"Error executing tool: {e}"

        # 6. Synthesize final answer using LLM
        tool_payload = mcp_response.structured_content or mcp_response.content

        # Handle FastMCP response types (TextContent, dict, etc.)
        if hasattr(tool_payload, 'text'):
            tool_response = tool_payload.text
        elif hasattr(tool_payload, 'content'):
            tool_response = tool_payload.content
        elif isinstance(tool_payload, (str, dict)):
            tool_response = tool_payload if isinstance(tool_payload, str) else json.dumps(tool_payload)
        else:
            tool_response = str(tool_payload)
            
        final_prompt = FINAL_ANSWER_PROMPT.format(
            user_message=user_query,
            tool_name=tool_name,
            tool_response=tool_response,
        )

        #final_answer = await self.call_llm(final_prompt)



        # Step 7: Send tool output back to LLM for final synthesis
        print(f"\n--- FINAL SYNTHESIS PROMPT SENT TO LLM ---\n{final_prompt}\n")

        final_response = await chat_with_ollama(final_prompt, self.model_name)
        final_text = final_response.get("message", "")

        print(f"\n--- FINAL ANSWER FROM LLM ---\n{final_text}\n")

        #return {"response": final_text, "tool_output": tool_output}

        # Step 8: Direct answer
        #return {"response": decision.final_answer or raw_message, "tool_output": tool_output}


        #return final_answer
        return final_text

    # ---------------------------
    # Stub LLM call (replace with your LLM client)
    # ---------------------------
    async def call_llm(self, prompt: str) -> str:
        """
        Call your LLM with the given prompt.
        Replace this stub with your actual LLM client call.
        """
        logger.info(f"LLM prompt: {prompt}")
        print("call_llm: prompt",prompt)
        # This stub returns a valid JSON decision with no tool usage
        return (
            '{"tool_required": false, "tool_name": null, "arguments": {}, '
            '"final_answer": "Stub answer"}'
        )


# ---------------------------
# Singleton orchestrator instance
# ---------------------------
model_name = DEFAULT_MODEL
orchestrator = ChatOrchestrator(model_name=model_name)
