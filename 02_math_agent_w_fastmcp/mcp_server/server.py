from fastmcp import FastMCP
import asyncio

mcp = FastMCP("FastMCP Math Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    return a // b

if __name__ == "__main__":
    asyncio.run(mcp.run_sse_async(host="0.0.0.0", port=8080))
