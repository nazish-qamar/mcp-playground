from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Service")

@mcp.tool()
def get_weather(location: str) -> str:
    """Get current weather of the specific location"""
    return f"Weather in {location}: Sunny, 72° F"


@mcp.resource("weather://{location}")
def weather_resource(location:str) -> str:
    """provide weather data as resource"""
    return f"Weather data for {location}: Sunny, 72° F"

@mcp.prompt()
def weather_report(location:str) -> str:
    """Create a weather report prompt"""
    return f"You are a weather reported. Weather report for {location}?"

# Run the server
if __name__ == "__main__": 
    mcp.run(transport="sse", port=3001)