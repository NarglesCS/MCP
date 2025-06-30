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

@mcp.tool()
async def getAlerts(state: str) -> str:
    """Get weather alerts for a United States State code provided as a two digit state code.
    
    Args: 
        state: Two-letter US State Code (As an example MI, FL, CA)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return f"Failed to fetch alerts for the provided state code: {state}"
    
    if not data["features"]:
        return f"No active alerts in {state}"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "/n---/n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get Weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    #First we get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."
    
    #Get the forecast URL fropom the points response
    forecast_url = points_data["properties"]["forecast"]
    forecase_data = await make_nws_request(forecast_url)

    if not forecase_data:
        return "Unable to fetch detailed forecast."
    
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "/n---/n".join(forecasts)


if __name__ == "__main__":
    mcp.run(transport='stdio')