# MCP tutorial project

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the National Weather System API with proper error handling."""
    headers = {
        "User-Agent" : USER_AGENT,
        "Accept" : "application/geo+json" #RFC7946 - https://datatracker.ietf.org/doc/html/rfc7946
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0) #Time out is in seconds
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
    
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string for output."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description availiable')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""