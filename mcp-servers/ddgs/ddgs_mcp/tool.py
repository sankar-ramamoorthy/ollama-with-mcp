from typing import List, Dict, Any
from pydantic import BaseModel, Field
import logging

from ddgs import DDGS

logger = logging.getLogger("ddgs-mcp")


class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str

class WebSearchResponse(BaseModel):
    query: str
    results: List[SearchResult] = Field(default_factory=list)
    total_results: int = 0

def web_search(query: str, max_results: int = 5) -> WebSearchResponse:
    """
    Perform DuckDuckGo web search.
    """
    if not query or not isinstance(query, str):
        return WebSearchResponse(query=query, results=[])
    
    try:
        results = []
        with DDGS() as ddgs:
            ddgs_results = ddgs.text(query, max_results=max_results)
            for r in ddgs_results:
                results.append(SearchResult(
                    title=r.get("title", ""),
                    link=r.get("href", ""),
                    snippet=r.get("body", "")
                ))
        
        response = WebSearchResponse(
            query=query,
            results=results,
            total_results=len(results)
        )
        logger.info(f"DDGS search '{query}': {len(results)} results")
        return response
    
    except Exception as e:
        logger.error(f"DDGS search error: {e}")
        return WebSearchResponse(query=query, results=[])

