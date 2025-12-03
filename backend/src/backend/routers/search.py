# backend/src/backend/routers/search.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.mcp_clients import call_ddgs

router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    query: str
    max_results: int = 5


@router.post("/get")
async def search_endpoint(request: SearchRequest):
    """
    Call the DDGS MCP tool for a given query.
    """
    result = await call_ddgs(request.query, request.max_results)

    if not result or "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))

    return result
