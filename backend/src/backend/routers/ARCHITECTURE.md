Frontend / UI
     |
     v
+-----------------+
| FastAPI Backend |
|  Routers        |
|-----------------|
| /chat           | ---> chat_reply() --> LLM
| /mcp/search     | ---> call_searchxng() --> SearchXNG MCP
| /mcp/weather    | ---> call_weather() --> Weather MCP
+-----------------+
     |
     v
+-----------------+       +-----------------+
| MCP Server      |       | MCP Server      |
| SearchXNG MCP   |       | Weather MCP     |
| Port 50052      |       | Port 50053      |
+-----------------+       +-----------------+
     |                         |
     v                         v
 Search API / DB           Weather source
