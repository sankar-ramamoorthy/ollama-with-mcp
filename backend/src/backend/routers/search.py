from fastapi import APIRouter, Query
from fastmcp.client.client import CallToolResult
from backend.mcp_clients import call_searchxng

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.get("/search")
async def search_endpoint(query: str = Query(..., description="Search query")):
    """
    Call the SearchXNG MCP tool via backend.
    Returns MCP server results.
    """
    #result = await call_searchxng(query)
    mcp_result: CallToolResult = await call_searchxng(query)
    # Access the actual data from the CallToolResult object
    # Assuming the server returns a dictionary with 'results' and potentially 'error'
    result_data = mcp_result.structured_content or mcp_result.content

    # Optional: if the MCP call failed, return a clear error
    if "error" in result_data:
        return {"success": False, "error": result_data["error"], "results": []}

    return {"success": True, "query": query, "results": result_data.get("results", [])}
    #return(result_data)
