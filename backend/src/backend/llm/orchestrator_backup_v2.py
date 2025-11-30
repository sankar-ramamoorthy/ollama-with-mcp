import logging
import json
import re
from typing import Dict, Any
from backend.mcp.manager import MCPManager
from backend.services.ollama_service import chat_with_ollama
from backend.llm.schemas import ToolDecision
from backend.llm.prompt_templates import TOOL_DECISION_PROMPT

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LLMOrchestrator:
    """
    Handles multi-step orchestration: user -> LLM -> tool -> LLM final answer
    """

    def __init__(self, model_name: str = "granite4:350m"):
        self.model_name = model_name
        self.mcp_manager = MCPManager()

    async def process_query(self, user_query: str) -> Dict[str, Any]:
        logger.info("\n==================== NEW REQUEST ====================")
        logger.info(f"User Query: {user_query}")

        # Step 1: Build prompt
        decision_prompt = TOOL_DECISION_PROMPT.format(user_query=user_query)
        print(f"\n\n--- DECISION PROMPT SENT TO LLM ---\n{decision_prompt}\n\n")

        # Step 2: Call LLM
        llm_response = await chat_with_ollama(decision_prompt, self.model_name)
        raw_message = llm_response.get("message", "")

        print(f"\n--- RAW LLM RESPONSE ---\n{raw_message}\n")
        logger.info(f"[LLM Decision] Raw response: {raw_message}")

        # Step 3: Extract and repair JSON
        cleaned_json = self._extract_and_fix_json(raw_message)
        print(f"\n--- CLEANED JSON (POST-FIX) ---\n{cleaned_json}\n")

        # Step 4: Parse JSON into ToolDecision
        try:
            decision = ToolDecision.model_validate_json(cleaned_json)
        except Exception as e:
            logger.error(f"Failed to parse cleaned LLM JSON: {e}")

            decision = ToolDecision(
                tool_required=False,
                tool_name=None,
                arguments={},
                final_answer=f"LLM produced invalid JSON: {e}"
            )

        # Step 5: Validate tool choice
        decision = self._validate_tool_decision(decision)

        # Step 6: Tool required
        tool_output = None
        if decision.tool_required and decision.tool_name:
            tool_name = decision.tool_name

            # Construct actual tool function
            tool_func = f"get_{tool_name}"

            print(f"\n--- CALLING TOOL ---\nServer={tool_name}, Function={tool_func}, Args={decision.arguments}\n")
            try:
                tool_output = await self.mcp_manager.call_tool(
                    tool_name,
                    tool_func,
                    decision.arguments or {}
                )
            except Exception as e:
                logger.error(f"Tool call failed: {e}")
                tool_output = {"error": str(e)}

            # Step 7: Send tool output back to LLM for final synthesis
            final_prompt = f"""
The user asked: {user_query}
The tool '{tool_name}' returned this data: {tool_output}

Please produce a final natural-language answer.
"""
            print(f"\n--- FINAL SYNTHESIS PROMPT SENT TO LLM ---\n{final_prompt}\n")

            final_response = await chat_with_ollama(final_prompt, self.model_name)
            final_text = final_response.get("message", "")

            print(f"\n--- FINAL ANSWER FROM LLM ---\n{final_text}\n")

            return {"response": final_text, "tool_output": tool_output}

        # Step 8: Direct answer
        return {"response": decision.final_answer or raw_message, "tool_output": tool_output}

    # ----------------------------------------------------------
    # JSON Extraction + Repair
    # ----------------------------------------------------------
    def _extract_and_fix_json(self, text: str) -> str:
        """
        Extract JSON block, repair missing braces, ensure valid parseable JSON.
        """
        # Extract the first {...} block
        match = re.search(r"{[\s\S]*", text)
        if not match:
            return "{}"

        cleaned = match.group().strip()

        # Fix common JSON errors
        # ------------------------------------------------------
        # 1. Missing final }
        if cleaned.count("{") > cleaned.count("}"):
            cleaned += "}"

        # 2. Ensure "arguments" is always a dict
        cleaned = cleaned.replace('"arguments": null', '"arguments": {}')

        # 3. Ensure commas between fields (Granite often forgets them)
        cleaned = re.sub(r'"\s*\n"', '",\n"', cleaned)

        return cleaned

    # ----------------------------------------------------------
    # Tool Validation
    # ----------------------------------------------------------
    def _validate_tool_decision(self, decision: ToolDecision) -> ToolDecision:
        valid_tools = ["weather", "geocoding", "searchxng", "datetime"]

        if decision.tool_required and decision.tool_name not in valid_tools:
            logger.warning(f"Invalid tool '{decision.tool_name}' — falling back to direct answer.")
            decision.tool_required = False
            decision.tool_name = None
            decision.arguments = {}
            decision.final_answer = "Invalid tool selected; answering directly."

        return decision
