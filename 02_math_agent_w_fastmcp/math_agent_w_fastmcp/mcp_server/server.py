import os
import asyncio

from fastmcp import FastMCP


#---------------
# settings
#---------------
host=os.environ.get("FASTMCP_HOST", "0.0.0.0")
port=os.environ.get("FASTMCP_PORT", 8080)
transport=os.environ.get("FASTMCP_TRANSPORT", "sse")    # sse, streamable-http, etc.


#-------------
# mcp
#-------------
# https://gofastmcp.com/servers/fastmcp#server-configuration
mcp = FastMCP(
    name="FastMCP Math Server",
    host=host,
    port=port
)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    return a / b

@mcp.tool()
def quotient(a: int, b: int) -> int:
    """Divide two numbers, ignoring remainder"""
    return a // b


# https://gofastmcp.com/deployment/running-server
if __name__ == "__main__":
    try:
        asyncio.run(mcp.run(transport=transport, host=host, port=port))
    except KeyboardInterrupt:
        print("> FastMCP Math Server stopped by user.")
    except Exception as e:
        print(f"> FastMCP Math Server encountered error: {e}")
    finally:
        print("> FastMCP Math Server exiting.")
