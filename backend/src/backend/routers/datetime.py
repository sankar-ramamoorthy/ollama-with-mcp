from fastapi import APIRouter, HTTPException
from backend.mcp_clients import call_datetime  # <-- call_datetime client function
from pydantic import BaseModel

router = APIRouter(prefix="/datetime", tags=["datetime"])

class DatetimeRequest(BaseModel):
    timestamp: str  # Assuming you're working with a timestamp to get datetime info

@router.post("/get")
async def get_datetime(request: DatetimeRequest):
    """
    Call the Datetime MCP tool for a given timestamp.
    """
    result = await call_datetime(request.timestamp)
    
    if not result or "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    
    return result
