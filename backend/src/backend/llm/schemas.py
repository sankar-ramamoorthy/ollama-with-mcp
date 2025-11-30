from pydantic import BaseModel
from typing import Optional, Dict, Any

class ToolDecision(BaseModel):
    tool_required: bool
    tool_name: Optional[str]
    arguments: Optional[Dict[str, Any]]
    final_answer: Optional[str]  # Optional direct answer if tool not required
