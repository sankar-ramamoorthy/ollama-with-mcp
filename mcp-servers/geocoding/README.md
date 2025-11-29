# Geocoding
 MCP Server


 📍 Geocoding MCP Tool (Nominatim + Python + Async + Rate Limiting)

This MCP tool provides geocoding capabilities using the OpenStreetMap Nominatim API, fully compliant with Nominatim's usage policy, including:

Valid Referer header

1 request per second rate limiting

Async HTTP requests (httpx)

Clean JSON output (lat, lon, city, state, country)

This project is intended for use with MCP-based LLM environments such as
👉 https://github.com/sankar-ramamoorthy/ollama-with-mcp

🚀 Features

✔ Async geocoding using httpx
✔ Nominatim-compliant Referer header
✔ Built-in 1 request/second rate limiting
✔ Graceful error handling
✔ Clean parsed geocoding output
✔ Ready to plug into MCP tools

