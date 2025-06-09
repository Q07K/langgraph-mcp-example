"""MCP Server time"""

from datetime import datetime

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with configuration
mcp = FastMCP(
    name="time",  # Name of the MCP server
    instructions="You are a time assistant that can provide the current time",  # Instructions for the LLM on how to use this tool
    host="0.0.0.0",  # Host address (0.0.0.0 allows connections from any IP)
    port=8005,  # Port number for the server
)


@mcp.tool()
async def get_time() -> str:
    """
    Get current time in user os".

    Returns:
        str: A string containing the current time information for the specified timezone
    """
    current_time = datetime.now()

    # Format the time as a string
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")

    return f"Current time is: {formatted_time}"


if __name__ == "__main__":
    mcp.run(transport="sse")
