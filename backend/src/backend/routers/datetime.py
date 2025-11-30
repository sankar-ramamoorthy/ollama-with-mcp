from fastapi import APIRouter, HTTPException
from backend.mcp_clients import call_datetime  # <-- call_datetime client function
from pydantic import BaseModel

router = APIRouter(prefix="/datetime", tags=["datetime"])

class DatetimeRequest(BaseModel):
    """Model for datetime request."""
    # You can add fields here if needed. Currently, it's empty.

@router.post("/get")
async def get_datetime():
    """
    Call the Datetime MCP tool to get current Time in UTC.
    """
    result = await call_datetime()
    
    if not result or "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    
    return result
