from fastapi import APIRouter, HTTPException
from backend.mcp_clients import call_geocoding  # <-- call_geocoding client function
from pydantic import BaseModel

router = APIRouter(prefix="/geocoding", tags=["geocoding"])

class GeocodingRequest(BaseModel):
    address: str

@router.post("/get")
async def get_geocoding(request: GeocodingRequest):
    """
    Call the Geocoding MCP tool for a given address.
    """
    result = await call_geocoding(request.address)
    
    if not result or "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    
    return result
