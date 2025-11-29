# backend/src/backend/llm/orchestrator.py

import logging
from typing import Dict, Any
from backend.llm.mcp_manager import MCPManager
from backend.services.ollama_service import chat_with_ollama
from backend.llm.schemas import ToolDecision
from backend.llm.prompt_templates import TOOL_DECISION_PROMPT

logger = logging.getLogger(__name__)

class LLMOrchestrator:
    """
    Handles multi-step orchestration: user -> LLM -> tool -> LLM final answer
    """

    def __init__(self, model_name: str = "granite4:350m"):
        self.model_name = model_name
        self.mcp_manager = MCPManager()

    async def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Main orchestrator method.
        Steps:
        1. Ask LLM whether a tool is needed (using standardized prompt template)
        2. Parse LLM response into ToolDecision
        3. Call MCPManager if tool is required
        4. Send tool output back to LLM for final synthesis
        5. Return final answer
        """
        # Step 1: Build prompt
        decision_prompt = TOOL_DECISION_PROMPT.format(user_query=user_query)

        # Step 2: Call LLM
        llm_response = await chat_with_ollama(decision_prompt, self.model_name)
        raw_message = llm_response.get("message", "{}")
        logger.info(f"[LLM Decision] Raw response: {raw_message}")

        # Step 3: Parse LLM response into ToolDecision
        try:
            decision = ToolDecision.parse_raw(raw_message)
        except Exception as e:
            logger.error(f"Failed to parse LLM decision: {e}")
            # Fallback: direct answer with error info
            decision = ToolDecision(
                tool_required=False,
                tool_name=None,
                arguments={},
                final_answer=f"LLM failed to produce a valid decision: {str(e)}"
            )

        # Step 4: Validate tool choice
        decision = self._validate_tool_decision(decision)

        # Step 5: Call tool if required
        tool_output = None
        if decision.tool_required and decision.tool_name:
            try:
                tool_output = await self.mcp_manager.call_tool(
                    decision.tool_name, decision.tool_name, decision.arguments or {}
                )
            except Exception as e:
                logger.error(f"Tool call failed: {e}")
                tool_output = {"error": f"Tool execution failed: {str(e)}"}

            # Step 6: Send tool output back to LLM for final synthesis
            final_prompt = f"""
            User query: {user_query}
            Tool {decision.tool_name} output: {tool_output}
            Please generate a final answer combining the information.
            """
            final_response = await chat_with_ollama(final_prompt, self.model_name)
            return {"response": final_response.get("message", ""), "tool_output": tool_output}

        # Step 7: Direct answer scenario
        return {"response": decision.final_answer or raw_message, "tool_output": tool_output}

    def _validate_tool_decision(self, decision: ToolDecision) -> ToolDecision:
        """
        Ensure tool decisions are valid.
        """
        valid_tools = ["weather", "geocoding", "searchxng", "datetime"]
        if decision.tool_required and decision.tool_name not in valid_tools:
            logger.warning(f"Invalid tool_name received: {decision.tool_name}. Setting tool_required=False")
            decision.tool_required = False
            decision.tool_name = None
            decision.arguments = {}
        return decision
